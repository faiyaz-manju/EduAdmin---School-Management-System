from django.db import models
from teacher.models import ClassModel
from student.models import Student

# Create your models here.
class FeesMasterModel(models.Model):
    student_class = models.ForeignKey(ClassModel, on_delete=models.CASCADE)
    admission = models.DecimalField(max_digits=10, decimal_places=2)
    hostel = models.DecimalField(max_digits=10, decimal_places=2)
    transport = models.DecimalField(max_digits=10, decimal_places=2)
    school = models.DecimalField(max_digits=10, decimal_places=2)
    tuition = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.student_class.class_name
    

class PaymentModel(models.Model):
    receipt_number = models.CharField(max_length=100, unique=True)
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.receipt_number
    
class ReceiptCounter(models.Model):
    year = models.IntegerField(unique=True, db_index=True)
    last = models.BigIntegerField(default=0)