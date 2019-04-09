from django.test import TestCase
from .models import Alergia, PacienteTemAlergia
from paciente.models import Paciente
from django.utils import timezone
from random import randint, random, uniform
from rest_framework.test import APIRequestFactory
from .views import AlergiaViewSet
from django.urls import reverse
from rest_framework.test import APIClient
from .serializers import AlergiaSerializer


class AlergiaTest(TestCase):
    def setUp(self):
        alergias = []
        for i in range(3):
            a = Alergia.objects.create(**{
                'id': i+1,
                'principio_ativo': 'a' * 2,
                'descricao': 'b' * 2,
                'grau_risco': randint(1, 5)
            })
            alergias.append(a)

        cpfs = ['81653635061', '11928717071']
        for i in range(len(cpfs)):
            p = Paciente.objects.create(**{
                "cpf": cpfs[i],
                "nome_completo": "teste teste",
                "data_nascimento": "1980-01-01",
                "sexo": "m",
                "tipo_sanguineo": "A+"
            })
            PacienteTemAlergia.objects.create(**{
                'paciente': p,
                'alergia': alergias[i+1],
                'consulta_id': uniform(1, 10000)
            })
        p = Paciente.objects.create(**{
            "cpf": '52495749046',
            "nome_completo": "teste teste",
            "data_nascimento": "1980-01-01",
            "sexo": "m",
            "tipo_sanguineo": "A+"
        })
        self.client = APIClient()

    def testePost(self):
        a = {
            "principio_ativo": "awerkp",
            "descricao": "Alimentar",
            "grau_risco": 2
        }
        response = self.client.post(
            '/stagiop_bd/api/alergia', a, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['descricao'], a['descricao'])

    def testeList(self):
        response = self.client.get('/stagiop_bd/api/alergia')
        data = Alergia.objects.all()
        serializer = AlergiaSerializer(data, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def testeGet(self):
        response = self.client.get('/stagiop_bd/api/alergia/1')
        data = Alergia.objects.filter(id="1").first()
        serializer = AlergiaSerializer(data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def testePut(self):
        response = self.client.put(
            '/stagiop_bd/api/alergia/1', {
                "grau_risco": 5
            }, format='json')
        self.assertEqual(response.status_code, 201)

    def testeGet404(self):
        response = self.client.get('/stagiop_bd/api/alergia/98498194')
        self.assertEqual(response.status_code, 404)

    def testePostTemAlergia(self):
        pa = {
            "paciente": "52495749046",
            "alergia": 1,
            "consulta_id": 2
        }
        response = self.client.post(
            '/stagiop_bd/api/paciente-alergia', pa, format='json')
        self.assertEqual(response.status_code, 201)

    def testeGetTemAlergia(self):
        response = self.client.get(
            '/stagiop_bd/api/paciente-alergia/{}'.format('81653635061'))
        self.assertEqual(response.status_code, 200)
