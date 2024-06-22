from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.forms import ProductForm
from core.models import Product, Brand
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem, Product
import json

def product_List(request):
    brands = Brand.objects.all()
    brand_id = request.GET.get("brand_id")
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos",
    }
    products = Product.objects.filter(brand=brand_id)
    for product in products:
        if not product.image:
            product.image = 'products/default.png'  # Ruta a una imagen por defecto
    if not products:
        products = Product.objects.all()
        data["products"] = products
        data["brands"] = brands
        return render(request, "core/shop/varios.html", data)
    data["products"] = products
    data["brands"] = brands
    return render(request, "core/shop/list.html", data)

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        
        cart, created = Cart.objects.get_or_create(user=request.user, state=True)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if created:
            if product.stock < 1:
                return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
            cart_item.quantity = 1
        else:
            if product.stock < cart_item.quantity + 1:
                return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
            cart_item.quantity += 1
        
        product.reduce_stock(1)
        product.save()
        cart_item.save()

        cart_items = CartItem.objects.filter(cart=cart)
        items_data = [
            {
                'product_id': item.product.id,
                'product_description': item.product.description,
                'product_price': float(item.product.price),
                'product_image_url': item.product.image.url if item.product.image else '',
                'quantity': int(item.quantity),
                'total_price': float(item.quantity * item.product.price)
            } for item in cart_items
        ]

        return JsonResponse({
            'cart_item_count': cart.total_items(),
            'cart_total': float(cart.total_cost()),
            'cart_items': items_data
        })

    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user, state=True)
        cart_items = CartItem.objects.filter(cart=cart, state=True)
        items_data = [
            {
                'product_id': item.product.id,
                'product_description': item.product.description,
                'product_price': float(item.product.price),
                'product_image_url': item.product.image.url if item.product.image else '',
                'quantity': int(item.quantity),
                'total_price': float(item.quantity * item.product.price)
            } for item in cart_items
        ]
        return JsonResponse({
            'cart_item_count': cart.total_items(),
            'cart_total': float(cart.total_cost()),
            'cart_items': items_data
        })

class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)

        cart, created = Cart.objects.get_or_create(user=request.user, state=True)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if action == 'increment':
            if product.stock < 1:
                return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
            cart_item.quantity += 1
            product.reduce_stock(1)
            product.save()
            cart_item.save()
        elif action == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                product.increase_stock(1)
                product.save()
                cart_item.save()
            else:
                product.increase_stock(cart_item.quantity)
                product.save()
                cart_item.delete()

        cart_items = [
            {
                'product_id': item.product.id,
                'product_description': item.product.description,
                'product_price': float(item.product.price),
                'product_image_url': item.product.image.url if item.product.image else '',
                'quantity': int(item.quantity),
                'total_price': float(item.quantity * item.product.price)
            } for item in cart.cart_items.all()
        ]

        return JsonResponse({
            'cart_item_count': cart.total_items(),
            'cart_total': float(cart.total_cost()),
            'cart_items': cart_items
        })
