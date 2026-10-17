from django.shortcuts import render, redirect
from nucleo.models import Colaborador


def home(req):
    busca = req.GET.get('q', '').strip()

    colaboradores = Colaborador.objects.all().order_by('nome')
    if busca:
        colaboradores = colaboradores.filter(nome__icontains=busca)

    return render(req, 'nucleo/index.html', {
        'colaboradores': colaboradores,
        'busca': busca,
    })


def tela_criar(req):
    return render(req, 'nucleo/forms/criar.html')


def salvar(req):
    nome = req.POST.get('nome')

    if nome is None:
        return redirect('nucleo-criar')

    telefone = req.POST.get('telefone')

    colaborador = Colaborador.objects.create(
        nome=nome,
        telefone=telefone
    )
    return redirect('nucleo-inicial')
