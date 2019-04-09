from django.test import TestCase
from django.utils import timezone
from random import randint, random, uniform
from rest_framework.test import APIRequestFactory
from .views import PacienteViewSet
from django.urls import reverse
from rest_framework.test import APIClient
from .serializers import PacienteSerializer
from .models import Paciente


class PacienteTest(TestCase):
    def setUp(self):
        cpfs = ['81653635061', '11928717071']
        for i in range(len(cpfs)):
            Paciente.objects.create(**{
                "cpf": cpfs[i],
                "nome_completo": "teste teste",
                "data_nascimento": "1980-01-01",
                "sexo": "M",
                "tipo_sanguineo": "A+"
            })
        self.client = APIClient()

    def testePost(self):
        p = {
            "cpf": '52495749046',
            "nome_completo": "teste teste",
            "data_nascimento": "01/01/1980",
            "sexo": "M",
            "tipo_sanguineo": "A+"
        }
        response = self.client.post(
            '/stagiop_bd/api/paciente', p, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['cpf'], p['cpf'])

    def testeList(self):
        response = self.client.get('/stagiop_bd/api/paciente')
        data = Paciente.objects.all()
        serializer = PacienteSerializer(data, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, 200)

    def testeGet(self):
        response = self.client.get('/stagiop_bd/api/paciente/11928717071')
        data = Paciente.objects.filter(cpf="11928717071").first()
        serializer = PacienteSerializer(data)
        self.assertEqual(response.data['cpf'], serializer.data['cpf'])
        self.assertEqual(response.status_code, 200)

    def testePut(self):
        response = self.client.put(
            '/stagiop_bd/api/paciente/11928717071', {
                "nome_completo": "teste put"
            }, format='json')
        self.assertEqual(response.status_code, 201)

    def testeCpfInvalido(self):
        p = {
            "cpf": '111111111',
            "nome_completo": "teste teste",
            "data_nascimento": "01/01/1980",
            "sexo": "M",
            "tipo_sanguineo": "A+"
        }
        response = self.client.post(
            '/stagiop_bd/api/paciente', p, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "CPF Inválido!")
