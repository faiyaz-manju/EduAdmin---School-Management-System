from django import forms
from .models import CustomUser

class UserForm(forms.ModelForm):

    class Meta:

        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role']
