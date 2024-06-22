from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from core.forms import UserRegistrationForm, LoginForm, EditProfileForm
from core.forms import ProductForm
from core.models import Product, Profile, Brand, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, SESSION_KEY, get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    Brands = Brand.objects.all()
    data = {
        "header": "Home",
        "src": ["img/koaj-rebajas.jpeg", "img\pinto.jpg"],
        "jeans": "img\jeans.jpg",
        "marcas": ["img\pulland.jpg", "img\campana-pull-and-bear.jpg", "img/rebaja.jpg","img/articles.jpg","img\zara.jpg","img\local.jpg"]
    }
    data["brands"] = Brands
    return render(request, 'core/home.html', data)


class UserRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('admin:index')  # Redirigir al admin si ya está autenticado como staff
        form = UserRegistrationForm()
        return render(request, 'core/auth/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('admin:index')  # Redirigir al admin si ya está autenticado como staff
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            imagen = form.cleaned_data.get('imagen')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nombre de usuario ya en uso. Por favor, intenta con otro.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Correo electrónico ya en uso. Por favor, intenta con otro.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                if imagen:
                    Profile.objects.create(user=user, image=imagen)
                messages.success(request, 'Usuario registrado exitosamente. Por favor, inicia sesión.')
                return redirect('login')
        else:
            messages.error(request, 'Hubo un error con tu registro. Por favor, revisa el formulario y completa los datos correctamente.')
        return render(request, 'core/auth/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('admin:index')  # Redirigir al admin si ya está autenticado como staff
        form = LoginForm()
        return render(request, 'core/auth/login.html', {'form': form})
    def post(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('admin:index')  # Redirigir al admin si ya está autenticado como staff
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            keep_logged_in = form.cleaned_data.get('keep_logged_in', False)  # Obtener el valor del campo
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not keep_logged_in:  # Si el usuario no seleccionó "mantener la sesión iniciada"
                    request.session.set_expiry(0)  # Duración de sesión corta
                messages.success(request, 'INICIO DE SESIÓN EXITOSO.')
                return redirect('core:home')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Formulario inválido. Por favor, revisa los datos proporcionados.')
        return render(request, 'core/auth/login.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'TU PERFIL SE HA ACTUALIZADO CON EXITO.')
            return redirect('core:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
                    # You can customize the messages further if needed
    else:
        form = EditProfileForm(instance=request.user)
    
    # Verificar si el usuario tiene una imagen de perfil, si no, establecer la imagen predeterminada
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if not profile.image:
        profile.image = 'profiles/default.png'
        profile.save()
        messages.info(request, 'No tenías una imagen de perfil. Se ha asignado una imagen predeterminada.')

    return render(request, 'core/auth/edit_profile.html', {'form': form})

def sesionLogout(request):
    logout(request)
    return redirect('login')