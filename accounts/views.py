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
        return redirect('home')
    
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
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.email}!')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except User.DoesNotExist:
            messages.error(request, 'El correo no está registrado.')
    
    return render(request, 'accounts/login.html')


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('home')


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
