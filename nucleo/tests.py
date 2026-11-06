from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from nucleo.models import CategoriaEpi, Colaborador, Emprestimo, Epi

from django.contrib.auth import get_user_model


class EmprestimoTests(TestCase):
    def setUp(self):
        usuario = get_user_model().objects.create_user('teste', password='senha-de-teste-123')
        self.client.force_login(usuario)
        cat = CategoriaEpi.objects.create(nome='Cabeça')
        self.ana = Colaborador.objects.create(nome='Ana', telefone='1')
        self.bia = Colaborador.objects.create(nome='Bia', telefone='2')
        self.capacete = Epi.objects.create(nome_epi='Capacete', tamanho_epi='M', categoria_epi=cat)
        self.luva = Epi.objects.create(nome_epi='Luva', tamanho_epi='G', categoria_epi=cat)
        prevista = timezone.now() + timedelta(days=1)
        self.e1 = Emprestimo.objects.create(colaborador=self.ana, epi=self.capacete, status='EMP',
                                            data_prevista_devolucao=prevista, condicoes='ok')
        self.e2 = Emprestimo.objects.create(colaborador=self.ana, epi=self.luva, status='DEV',
                                            data_prevista_devolucao=prevista, condicoes='ok')
        self.e3 = Emprestimo.objects.create(colaborador=self.bia, epi=self.capacete, status='EMP',
                                            data_prevista_devolucao=prevista, condicoes='ok')

    def test_criar_emprestimo(self):
        futuro = (timezone.localtime() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        r = self.client.post(reverse('nucleo-salvar-emprestimo'), {
            'colaborador': self.bia.id, 'epi': self.luva.id, 'status': 'EMP',
            'data_prevista_devolucao': futuro, 'condicoes': 'novo'})
        self.assertRedirects(r, reverse('nucleo-criar-emprestimo'))
        self.assertEqual(Emprestimo.objects.count(), 4)

    def test_criar_rejeita_data_passada_e_status_devolvido(self):
        passado = (timezone.localtime() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        r = self.client.post(reverse('nucleo-salvar-emprestimo'), {
            'colaborador': self.bia.id, 'epi': self.luva.id, 'status': 'EMP',
            'data_prevista_devolucao': passado, 'condicoes': 'x'})
        self.assertEqual(r.status_code, 200)
        r = self.client.post(reverse('nucleo-salvar-emprestimo'), {
            'colaborador': self.bia.id, 'epi': self.luva.id, 'status': 'DEV',
            'data_prevista_devolucao': '2999-01-01T10:00', 'condicoes': 'x'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Emprestimo.objects.count(), 3)

    def test_filtros_and(self):
        url = reverse('nucleo-emprestimos-home')
        r = self.client.get(url, {'colaborador': 'ana', 'status': 'EMP'})
        self.assertEqual(list(r.context['emprestimos']), [self.e1])
        r = self.client.get(url, {'colaborador': 'ana', 'equipamento': 'luva', 'status': 'EMP'})
        self.assertEqual(list(r.context['emprestimos']), [])
        r = self.client.get(url, {'equipamento': 'capacete'})
        self.assertEqual(set(r.context['emprestimos']), {self.e1, self.e3})

    def test_editar_devolvido(self):
        r = self.client.get(reverse('nucleo-editar-emprestimo', args=[self.e1.id]))
        self.assertContains(r, 'disabled')
        self.e1.data_emprestimo = timezone.now() - timedelta(hours=2)
        self.e1.save()
        agora = timezone.localtime().strftime('%Y-%m-%dT%H:%M')
        r = self.client.post(reverse('nucleo-atualizar-emprestimo', args=[self.e1.id]), {
            'status': 'DAN', 'data_devolucao': agora, 'observacao_devolucao': 'rachado',
            'condicoes': 'ok', 'colaborador': self.bia.id, 'epi': self.luva.id})
        self.assertRedirects(r, reverse('nucleo-emprestimos-home'))
        self.e1.refresh_from_db()
        self.assertEqual(self.e1.status, 'DAN')
        self.assertEqual(self.e1.observacao_devolucao, 'rachado')
        self.assertIsNotNone(self.e1.data_devolucao)
        # campos bloqueados não mudam mesmo se enviados
        self.assertEqual(self.e1.colaborador, self.ana)
        self.assertEqual(self.e1.epi, self.capacete)

    def test_editar_exige_data_devolucao(self):
        r = self.client.post(reverse('nucleo-atualizar-emprestimo', args=[self.e1.id]), {
            'status': 'DEV', 'condicoes': 'ok'})
        self.assertEqual(r.status_code, 200)
        self.e1.refresh_from_db()
        self.assertEqual(self.e1.status, 'EMP')
