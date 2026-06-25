from django import forms
from .models import TeacherModel, ClassModel

class TeacherForm(forms.ModelForm):

    class Meta:

        model = TeacherModel
        fields = '__all__'
        

class ClassForm(forms.ModelForm):

    class Meta:

        model = ClassModel
        fields = '__all__'


