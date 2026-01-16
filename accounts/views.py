from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from .forms import RegistroForm, LoginForm, RecuperarForm


@require_http_methods(["GET", "POST"])
def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'accounts/registro.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = authenticate(request, username=identifier, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name or user.username or user.email}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas. Revisa tu correo/usuario y contraseña.')
    
    return render(request, 'accounts/login.html')


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


class RecuperarContraseña(PasswordResetView):
    form_class = RecuperarForm
    template_name = 'accounts/recuperar.html'
    email_template_name = 'accounts/email_recuperar.txt'
    subject_template_name = 'accounts/subject_recuperar.txt'
    success_url = reverse_lazy('password_reset_done')


class RecuperarContraseñaConfirm(PasswordResetConfirmView):
    template_name = 'accounts/recuperar_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class RecuperarContraseñaComplete(PasswordResetCompleteView):
    template_name = 'accounts/recuperar_complete.html'
