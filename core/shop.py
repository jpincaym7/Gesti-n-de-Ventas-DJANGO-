from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.forms import ProductForm
from core.models import Product, Brand
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem, Invoice, InvoiceDetail, Customer
from django.contrib.auth.decorators import login_required
import json
import stripe

@login_required
def borrar_carrito(request):
    try:
        # Obtener el carrito del usuario
        carrito = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # Si el carrito no existe, redirigir a algún lugar
        return redirect('core:home')

    print(carrito)
    print("carrito borrado")

    # Borrar el carrito y sus elementos asociados de manera física
    carrito.delete()



def invoice_detail_view(request, invoice_id):
    # Obtener la factura y sus detalles asociados
    invoice = Invoice.objects.get(id=invoice_id)
    details = InvoiceDetail.objects.filter(invoice=invoice)
    for detail in details:
        detail.quantity = int(detail.quantity)  # Convertir a entero
    
    return render(request, 'core/shop/invoice_detail.html', {'invoice': invoice, 'details': details})

@login_required
def invoice_view(request):
    # Obtener el cliente asociado al usuario que ha iniciado sesión
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        # Obtener el carrito del usuario
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Crear la factura y los detalles de la factura
        invoice = Invoice.objects.create(
            customer=customer,
            subtotal=cart.total_cost(),
            total=cart.total_cost(),
            user=request.user
        )

        for cart_item in cart_items:
            InvoiceDetail.objects.create(
                invoice=invoice,
                product=cart_item.product,
                quantity=int(cart_item.quantity),
                price=cart_item.product.price,
                iva=cart_item.product.iva
            )

        # Procesar el pago utilizando Stripe
        stripe.api_key = 'sk_test_51PP7K905iukLqcQyrTHerMvEroAsIDiC13vC26TUsLFyHPBCA48gyCWT2lbZzHfe05HeNBTX0EyICw4pQf9EZ6o800SJa1Uei1'

        try:
            # Crear el PaymentIntent de Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(cart.total_cost() * 100),  # El monto se debe especificar en centavos
                currency='usd',
                description='Compra en MiTienda',
                receipt_email=request.user.email,
            )

            client_secret = payment_intent['client_secret']

            # Marcar la factura como pagada
            invoice.paid = True
            invoice.save()

            # Borrar el carrito de manera lógica
            borrar_carrito(request)

            # Redireccionar a la página de detalle de factura
            return redirect('core:invoice_detail', invoice_id=invoice.id)

        except stripe.error.CardError as e:
            # Si hay un error con la tarjeta, mostrar un mensaje de error
            error_msg = e.error.message
            return render(request, 'core/shop/invoice.html', {'error_msg': error_msg})

    else:
        # Obtener el carrito del usuario
        cart = Cart.objects.get(user=request.user)

        # Crear el PaymentIntent de Stripe
        stripe.api_key = 'sk_test_51PP7K905iukLqcQyrTHerMvEroAsIDiC13vC26TUsLFyHPBCA48gyCWT2lbZzHfe05HeNBTX0EyICw4pQf9EZ6o800SJa1Uei1'

        payment_intent = stripe.PaymentIntent.create(
            amount=int(cart.total_cost() * 100),  # El monto se debe especificar en centavos
            currency='usd',
            description='Compra en MiTienda',
            receipt_email=request.user.email,
        )

        client_secret = payment_intent['client_secret']

        return render(request, 'core/shop/invoice.html', {'client_secret': client_secret})