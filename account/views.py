from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse
from .models import CustomUser, TeacherProfile, ParentsProfile
from student.models import Student
from teacher.models import TeacherModel, ClassModel
from fees.models import FeesMasterModel, PaymentModel
from account.decorator import role_required

# Create your views here.
@role_required('PARENT')
def parents_portal(request):
    parent_profile = request.user.parent_profile
    
    # Auto-match students by parent name if none linked yet
    if not parent_profile.students.exists():
        parent_name = request.user.full_name.strip()
        matched = Student.objects.filter(
            Q(father_name__iexact=parent_name) | Q(mother_name__iexact=parent_name)
        )
        if matched.exists():
            parent_profile.students.add(*matched)
    
    children = parent_profile.students.all()

    selected_child_id = request.GET.get('child')
    if selected_child_id:
        selected_child = get_object_or_404(Student, id=selected_child_id, parents=parent_profile)
    else:
        selected_child = children.first()

    context = {
        'children': children,
        'selected_child': selected_child,
    }

    if not selected_child:
        return render(request, 'account/portal.html', context)

    # Fee structure for the child's class
    feemaster = FeesMasterModel.objects.filter(
        student_class=selected_child.student_class
    ).first()

    # Total paid by this child
    total_paid = PaymentModel.objects.filter(
        student_name=selected_child
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Build fee breakdown
    fee_types = [
        ('admission', 'Admission'),
        ('hostel', 'Hostel'),
        ('transport', 'Transport'),
        ('school', 'School Fee'),
        ('tuition', 'Tuition'),
    ]
    fee_breakdown = []
    total_due = Decimal('0.00')
    if feemaster:
        for attr, label in fee_types:
            amount = getattr(feemaster, attr, 0) or 0
            amount = Decimal(str(amount))
            total_due += amount
            fee_breakdown.append({'type': label, 'total': amount, 'paid': 0, 'percent': 0})

        # Distribute total_paid proportionally across fee types
        if total_due > 0 and total_paid > 0:
            for item in fee_breakdown:
                ratio = item['total'] / total_due
                paid = (total_paid * ratio).quantize(Decimal('0.01'))
                item['paid'] = paid
                item['percent'] = int((paid / item['total']) * 100) if item['total'] > 0 else 0

    total_outstanding = total_due - total_paid if feemaster else Decimal('0.00')

    payments = PaymentModel.objects.filter(
        student_name=selected_child
    ).order_by('-date')

    context.update({
        'fee_breakdown': fee_breakdown,
        'total_outstanding': total_outstanding,
        'total_due': total_due,
        'total_paid': total_paid,
        'payments': payments,
    })

    return render(request, 'account/portal.html', context)

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'PARENT':
            return redirect('account:portal')
        
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = email, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.must_change_password:
                return redirect('account:change_password')
            
            if user.role == "PARENT":
                return redirect('account:portal')
            
            if user.role == "TEACHER":
                return redirect('show_students')
            
            return redirect('dashboard')
    
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('account:login')

def register_view(request):
    if CustomUser.objects.filter(role='ADMIN').exists():
        messages.error(request, 'Setup already Complete. Please log in.')
        return redirect('account:login')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('account:register')
        
        user = CustomUser.objects.create_superuser(
            email = email,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.must_change_password = False
        user.save()
        messages.success(request, 'Admin account is created. Please Log in. ')
        return redirect('account:login')
    
    return render(request, 'account/register.html')

def change_password_view(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Password do not match.')
            return redirect('account:change_password')
        
        if len(password1) < 8 :
            messages.error(request, 'Password must be at least 8 characters')
            return redirect('account:change_password')

        request.user.set_password(password1)
        request.user.must_change_password = False
        request.user.save()
        
        # Re-authenticate so session stays valid after password change
        user = authenticate(request, username=request.user.email, password=password1)
        login(request, user)
        messages.success(request, 'Password changed successfully.')

        if request.user.role == 'PARENT':
            return redirect('account:portal')
        elif request.user.role == 'TEACHER':
            return redirect('show_students')
        return redirect('account:login')
    
    return render(request, 'account/change_password.html')

@role_required('ADMIN')
def user_management_view(request):
    
    if request.method =="POST":
        email = request.POST.get('email')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Password do not match. try again.")
            return redirect('account:user')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with this email has already exist.")
            return redirect('account:user')
        
        full_name = request.POST.get('full_name', '').strip()
        if not full_name:
            messages.error(request, 'Full name is required.')
            return redirect('account:user')
        parts = full_name.split(maxsplit=1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''
        
        if role == 'TEACHER':
            subject = request.POST.get('subject', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
        elif role == 'PARENT':
            phone_number = request.POST.get('phone_number', '').strip()
            student_ids = request.POST.getlist('students')
        
        user = CustomUser.objects.create_user(
            email = email,
            password = password1,
            first_name = first_name,
            last_name = last_name,
            role = role,
        )
        user.must_change_password = True
        if role == "ADMIN":
            user.is_staff = True
            user.is_active = True
        user.save()
        
        if role == 'TEACHER':
            teacher = TeacherModel.objects.create(
                name=full_name,
                email=email,
                subject=subject,
                phone_number=phone_number,
            )
            TeacherProfile.objects.create(
                user=user,
                teacher=teacher,
                phone=phone_number,
            )
        elif role == 'PARENT':
            parent_profile = ParentsProfile.objects.create(
                user=user,
                phone=phone_number,
            )
            if student_ids:
                parent_profile.students.set(Student.objects.filter(id__in=student_ids))
        
        messages.success(request, f'{role.capitalize()} account has been created for {email}.')
        return redirect('account:user')
    
    total_users = CustomUser.objects.count()
    pending_users = CustomUser.objects.filter(must_change_password=True).count()
    locked_users = CustomUser.objects.filter(is_active=False).count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    students = Student.objects.all()
    
    return render(request, 'account/user_management.html', {
        'total_users': total_users,
        'pending_users': pending_users,
        'locked_users': locked_users,
        'recent_users': recent_users,
        'students': students,
    })

@role_required('ADMIN')
def edit_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    
    if request.method == "POST":
        email = request.POST.get('email')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'True'
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 and password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('account:edit_user', id=id)
        
        if email != user.email and CustomUser.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return redirect('account:edit_user', id=id)
        
        full_name = request.POST.get('full_name', '').strip()
        if not full_name:
            messages.error(request, 'Full name is required.')
            return redirect('account:edit_user', id=id)
        parts = full_name.split(maxsplit=1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''
        
        if role == 'TEACHER':
            subject = request.POST.get('subject', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
        elif role == 'PARENT':
            phone_number = request.POST.get('phone_number', '').strip()
            student_ids = request.POST.getlist('students')
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.role = role
        user.is_active = is_active
        
        if password1:
            user.set_password(password1)
            user.must_change_password = True
        
        user.save()
        
        if role == 'TEACHER':
            teacher, _ = TeacherModel.objects.get_or_create(
                email=email,
                defaults={'name': full_name, 'subject': subject, 'phone_number': phone_number}
            )
            if teacher.name != full_name or teacher.subject != subject or teacher.phone_number != phone_number:
                teacher.name = full_name
                teacher.subject = subject
                teacher.phone_number = phone_number
                teacher.save()
            TeacherProfile.objects.get_or_create(
                user=user,
                defaults={'teacher': teacher, 'phone': phone_number}
            )
        elif role == 'PARENT':
            parent_profile, created = ParentsProfile.objects.get_or_create(
                user=user,
                defaults={'phone': phone_number}
            )
            if not created:
                parent_profile.phone = phone_number
                parent_profile.save()
            if student_ids:
                parent_profile.students.add(*student_ids)
        
        messages.success(request, f'User {user.email} updated successfully.')
        return redirect('account:user')
    
    total_users = CustomUser.objects.count()
    pending_users = CustomUser.objects.filter(must_change_password=True).count()
    locked_users = CustomUser.objects.filter(is_active=False).count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    students = Student.objects.all()
    
    return render(request, 'account/user_management.html', {
        'total_users': total_users,
        'pending_users': pending_users,
        'locked_users': locked_users,
        'recent_users': recent_users,
        'students': students,
        'edit_user_obj': user,
    })

@role_required('ADMIN')
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if user == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('account:user')
    email = user.email
    user.delete()
    messages.success(request, f'User {email} deleted successfully.')
    return redirect('account:user')
