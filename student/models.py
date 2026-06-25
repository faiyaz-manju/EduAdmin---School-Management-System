from django.db import models
from teacher.models import ClassModel

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10)
    adhar_number = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    student_class = models.ForeignKey(ClassModel, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
