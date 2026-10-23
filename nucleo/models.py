from django.db import models
from django.utils import timezone

class Colaborador(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    telefone = models.CharField(max_length=30)

    def __str__(self):
        return self.nome

class Epi(models.Model):
    nome_epi = models.CharField(max_length=30, null=False, blank=False)
    tamanho_epi = models.CharField(max_length=30, null=False, blank=False)
    categoria_epi = models.ForeignKey("nucleo.CategoriaEpi", verbose_name='Categoria_Epi', on_delete=models.CASCADE, null=False)
    
    def __str__(self):
            return self.nome_epi

class CategoriaEpi(models.Model):
    nome = models.CharField(max_length=30, null=False, blank=False)
    # Depois implementar o campo [descricao] aqui, 
    # pois é o que remete a tabela em sua totalidade

    def __str__(self):
                return self.nome


class Emprestimo(models.Model):
    class Status(models.TextChoices):
        EMPRESTADO = 'EMP', 'Emprestado',
        FORNECIDO = 'FOR', 'Fornecido',
        DEVOLVIDO = 'DEV', 'Devolvido',
        DANIFICADO = 'DAN', 'Danificado',
        PERDIDO = 'PER', 'Perdido'
    
    status = models.CharField(
        'Emprestado',  # Correção do rótulo (verbose_name)
        max_length=3,
        choices=Status.choices,  # Vinculação das opções
        default=Status.EMPRESTADO,
    )

    # Campos da própria tabela (Sem precisar de chave estrangeira)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_prevista_devolucao = models.DateTimeField(null=False, blank=False)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, null=False, blank=False)
    observacao_devolucao = models.CharField(max_length=30, null=False, blank=False)
    condicoes = models.CharField(max_length=200)

    # Campos que necessitaram de uma chave estrangeira
    colaborador = models.ForeignKey("nucleo.Colaborador", verbose_name='Colaborador', on_delete=models.PROTECT, null=False)

    epi = models.ForeignKey("nucleo.Epi", verbose_name='Usuario', on_delete=models.PROTECT, null=False)
