from django.test import Client, TestCase
from django.urls import reverse
from busca import views
from django.contrib.auth import login
from django.contrib.auth.models import User
import os

class TestBusca(TestCase):
    # Método Para logar um Usuário
    def setUp(self) -> None:
        self.client = Client()
        self.clientLogado = Client()
       
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        logged_in = self.clientLogado.login(username='testuser', password='12345')

    # Método para verificar se o usuário não logado foi redirecionado
    def test_GET(self):
        response = self.client.get('/busca', follow= True) 
        self.assertRedirects(response, '/entrar')
    
    # Método para verificar se o usuário está logado foi redirecionado para a mesma pagina 
    def test_GET_logado(self):        
        response = self.clientLogado.get('/busca')

        self.assertEquals(response.status_code, 200)
        path = os.path.join('..', 'templates', 'busca.html')

        self.assertTemplateUsed(response, path) 
    
    # Método para teste De uma Busca simples na hashTable
    def test_POST_buscar(self):
        response = self.clientLogado.post('/busca', data={'busca': 'cielo'}, format='json')

        self.assertEqual(response.status_code, 200)
        
    # Método para verificar se o cicero é gay kkkkkkkkk
    def test_POST_adicionar(self):
        response = self.clientLogado.post('/busca', data={
                        'adicionar': True,
                        'symbol': 'CIEL3',
                        'name': 'Cielo',
                        'region': 'Br',
                        'currency': 'brl',
                        'open': '3:00',
                        'close': '4:00',
                        'timezone': -3,
                        'market_cap': 3921.2,
                        'price': 32.1,
                        'change_percent': 12.1,
                        'updated_at': '12/01/2020'}, format='json')
                        
        self.assertEqual(response.status_code, 200)
    
    #Método para verificar se uma acao foi desfeita
    def test_POST_desfazer(self):
        response = self.clientLogado.post('/busca', data={
                        'adicionar': True,
                        'symbol': 'CIEL3',
                        'name': 'Cielo',
                        'region': 'Br',
                        'currency': 'brl',
                        'open': '3:00',
                        'close': '4:00',
                        'timezone': -3,
                        'market_cap': 3921.2,
                        'price': 32.1,
                        'change_percent': 12.1,
                        'updated_at': '12/01/2020'}, format='json')
                        
        response = self.clientLogado.post('/busca', data={'desfazer': True}, format='json')

        self.assertEqual(response.status_code, 200)
        