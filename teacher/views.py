from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TeacherModel, ClassModel
from .form import TeacherForm, ClassForm
from account.models import CustomUser, TeacherProfile
from account.decorator import role_required

# Create your views here.
@role_required('ADMIN','TEACHER')
def show_teacher(request):
    teachers = TeacherModel.objects.all()
    
    form = TeacherForm()
    
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            # Auto-link to existing TEACHER user with matching email
            try:
                user = CustomUser.objects.get(email=teacher.email, role='TEACHER')
                TeacherProfile.objects.get_or_create(
                    user=user,
                    defaults={'teacher': teacher, 'phone': teacher.phone_number}
                )
                messages.success(request, f'Teacher "{teacher.name}" linked to user account {user.email}.')
            except CustomUser.DoesNotExist:
                pass
            return redirect('show_teachers')
    return render(request, 'teacher/teacher.html', {'teachers': teachers})

@role_required('ADMIN','TEACHER')
def show_class(request):
    teachers = TeacherModel.objects.all()
    classes = ClassModel.objects.all()
    
    form = ClassForm()
    
    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_classes')
    
    return render(request, 'teacher/class.html', {'classes': classes, 'teachers': teachers})

@role_required('ADMIN')
def edit_teacher(request, id):
    teacher = get_object_or_404(TeacherModel, id=id)
    form = TeacherForm(instance=teacher)
    teachers = TeacherModel.objects.all()
    if request.method == "POST":
        form = TeacherForm(
            request.POST,
            instance = teacher
        )
        
        if form.is_valid():
            form.save()
            return redirect('show_teachers')
    return render(request, 'teacher/teacher.html', {'form': form, 'teachers': teachers})

@role_required('ADMIN')
def delete_teacher(request, id):
    teacher = get_object_or_404(TeacherModel, id=id)
    teacher.delete()
    return redirect('show_teachers')

@role_required('ADMIN')
def edit_class(request, id):
    std_class = get_object_or_404(ClassModel, id=id)
    form = ClassForm(instance=std_class)
    teachers = TeacherModel.objects.all()
    classes = ClassModel.objects.all()  
    
    if request.method == "POST":
        form = ClassForm(
            request.POST,
            instance = std_class
        )
        
        if form.is_valid():
            form.save()
            return redirect('show_classes')
    return render(request, 'teacher/class.html', {'form': form, 'classes': classes, 'teachers': teachers})

@role_required('ADMIN')       
def delete_class(request, id):
    std_class = get_object_or_404(ClassModel, id=id)
    std_class.delete()
    return redirect('show_classes')