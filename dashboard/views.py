from django.shortcuts import render
from django.http import HttpResponse
from account.decorator import role_required

# Create your views here.
@role_required('ADMIN','TEACHER')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')