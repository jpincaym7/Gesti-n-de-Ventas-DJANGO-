from core.models import Invoice, InvoiceDetail
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

def InvoiceList(request):
    invoices = Invoice.objects.filter(user=request.user)
    for invoice in invoices:
        print(invoice)
    data = {
        "title1": "Facturas del Cliente"
    }
    data["invoices"] = invoices
    return render(request, 'core/shop/invoice_list.html', data)

def get_invoice_details(request):
    invoice_id = request.GET.get('invoice_id')
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        details = InvoiceDetail.objects.filter(invoice=invoice)
        invoice_details = {
            'id': invoice.id,
            'customer': {
                'id': invoice.customer.id,
                'name': f'{invoice.customer.first_name} {invoice.customer.last_name}',
                "image": invoice.customer.image.url,
                "correo": invoice.customer.email,
                "address": invoice.customer.address
            },
            'payment_method': {
                'id': invoice.payment_method.id,
                'name': invoice.payment_method.description,
            },
            "subtotal": float(invoice.subtotal),
            "total": float(invoice.total),
            "details": [{
                'product_name': detail.product.description,
                'quantity': int(detail.quantity),
                'price': float(detail.price),
                'total': float(detail.quantity * detail.price),
                'iva': detail.iva
            } for detail in details],
            "tax": float(sum(detail.iva for detail in details)) # Calcular el total del IVA
        }
        return JsonResponse(invoice_details)
    except Invoice.DoesNotExist:
        return JsonResponse({'error': 'Invoice not found'}, status=404)

def InvoiceViews(request, InvoiceId):
    invoices = Invoice.objects.get(pk=id)