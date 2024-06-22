from django.contrib import admin
from core.models import Category,Brand, Customer, Supplier,Product, Profile, Cart, CartItem, Invoice, InvoiceDetail

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated')
    search_fields = ('user__username', 'id')
    ordering = ('id',)

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'state', 'created', 'updated')
    list_filter = ('cart', 'product', 'state')
    search_fields = ('cart__id', 'product__description')
    ordering = ('cart', 'product')
    readonly_fields = ('created', 'updated')
    actions = ['mark_as_inactive', 'mark_as_active']

    def mark_as_inactive(self, request, queryset):
        queryset.update(state=False)
    mark_as_inactive.short_description = "Marcar seleccionados como inactivos"

    def mark_as_active(self, request, queryset):
        queryset.update(state=True)
    mark_as_active.short_description = "Marcar seleccionados como activos"

admin.site.register(CartItem, CartItemAdmin)
# Registra la clase ProductAdmin como administrador de los modelos de tipo Product en el panel de administración de Django
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Especifica los campos que se mostrarán en la lista de productos en el panel de administración
    list_display = ['description', 'price', 'stock', 'brand','supplier','line','categorias','state']
    # Define los campos por los cuales se pueden filtrar los productos en el panel de administración
    list_filter = ['state', 'brand','line']
    # Especifica los campos por los cuales se puede buscar productos en el panel de administración
    search_fields = ['description']
    # Define un filtro de jerarquía de fechas en el panel de administración para los productos
    date_hierarchy = 'expiration_date'
    # Define el orden en el que se muestran los productos en la lista del panel de administración
    ordering = ['description']

    # Define un método para mostrar las categorías de cada producto en la lista del panel de administración
    def categorias(self, obj):
        # Devuelve una cadena que contiene las descripciones de todas las categorías asociadas al producto, separadas por un guion (-)
        return " - ".join([c.description for c in obj.categories.all().order_by('description')])