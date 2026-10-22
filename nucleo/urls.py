"""
URL configuration for epi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    # URLs relaciondas a parte de Colaboradores
    path('', views.home, name='nucleo-inicial'),
    path('criar', views.tela_criar, name='nucleo-criar'),
    path('salvar', views.salvar, name='nucleo-salvar'),
    path('editar/<int:id>', views.tela_editar, name='nucleo-editar'),
    path('atualizar/<int:id>', views.atualizar, name='nucleo-atualizar'),
    path('excluir/<int:id>', views.excluir, name='nucleo-excluir'),

    # URLs relacionadas a parte de Equipamentos 
    path('epi-home', views.equipamentos_home, name='nucleo-epis-home'),
    path('criar-epi', views.tela_criar_epi, name='nucleo-criar-epi'),
    path('salvar-epi', views.salvar_epi, name='nucleo-salvar-epi'),
    path('editar-epi/<int:id>', views.tela_editar_epi, name='nucleo-editar-epi'),
    path('atualizar-epi/<int:id>', views.atualizar_epi, name='nucleo-atualizar-epi'),
    path('excluir-epi/<int:id>', views.excluir_epi, name='nucleo-excluir-epi'),
]
