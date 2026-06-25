from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Student
from teacher.models import ClassModel
from .form import StudentForm
from account.decorator import role_required
from account.models import ParentsProfile


def _auto_link_parents(student):
    def match_parents(name):
        if not name:
            return
        parts = name.strip().split(maxsplit=1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ''
        q = Q(user__first_name__iexact=first)
        if last:
            q &= Q(user__last_name__iexact=last)
        for profile in ParentsProfile.objects.filter(q):
            profile.students.add(student)
    
    match_parents(student.father_name)
    match_parents(student.mother_name)
# Create your views here.

@role_required('ADMIN','TEACHER')
def show_students(request):
    # Admins see all students; teachers see only students for their classes
    if getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'role', '').upper() == 'TEACHER':
        # Try to find the linked TeacherProfile -> TeacherModel
        teacher_profile = getattr(request.user, 'teacher_profile', None)
        if teacher_profile and getattr(teacher_profile, 'teacher', None):
            teacher_model = teacher_profile.teacher
            classes = ClassModel.objects.filter(class_teacher=teacher_model)
            students = Student.objects.filter(student_class__in=classes)
        else:
            # No teacher profile linked — show empty queryset
            students = Student.objects.none()
    else:
        students = Student.objects.all()

    return render(request, 'students/show-students.html', {'students': students})

@role_required('ADMIN')
def add_student(request):
    form = StudentForm()
    classes = ClassModel.objects.all()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Auto-link to parents matching father_name or mother_name
            _auto_link_parents(student)
            return redirect('show_students')
    return render(request, 'students/add-student.html', {'form': form, 'classes': classes})

@role_required('ADMIN')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(instance=student)
    classes = ClassModel.objects.all()

    if request.method == "POST":
        form = StudentForm(
            request.POST,
            instance= student
        )
        
        if form.is_valid():
            student = form.save()
            # Auto-link to parents matching father_name or mother_name
            _auto_link_parents(student)
            # Handle manual parent linking from form
            parent_ids = request.POST.getlist('linked_parents')
            if parent_ids:
                for profile in ParentsProfile.objects.filter(id__in=parent_ids):
                    profile.students.add(student)
            return redirect('show_students')
    parent_profiles = ParentsProfile.objects.all()
    return render(request, 'students/edit-student.html', {
        'form': form, 'student': student, 'classes': classes,
        'parent_profiles': parent_profiles,
    })

@role_required('ADMIN','TEACHER')
def student_profile(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/student-profile.html', {'student': student})