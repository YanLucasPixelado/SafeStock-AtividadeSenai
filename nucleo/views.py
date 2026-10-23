from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

# Imprtação das Classes (Diferentes Entidades dentro do Sistema)
from nucleo.models import Colaborador
from nucleo.models import Epi
from nucleo.models import CategoriaEpi
from nucleo.models import Emprestimo

# Importação de Ferramentas Úteis que irã facilitar a minha vida
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime





# Refere-se a parte de Colaboradores
NOME_MAX = Colaborador._meta.get_field('nome').max_length
TELEFONE_MAX = Colaborador._meta.get_field('telefone').max_length

# Refere-se a parte de EPIs
NOME_MAX_EPI = Epi._meta.get_field('nome_epi').max_length
TAMANHO_MAX_EPI = Epi._meta.get_field('tamanho_epi').max_length

# TIPO_EPI removido porque Foreignkey não tem max_length
# TIPO_EPI = Epi._meta.get_field('categoria_epi').max_length



# Pages  e Views relacionadas ao Colaborador
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

# Pages e Views relacionadas aos Equipamentos 
# Validando se os campos de preenchidos estão dentro da conformidade
def validar_epi(nome_epi, categoria_id, tamanho_epi):
    """Retorna o texto do problema encontrado ou None se os dados estão ok."""
    vazios = []
    if not nome_epi:
        vazios.append('Nome')
    if not categoria_id:
        vazios.append('Categoria')
    if not tamanho_epi:
        vazios.append('Tamanho')
    if vazios:
        return 'Preencher o campo: ' + ', '.join(vazios)

    if len(nome_epi) > NOME_MAX_EPI:
        return f'O campo Nome aceita no máximo {NOME_MAX_EPI} caracteres'
    if not categoria_id.isdigit() or not CategoriaEpi.objects.filter(pk=categoria_id).exists():
        return f'Categoria Inválida'
    if len(tamanho_epi) > TAMANHO_MAX_EPI:
        return f'O campo Tamanho aceita no máximo {TAMANHO_MAX_EPI} caractere'
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
    # Pega a informação por via POST do campo que tem o nome "nome_epi" (Este campo está localizado la´dentro de seu arquivo HTML- '_campos-epi.html')
    nome_epi = req.POST.get('nome_epi', '').strip()
    
    # Pega a informação por via POST do campo que tem o nome "categoria_epi" (Este campo está localizado la´dentro de seu arquivo HTML- '_campos-epi.html')
    categoria_epi = req.POST.get('categoria_epi', '').strip()

    # Pega a informação por via POST do campo que tem o nome "tamanho_epi" (Este campo está localizado la´dentro de seu arquivo HTML- '_campos-epi.html')
    tamanho_epi = req.POST.get('tamanho_epi', '').strip()


    problema = validar_epi(nome_epi, categoria_epi, tamanho_epi)
    if problema:
        # Alterado de "Usuário" para "EPI"
        messages.error(req, f'EPI não foi cadastrado! {problema}')
        return render(req, 'nucleo/forms/criar-epi.html', {
            'nome_epi': nome_epi,
            'categoria_epi': categoria_epi,
            'tamanho_epi': tamanho_epi,
            'categorias': CategoriaEpi.objects.order_by('nome'),
        })

    Epi.objects.create(nome_epi=nome_epi, categoria_epi_id=categoria_epi, tamanho_epi=tamanho_epi)

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
        'tamanho_epi': epi.tamanho_epi,
        'categorias': CategoriaEpi.objects.order_by('nome'),
    })


# View da Tela de atualização de um EPI dentro do sistema
@require_POST
def atualizar_epi(req, id):
    epi = get_object_or_404(Epi, pk=id)

    nome_epi = req.POST.get('nome_epi', '').strip()

    categoria_epi = req.POST.get('categoria_epi', '').strip()

    tamanho_epi = req.POST.get('tamanho_epi', '').strip()

    problema = validar_epi(nome_epi, categoria_epi, tamanho_epi)
    if problema:
        messages.error(req, f'EPI não foi atualizado! {problema}')
        return render(req, 'nucleo/forms/editar-epi.html', {
            'epi': epi,
            'nome_epi': nome_epi,
            'categoria_epi': categoria_epi,
            'tamanho_epi': tamanho_epi,
            'categorias': CategoriaEpi.objects.order_by('nome'),
        })

    epi.nome_epi = nome_epi
    epi.categoria_epi_id = categoria_epi
    epi.tamanho_epi = tamanho_epi
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


# ======================================================================

# Pages e Views relacionadas a "Empréstimos"
def validar_emprestimo(colaborador_id, epi_id, data_prevista, status, condicoes):
    vazios = []
    if not colaborador_id:
        vazios.append('Colaborador')

    #if not usuario_id:
     #   vazios.append('Usuario')

    if not epi_id:
        vazios.append('Equipamento')
    if not data_prevista:
        vazios.append('Data prevista da devolução')
    if not status:
        vazios.append('Status')
    if not condicoes:
        vazios.append('Condições do Equipamento')
    if vazios:
        return 'Preencher o campo: ' + ', '.join(vazios)

    if status not in ('FOR', 'EMP'):
        return 'Status Inválido'
    
    if not colaborador_id.isdigit() or not Colaborador.objects.filter(pk=colaborador_id).exists():
        return f'Colaborador Inválido'

    if not epi_id.isdigit() or not Epi.objects.filter(pk=epi_id).exists():
        return f'Equipamento Inválido'
    
    if data_prevista <= timezone.now():
        return 'A data prevista de devolução deve ser superior à data atual e hora atuais'
    return None


def emprestimos_home(req):
    busca = req.GET.get('q', '').strip()
    emprestimos = Emprestimo.objects.select_related('colaborador', 'epi')

    if busca:
        emprestimos = emprestimos.filter(Q(epi__nome_epi__icontains=busca) | Q(colaborador__nome__icontains=busca))

    return render(req, 'nucleo/index-emprestimo.html', {
        'emprestimos': emprestimos,
        'busca': busca,
    })


def tela_criar_emprestimo(req):
    return render(req, 'nucleo/forms/criar-emprestimo.html', contexto_emprestimo({
        'colaboradores': Colaborador.objects.order_by('nome'),
        'epis': Epi.objects.order_by('nome_epi'),
        'status_opcoes': Emprestimo.Status.choices, 
        'categorias': CategoriaEpi.objects.order_by('nome',)
    }))

def contexto_emprestimo(extra=None):
    contexto = {
        'colaboradores': Colaborador.objects.order_by('nome'),
        'epis': Epi.objects.order_by('nome_epi'),
        'agora': timezone.localtime().strftime('%Y-%m-%dT%H:%M'),
    }
    if extra:
        contexto.update(extra)
    return contexto

# View de Salvamento de um EPI 
@require_POST
def salvar_emprestimo(req):
    # Pega a informação por via POST do campo que tem o nome "nome_epi" (Este campo está localizado la´dentro de seu arquivo HTML- '_campos-epi.html')
    colaborador_id = req.POST.get('colaborador', '').strip("'\"")
    
    # Pega a informação por via POST do campo que tem o nome "categoria_epi" (Este campo está localizado la´dentro de seu arquivo HTML- '_campos-epi.html')
    #usuario_id = req.POST.get('usuario_id', '').strip()

    # Pega a informação por via POST do campo que tem o nome "tamanho_epi" (Este campo está localizado la´dentro de seu arquivo HTML- '_campos-epi.html')
    epi_id = req.POST.get('epi', '').strip()

    status = req.POST.get('status', '').strip()

    condicoes = req.POST.get('condicoes', '').strip()

    # Parte da data_prevista de devolução do Equipamento
    bruto = req.POST.get('data_prevista_devolucao', '').strip()
    data_prevista = parse_datetime(bruto) if bruto else None
    if data_prevista and timezone.is_naive(data_prevista):
        data_prevista = timezone.make_aware(data_prevista)


    #status = req.POST.get('status', '').strip()

    #data_emprestimo = req.POST.get('data_emprestimo', '').strip()

    #observacao = req.POST.get('observacao', '').strip()


    problema = validar_emprestimo(colaborador_id, epi_id, data_prevista, status, condicoes)
    if problema:
        # Alterado de "Usuário" para "EPI"
        messages.error(req, f'Emprestimo não foi cadastrado! {problema}')
        return render(req, 'nucleo/forms/criar-emprestimo.html', contexto_emprestimo({
            'epi_id': epi_id,
            'colaborador_id': colaborador_id,
            'data_prevista_devolucao': bruto,
            'status': status,
            'condicoes': condicoes,
        }))


    Emprestimo.objects.create(
        colaborador_id=colaborador_id,
        epi_id=epi_id, data_prevista_devolucao=data_prevista, status=status,
        condicoes=condicoes,
        )

    # Alterado de "Usuário" para "EPI"
    messages.success(req, 'Emprestimo cadastrado com sucesso!')
    return redirect('nucleo-criar-emprestimo')

    