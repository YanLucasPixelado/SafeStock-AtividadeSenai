from django.db import models

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
    