from rest_framework.views import APIView
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Alergia, PacienteTemAlergia
from .serializers import AlergiaSerializer, PacienteTemAlergiaSerializer
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from copy import deepcopy
import numpy as np
import os


def index_alergia(request):
    url = os.getenv('URL', 'http://127.0.0.1:8000')
    return render(request, 'alergia.index.html', {'url': url})


class AlergiaViewSet(ModelViewSet):
    queryset = Alergia.objects
    serializer_class = AlergiaSerializer

    def get_object(self):
        return get_object_or_404(Alergia, id=self.kwargs.get("pk"))

    # POST
    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'errors': serializer.errors,
            'message': 'Preencha todos os campos corretamente!'
        }, status=status.HTTP_400_BAD_REQUEST)

    # GET ALL
    def list(self, request):
        return Response(self.get_serializer_class()(self.queryset.all(), many=True).data, status.HTTP_200_OK)

    # GET POR ID
    def retrieve(self, request, *args, **kwargs):
        elements = self.queryset.filter(id=kwargs.get("pk")).first()
        if elements:
            return Response(self.get_serializer_class()(elements).data, status.HTTP_200_OK)
        return Response({"message": "Alergia não encontrada!"}, status.HTTP_404_NOT_FOUND)

    # PUT
    def update(self, request, *args, **kwargs):
        element = self.queryset.filter(id=kwargs.get("pk")).first()
        if element:
            serializer = self.serializer_class(
                element, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({
                'errors': serializer.errors,
                'message': 'Preencha todos os campos corretamente!'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Alergia não encontrada!"}, status.HTTP_404_NOT_FOUND)


class PacienteTemAlergiaViewSet(ModelViewSet):
    queryset = PacienteTemAlergia.objects
    serializer_class = PacienteTemAlergiaSerializer

    def get_object(self):
        return get_object_or_404(PacienteTemAlergia, id=self.kwargs.get("pk"))

    # POST
    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'errors': serializer.errors,
            'message': 'Preencha todos os campos corretamente!'
        }, status=status.HTTP_400_BAD_REQUEST)

    # GET POR CPF
    def retrieve(self, request, *args, **kwargs):
        elements = self.queryset.filter(paciente_id=kwargs.get("pk")).all()
        if elements:
            result = []
            for item in elements:
                new_item = {
                    'cpf': item.paciente_id,
                    'nome_completo': item.paciente.nome_completo,
                    'alergia_principio_ativo': item.alergia.principio_ativo,
                    'alergia_descricao': item.alergia.descricao,
                    'alergia_grau_risco': item.alergia.grau_risco,
                    'consulta_id': item.consulta_id
                }
                result.append(new_item)
            return Response(result, status.HTTP_200_OK)
        return Response({"message": "Paciente {} não possui alergias!".format(kwargs.get("pk"))}, status.HTTP_404_NOT_FOUND)
