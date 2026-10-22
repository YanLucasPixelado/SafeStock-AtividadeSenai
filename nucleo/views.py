from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

# Imprtação das Classes (Diferentes Entidades dentro do Sistema)
from nucleo.models import Colaborador
from nucleo.models import Epi
from nucleo.models import CategoriaEpi

# Refere-se a parte de Colaboradores
NOME_MAX = Colaborador._meta.get_field('nome').max_length
TELEFONE_MAX = Colaborador._meta.get_field('telefone').max_length

# Refere-se a parte de EPIs
NOME_MAX_EPI = Epi._meta.get_field('nome_epi').max_length

# TIPO_EPI removido porque Foreignkey não tem max_length
# TIPO_EPI = Epi._meta.get_field('categoria_epi').max_length



# Parte que remete as tela da funcionalidade "colaborador" (O mesmo se encontra no lado esquerda da home principal)
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


def tela_editar(req, id):
    colaborador = get_object_or_404(Colaborador, pk=id)
    return render(req, 'nucleo/forms/editar.html', {
        'colaborador': colaborador,
        'nome': colaborador.nome,
        'telefone': colaborador.telefone,
    })


@require_POST
def atualizar(req, id):
    colaborador = get_object_or_404(Colaborador, pk=id)

    nome = req.POST.get('nome', '').strip()
    telefone = req.POST.get('telefone', '').strip()

    problema = validar(nome, telefone)
    if problema:
        messages.error(req, f'Usuário não foi atualizado! {problema}')
        return render(req, 'nucleo/forms/editar.html', {
            'colaborador': colaborador,
            'nome': nome,
            'telefone': telefone,
        })

    colaborador.nome = nome
    colaborador.telefone = telefone
    colaborador.save()
    messages.success(req, 'Usuário atualizado com sucesso!')
    return redirect('nucleo-inicial')


@require_POST
def excluir(req, id):
    colaborador = get_object_or_404(Colaborador, pk=id)
    colaborador.delete()
    messages.success(req, 'Usuário removido com sucesso!')
    return redirect('nucleo-inicial')
# Final da parte que remete ao Colaborador

# ======================================================================

# Começo da parte das telas que remetem aos Equipamentos (EPI) e Controle de EPI
# Validando se os campos de preenchidos estão dentro da conformidade
def validar_epi(nome_epi, categoria_id):
    """Retorna o texto do problema encontrado ou None se os dados estão ok."""
    vazios = []
    if not nome_epi:
        vazios.append('Nome')
    if not categoria_id:
        vazios.append('Categoria')
    if vazios:
        return 'Preencher o campo: ' + ', '.join(vazios)

    if len(nome_epi) > NOME_MAX_EPI:
        return f'O campo Nome aceita no máximo {NOME_MAX_EPI} caracteres'
    if not categoria_id.isdigit() or not CategoriaEpi.objects.filter(pk=categoria_id).exists():
        return f'Categoria Inválida'
    return None

# View da Home da Tela de EPI
def equipamentos_home(req):
    busca = req.GET.get('q', '').strip()
    epis = Epi.objects.all().order_by('nome_epi')

    if busca:
        epis = epis.filter(nome_epi__icontains=busca)

    return render(req, 'nucleo/index-epi.html', {
        'epis': epis,
        'busca': busca,
    })


# View de Criação de Tela de EPI
def tela_criar_epi(req):
    return render(req, 'nucleo/forms/criar-epi.html', {
        'categorias': CategoriaEpi.objects.order_by('nome',)
    })


# View de Salvamento de um EPI 
@require_POST
def salvar_epi(req):
    nome_epi = req.POST.get('nome_epi', '').strip()
    categoria_epi = req.POST.get('categoria_epi', '').strip()

    problema = validar_epi(nome_epi, categoria_epi)
    if problema:
        # Alterado de "Usuário" para "EPI"
        messages.error(req, f'EPI não foi cadastrado! {problema}')
        return render(req, 'nucleo/forms/criar-epi.html', {
            'nome_epi': nome_epi,
            'categoria_epi': categoria_epi,
            'categorias': CategoriaEpi.objects.order_by('nome'),
        })

    Epi.objects.create(nome_epi=nome_epi, categoria_epi_id=categoria_epi)
    # Alterado de "Usuário" para "EPI"
    messages.success(req, 'EPI cadastrado com sucesso!')
    return redirect('nucleo-criar-epi')


# View da Tela de edição de um EPI dentro do sistema
def tela_editar_epi(req, id):
    epi = get_object_or_404(Epi, pk=id)
    return render(req, 'nucleo/forms/editar-epi.html', {
        'epi': epi,
        'nome_epi': epi.nome_epi,
        'categoria_epi': str(epi.categoria_epi_id),
        'categorias': CategoriaEpi.objects.order_by('nome'),
    })


# View da Tela de atualização de um EPI dentro do sistema
@require_POST
def atualizar_epi(req, id):
    epi = get_object_or_404(Epi, pk=id)

    nome_epi = req.POST.get('nome_epi', '').strip()
    categoria_epi = req.POST.get('categoria_epi', '').strip()

    problema = validar_epi(nome_epi, categoria_epi)
    if problema:
        messages.error(req, f'Usuário não foi atualizado! {problema}')
        return render(req, 'nucleo/forms/editar-epi.html', {
            'epi': epi,
            'nome_epi': nome_epi,
            'categoria_epi': categoria_epi,
            'categorias': CategoriaEpi.objects.order_by('nome'),
        })

    epi.nome_epi = nome_epi
    epi.categoria_epi_id = categoria_epi
    epi.save()
    messages.success(req, 'Equipamento atualizado com sucesso!')
    return redirect('nucleo-epis-home')

# View da Tela de exclusão de um EPI dentro do sistema
@require_POST
def excluir_epi(req, id):
    epi = get_object_or_404(Epi, pk=id)
    epi.delete()
    messages.success(req, 'Equipamento removido com sucesso!')
    return redirect('nucleo-epis-home')
