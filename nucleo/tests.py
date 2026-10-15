from django.test import TestCase
from django.urls import reverse

from nucleo.models import Colaborador


class ColaboradorCrudTests(TestCase):
    def test_listagem_vazia_mostra_mensagem(self):
        r = self.client.get(reverse('nucleo-inicial'))
        self.assertContains(r, 'não encontramos dados')

    def test_pesquisa_por_nome(self):
        Colaborador.objects.create(nome='Maria Souza', telefone='1')
        Colaborador.objects.create(nome='José Lima', telefone='2')
        r = self.client.get(reverse('nucleo-inicial'), {'q': 'mari'})
        self.assertContains(r, 'Maria Souza')
        self.assertNotContains(r, 'José Lima')

    def test_cadastro_permanece_na_tela_e_mostra_sucesso(self):
        r = self.client.post(reverse('nucleo-salvar'),
                             {'nome': 'Ana', 'telefone': '7199999'}, follow=True)
        self.assertRedirects(r, reverse('nucleo-criar'))
        self.assertContains(r, 'Usuário cadastrado com sucesso!')
        self.assertEqual(Colaborador.objects.count(), 1)

    def test_cadastro_invalido_mostra_falha_e_nao_grava(self):
        r = self.client.post(reverse('nucleo-salvar'), {'nome': '', 'telefone': ''})
        self.assertContains(r, 'Usuário não foi cadastrado! Preencher o campo: Nome, Telefone')
        self.assertEqual(Colaborador.objects.count(), 0)

    def test_cadastro_nome_longo_nao_grava(self):
        r = self.client.post(reverse('nucleo-salvar'),
                             {'nome': 'a' * 31, 'telefone': '1'})
        self.assertContains(r, 'no máximo 30')
        self.assertEqual(Colaborador.objects.count(), 0)

    def test_tela_editar_vem_preenchida(self):
        c = Colaborador.objects.create(nome='Ana', telefone='123')
        r = self.client.get(reverse('nucleo-editar', args=[c.id]))
        self.assertContains(r, 'value="Ana"')
        self.assertContains(r, 'value="123"')

    def test_atualizar(self):
        c = Colaborador.objects.create(nome='Ana', telefone='123')
        r = self.client.post(reverse('nucleo-atualizar', args=[c.id]),
                             {'nome': 'Ana Paula', 'telefone': '456'}, follow=True)
        self.assertContains(r, 'Usuário atualizado com sucesso!')
        c.refresh_from_db()
        self.assertEqual((c.nome, c.telefone), ('Ana Paula', '456'))

    def test_atualizar_invalido_nao_altera(self):
        c = Colaborador.objects.create(nome='Ana', telefone='123')
        r = self.client.post(reverse('nucleo-atualizar', args=[c.id]),
                             {'nome': '', 'telefone': '456'})
        self.assertContains(r, 'Usuário não foi atualizado! Preencher o campo: Nome')
        c.refresh_from_db()
        self.assertEqual(c.nome, 'Ana')

    def test_excluir_somente_por_post(self):
        c = Colaborador.objects.create(nome='Ana', telefone='123')
        self.assertEqual(self.client.get(reverse('nucleo-excluir', args=[c.id])).status_code, 405)
        self.assertEqual(Colaborador.objects.count(), 1)
        r = self.client.post(reverse('nucleo-excluir', args=[c.id]), follow=True)
        self.assertContains(r, 'Usuário removido com sucesso!')
        self.assertEqual(Colaborador.objects.count(), 0)

    def test_editar_inexistente_da_404(self):
        self.assertEqual(self.client.get(reverse('nucleo-editar', args=[999])).status_code, 404)
