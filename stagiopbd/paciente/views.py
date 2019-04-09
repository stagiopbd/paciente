from rest_framework.views import APIView
from django.shortcuts import render
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Paciente
from .serializers import PacienteSerializer
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from copy import deepcopy
import numpy as np
from paciente.util import formatar_paciente_dict, formatar_paciente_model
from pycpfcnpj import cpfcnpj
import os


def index(request):
    url = os.getenv('URL', 'http://127.0.0.1:8000')
    return render(request, 'index.html', {'url': url})


def index_paciente(request):
    url = os.getenv('URL', 'http://127.0.0.1:8000')
    return render(request, 'paciente.index.html', {'url': url})


class PacienteViewSet(ModelViewSet):
    queryset = Paciente.objects
    serializer_class = PacienteSerializer

    def get_object(self):
        return get_object_or_404(Paciente, cpf=self.kwargs.get("pk"))

    # POST
    def create(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        serializer = self.serializer_class(data=data)
        try:
            if not serializer.initial_data.get('data_nascimento'):
                return Response({
                    'errors': "'data_nascimento' is required!"
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.initial_data['data_nascimento'] = datetime.strptime(
                serializer.initial_data['data_nascimento'], '%d/%m/%Y')
        except Exception:
            return Response({
                'errors': "Incorrect data format, should be DD/MM/YYYY"
            }, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            if not cpfcnpj.validate(data['cpf']):
                return Response({
                    'message': 'CPF Inválido!',
                    'errors': ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['inativo'] = None
            serializer.validated_data['data_nascimento'] = serializer.initial_data['data_nascimento']
            serializer.save()
            return Response(formatar_paciente_dict(serializer.validated_data), status=status.HTTP_201_CREATED)
        return Response({
            'errors': serializer.errors,
            'message': 'Preencha todos os campos corretamente!'
        }, status=status.HTTP_400_BAD_REQUEST)

    # GET ALL
    def list(self, request):
        data = self.queryset.all()
        result = []
        if data:
            for item in data:
                result.append(formatar_paciente_model(item))
        return Response(result, status.HTTP_200_OK)

    # GET POR ID
    def retrieve(self, request, *args, **kwargs):
        element = self.queryset.filter(cpf=kwargs.get("pk")).first()
        if element:
            return Response(formatar_paciente_model(element), status.HTTP_200_OK)
        return Response({"message": "Paciente não encontrado!"}, status.HTTP_404_NOT_FOUND)

    # PUT
    def update(self, request, *args, **kwargs):
        element = self.queryset.filter(cpf=kwargs.get("pk")).first()
        if element:
            serializer = self.serializer_class(
                element, data=request.data, partial=True)

            update_data_nascimento = serializer.initial_data.get(
                'data_nascimento')

            try:
                if update_data_nascimento:
                    serializer.initial_data['data_nascimento'] = datetime.strptime(
                        serializer.initial_data['data_nascimento'], '%d/%m/%Y')
            except Exception:
                return Response({
                    'errors': "Incorrect data format, should be DD/MM/YYYY"
                }, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                if update_data_nascimento:
                    serializer.validated_data['data_nascimento'] = serializer.initial_data['data_nascimento']

                serializer.save()

                data = deepcopy(serializer.data)
                if update_data_nascimento:
                    data['data_nascimento'] = serializer.initial_data['data_nascimento']
                else:
                    data['data_nascimento'] = element.data_nascimento

                return Response(formatar_paciente_dict(data), status=status.HTTP_201_CREATED)
            return Response({
                'errors': serializer.errors,
                'message': 'Preencha todos os campos corretamente!'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Paciente não encontrado!"}, status.HTTP_404_NOT_FOUND)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        element = self.queryset.filter(cpf=kwargs.get("pk")).first()
        if element:
            element.inativo = True
            element.save()
            return Response({
                'message': 'OK'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Paciente não encontrado!"}, status.HTTP_404_NOT_FOUND)
