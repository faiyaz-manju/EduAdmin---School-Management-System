from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from .models import FeesMasterModel, ReceiptCounter, PaymentModel
from decimal import Decimal
from teacher.models import ClassModel
from student.models import Student
from .form import FeesMasterForm, PaymentForm
from account.decorator import role_required

# Create your views here.
@role_required('ADMIN')
def master(request):
    classes = ClassModel.objects.all()
    
    
    form = FeesMasterForm()
    
    if request.method == 'POST':
        form = FeesMasterForm(request.POST)
        if form.is_valid():
            FeesMasterModel.objects.update_or_create(
                student_class = form.cleaned_data['student_class'],
                defaults={
                    'admission': form.cleaned_data['admission'],
                    'hostel': form.cleaned_data['hostel'],
                    'transport': form.cleaned_data['transport'],
                    'school': form.cleaned_data['school'],
                    'tuition': form.cleaned_data['tuition'],
                }
            )
            return redirect('master')
        else:
            return HttpResponse("Invalid form data")
        
        
    feemaster = FeesMasterModel.objects.all()
    context = {
        'feemaster' : feemaster,
        'form' : form,
        'classes' : classes,
        }
                    
    return render(request, 'fees/master.html', context)
    

# def delete_fees(request, id):
#     fee = FeesMasterModel.objects.get(id=id)
#     fee.delete()
#     return redirect('master')

    

@role_required('ADMIN')
def payment(request):
    students = Student.objects.all()
    payments = PaymentModel.objects.all()
    return render(request, 'fees/payment.html', {'students': students, 'payments': payments})

@role_required('ADMIN')
def add_payment(request):
    
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student_name']
            amount = form.cleaned_data['amount']
            
            year = timezone.now().year
            with transaction.atomic():
                counter = ReceiptCounter.objects.select_for_update().get_or_create(year=year, defaults={'last':0})[0]
                counter.last += 1
                n = counter.last
                counter.save(update_fields=['last'])
                
                receipt = f"RCP-{year}-{n:03d}"
                
                payment = form.save(commit=False)
                payment.receipt_number = receipt
                payment.save()
                
            return redirect('generate_receipt', payment.id)
        else:
            return HttpResponse("Invalid Form", status=400)
    return redirect('payment')
            
@role_required('ADMIN')         
def generate_receipt(request, id):
    payment = get_object_or_404(PaymentModel, id=id)
    # Build fee breakdown from FeesMasterModel for the student's class
    student = payment.student_name
    feemaster = None
    try:
        feemaster = FeesMasterModel.objects.get(student_class=student.student_class)
    except FeesMasterModel.DoesNotExist:
        feemaster = None

    fee_items = []
    total_due = Decimal('0.00')
    if feemaster:
        # ordered list of fields and display labels coming from FeesMasterModel
        fields = [
            ('admission', 'Admission'),
            ('hostel', 'Hostel'),
            ('transport', 'Transport'),
            ('school', 'School'),
            ('tuition', 'Tuition'),
        ]
        for attr, label in fields:
            amt = getattr(feemaster, attr, 0) or 0
            amt = Decimal(amt)
            fee_items.append({'label': label, 'amount': amt})
            total_due += amt

    outstanding = total_due - Decimal(payment.amount or 0)

    context = {
        'payment': payment,
        'fee_items': fee_items,
        'total_due': total_due,
        'outstanding': outstanding,
    }
    return render(request, 'receipts/receipt.html', context)