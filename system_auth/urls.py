# Importação do módulo para rotas/caminhos
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='auth-login'),
    path('logout/', views.logout_view, name='auth-logout'),
]
