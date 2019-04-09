from django.test import TestCase
from .models import QuadroClinico
from paciente.models import Paciente
from django.utils import timezone
from random import randint, random, uniform
from rest_framework.test import APIRequestFactory
from .views import QuadroClinicoViewSet
from django.urls import reverse
from rest_framework.test import APIClient
from .serializers import QuadroClinicoSerializer
from .utils import calc_imc


class QuadroClinicoTest(TestCase):
    def setUp(self):
        cpfs = ['111111111', '222222222']
        for i in range(len(cpfs)):
            p = Paciente.objects.create(**{
                "cpf": cpfs[i],
                "nome_completo": "teste teste",
                "data_nascimento": "1980-01-01",
                "sexo": "m",
                "tipo_sanguineo": "A+"
            })
            QuadroClinico.objects.create(**{
                "paciente": p,
                "peso": uniform(20, 500),
                "altura": uniform(0.5, 3),
                "fuma": False,
                "bebe": False,
                "pratica_atividade": False
            })
        p = Paciente.objects.create(**{
            "cpf": '333333333',
            "nome_completo": "teste teste",
            "data_nascimento": "1980-01-01",
            "sexo": "m",
            "tipo_sanguineo": "A+"
        })
        self.client = APIClient()

    def testePost(self):
        qc = {
            "paciente": '333333333',
            "peso": uniform(20, 500),
            "altura": uniform(0.5, 3),
            "fuma": False,
            "bebe": False,
            "pratica_atividade": False
        }
        response = self.client.post(
            '/stagiop_bd/api/quadro_clinico', qc, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['paciente'], qc['paciente'])

    def testeList(self):
        response = self.client.get('/stagiop_bd/api/quadro_clinico')
        data = QuadroClinico.objects.all()
        serializer = QuadroClinicoSerializer(data, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def testeGet(self):
        response = self.client.get('/stagiop_bd/api/quadro_clinico/222222222')
        data = QuadroClinico.objects.filter(paciente_id="222222222").first()
        serializer = QuadroClinicoSerializer(data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def testePut(self):
        response = self.client.put(
            '/stagiop_bd/api/quadro_clinico/222222222', {
                "fuma": True,
                "fuma_frequencia": "sempre"
            }, format='json')
        self.assertEqual(response.status_code, 201)

    def testePut404(self):
        response = self.client.put(
            '/stagiop_bd/api/quadro_clinico/98498194', {
                "fuma": True,
                "fuma_frequencia": "todo_dia"
            }, format='json')
        self.assertEqual(response.status_code, 404)

    def testeImc(self):
        imc = calc_imc(78, 1.65)
        self.assertEqual(imc, 'Levemente acima do peso')
