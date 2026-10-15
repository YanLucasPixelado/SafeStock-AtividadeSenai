from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from nucleo.models import Colaborador

NOME_MAX = Colaborador._meta.get_field('nome').max_length
TELEFONE_MAX = Colaborador._meta.get_field('telefone').max_length


def validar(nome, telefone):
    """Retorna o texto do problema encontrado ou None se os dados estão ok."""
    vazios = []
    if not nome:
        vazios.append('Nome')
    if not telefone:
        vazios.append('Telefone')
    if vazios:
        return 'Preencher o campo: ' + ', '.join(vazios)

    if len(nome) > NOME_MAX:
        return f'O campo Nome aceita no máximo {NOME_MAX} caracteres'
    if len(telefone) > TELEFONE_MAX:
        return f'O campo Telefone aceita no máximo {TELEFONE_MAX} caracteres'
    return None


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


@require_POST
def salvar(req):
    nome = req.POST.get('nome', '').strip()
    telefone = req.POST.get('telefone', '').strip()

    problema = validar(nome, telefone)
    if problema:
        messages.error(req, f'Usuário não foi cadastrado! {problema}')
        # Permanece na tela de cadastro, mantendo o que foi digitado
        return render(req, 'nucleo/forms/criar.html', {
            'nome': nome,
            'telefone': telefone,
        })

    Colaborador.objects.create(nome=nome, telefone=telefone)
    messages.success(req, 'Usuário cadastrado com sucesso!')
    # Após cadastrar, o sistema permanece na tela de cadastro
    return redirect('nucleo-criar')
