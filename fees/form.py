from django import forms
from .models import FeesMasterModel, PaymentModel

class FeesMasterForm(forms.ModelForm):
    
    class Meta:
        
        model = FeesMasterModel
        fields = '__all__'


class PaymentForm(forms.ModelForm):

    class Meta:

        model = PaymentModel
        fields = ['student_name', 'amount']

