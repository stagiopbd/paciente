from rest_framework import serializers
from .models import Paciente
from copy import deepcopy


class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paciente
        exclude = ('data_nascimento',)
