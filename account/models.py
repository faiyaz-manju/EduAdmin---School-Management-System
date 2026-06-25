from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('must_change_password', False)
        return self.create_user(email, password, **extra_fields)
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('PARENT', 'Parent'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} ({self.role})"    
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        # Auto-sync role with Django permission flags
        if self.role == 'ADMIN':
            self.is_staff = True
        elif self.role == 'TEACHER':
            self.is_staff = True
            self.is_superuser = False
        elif self.role == 'PARENT':
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
    

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher = models.OneToOneField('teacher.TeacherModel', on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"Teacher Profile - {self.user.full_name}"
    
class ParentsProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent_profile')
    students = models.ManyToManyField('student.Student', blank=True, related_name='parents')
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"Parent Profile - {self.user.full_name}"
    
    
    

        