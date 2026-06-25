from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ExpenditureModel
from .form import ExpenditureForm
from account.decorator import role_required

# Create your views here.
@role_required('ADMIN')
def expenditure(request):
    expenditures = ExpenditureModel.objects.all()
    
    
    form = ExpenditureForm()
    
    if request.method == 'POST':
        form = ExpenditureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenditure')
        else:
            context = {
                'expenditures': expenditures,
                'form': form
            }
            return render(request, 'expenditure/expenditure.html', context)
    else:
        form = ExpenditureForm()
        
        context = {
            'expenditures': expenditures,
            'form': form
        }
    return render(request, 'expenditure/expenditure.html', context)