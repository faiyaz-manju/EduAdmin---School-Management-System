from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','father_name','mother_name','date_of_birth','phone_number','adhar_number','email','address','student_class',]