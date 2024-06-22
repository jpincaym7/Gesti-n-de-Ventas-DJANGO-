from django.urls import path
from core import views
from django.contrib.auth.decorators import login_required

from core.shop import invoice_detail_view, invoice_view
from core.invoice import InvoiceList, get_invoice_details
from .views import home, UserRegistrationView, LoginView, sesionLogout, edit_profile
from .products import AddToCartView, UpdateCartItemView, product_List
 
app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("edit/", edit_profile, name="edit"),
    path("logout/", sesionLogout, name="logout"),
    path("home/", login_required(views.home), name="home"),
    path('products/', login_required(product_List), name='product_list'),
    path('add/', login_required(AddToCartView.as_view()), name='add_to_cart'),
    path('update-cart-item/', login_required(UpdateCartItemView.as_view()), name='update_cart_item'),
    path("invoice/",login_required(invoice_view),name="invoice_view"),
    path("details/<int:invoice_id>/", login_required(invoice_detail_view), name="invoice_detail"),
    path("list_invoice/",login_required(InvoiceList),name="list_invoice"),
    path('get_invoice_details', login_required(get_invoice_details), name='get_invoice_details'),
]