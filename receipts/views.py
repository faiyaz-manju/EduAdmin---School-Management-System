from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from student.models import Student
from fees.models import PaymentModel, FeesMasterModel
from account.decorator import role_required

# Create your views here.
@role_required('ADMIN')
def show_receipts(request):
    receipts = PaymentModel.objects.all()
    students = Student.objects.all()
    return render(request, 'receipts/list.html', {'receipts': receipts, 'students': students})

@role_required('ADMIN')
def receipt(request, id):
    payment = get_object_or_404(PaymentModel, id=id)
    student = payment.student_name

    feemaster = FeesMasterModel.objects.filter(student_class=student.student_class).first()

    fee_items = []
    total_due = Decimal('0.00')
    if feemaster:
        for attr, label in [
            ('admission', 'Admission'),
            ('hostel', 'Hostel'),
            ('transport', 'Transport'),
            ('school', 'School'),
            ('tuition', 'Tuition'),
        ]:
            amount = Decimal(getattr(feemaster, attr) or 0)
            fee_items.append({'label': label, 'amount': amount})
            total_due += amount

    outstanding = total_due - Decimal(payment.amount or 0)

    context = {
        'payment': payment,
        'fee_items': fee_items,
        'total_due': total_due,
        'outstanding': outstanding,
    }
    return render(request, 'receipts/receipt.html', context)

@role_required('ADMIN','TEACHER','PARENT')
def download_receipt(request, id):
    import weasyprint

    payment = get_object_or_404(PaymentModel, id=id)
    student = payment.student_name

    feemaster = FeesMasterModel.objects.filter(student_class=student.student_class).first()

    fee_items = []
    total_due = Decimal('0.00')
    if feemaster:
        for attr, label in [
            ('admission', 'Admission'),
            ('hostel', 'Hostel'),
            ('transport', 'Transport'),
            ('school', 'School'),
            ('tuition', 'Tuition'),
        ]:
            amount = Decimal(getattr(feemaster, attr) or 0)
            fee_items.append({'label': label, 'amount': amount})
            total_due += amount

    outstanding = total_due - Decimal(payment.amount or 0)

    context = {
        'payment': payment,
        'fee_items': fee_items,
        'total_due': total_due,
        'outstanding': outstanding,
    }

    # Render HTML from the same receipt template
    html_string = render_to_string('receipts/receipt.html', context=context, request=request)

    # Convert HTML to PDF with WeasyPrint
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    css = weasyprint.CSS(string='@page { size: A4; margin: 12mm align-content: center; }')
    pdf = html.write_pdf(stylesheets=[css])

    # Return PDF as attachment
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"{payment.receipt_number}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response