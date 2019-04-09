from rest_framework import serializers
from .models import QuadroClinico


class QuadroClinicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuadroClinico
        fields = '__all__'

    def check_exists(self, data, father_field, children_field):
        if data.get(father_field) and not data.get(children_field):
            raise serializers.ValidationError(
                "Field {} is required".format(children_field))

    def validate(self, data):
        self.check_exists(data, 'fuma', 'fuma_frequencia')
        self.check_exists(data, 'bebe', 'bebe_frequencia')
        self.check_exists(data, 'pratica_atividade', 'pratica_frequencia')
        return data
