from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy, reverse
from .forms import RegistroForm, LoginForm, RecuperarForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


@require_http_methods(["GET", "POST"])
def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Desactivar hasta que confirme email
            user.save()
            # Enviar email de activación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_url = request.build_absolute_uri(
                reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
            )
            subject = render_to_string('accounts/subject_activacion.txt').strip()
            message = render_to_string('accounts/email_activacion.txt', {
                'user': user,
                'activation_url': activation_url,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, '¡Registro exitoso! Revisa tu correo para activar tu cuenta.')
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
            if not user.is_active:
                messages.error(request, 'Tu cuenta no está activada. Revisa tu correo para activarla.')
                return render(request, 'accounts/login.html')
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.first_name or user.username or user.email}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas. Revisa tu correo/usuario y contraseña.')

    return render(request, 'accounts/login.html')

# Vista para activar cuenta
from django.views import View

class ActivarCuentaView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, '¡Cuenta activada! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'El enlace de activación no es válido o ha expirado.')
            return redirect('login')


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
