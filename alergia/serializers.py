from rest_framework import serializers
from .models import Alergia, PacienteTemAlergia


class AlergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergia
        fields = '__all__'


class PacienteTemAlergiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteTemAlergia
        fields = '__all__'
