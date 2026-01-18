from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar/', views.RecuperarContraseña.as_view(), name='password_reset'),
    path('recuperar/enviado/', views.RecuperarContraseña.as_view(), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', views.RecuperarContraseñaConfirm.as_view(), name='password_reset_confirm'),
    path('recuperar/completo/', views.RecuperarContraseñaComplete.as_view(), name='password_reset_complete'),
    path('activar/<uidb64>/<token>/', views.ActivarCuentaView.as_view(), name='activar_cuenta'),
]
