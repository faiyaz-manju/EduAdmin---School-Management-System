from django import forms
from .models import ExpenditureModel

class ExpenditureForm(forms.ModelForm):

    class Meta:

        model = ExpenditureModel
        fields = ['category', 'description', 'amount', 'date']
