from django.db import models

# Create your models here.
class TeacherModel(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14)
    subject = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    
    
    def __str__(self):
        return self.name


class ClassModel(models.Model):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    capacity = models.BigIntegerField()
    class_teacher = models.ForeignKey(TeacherModel, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.class_name
    