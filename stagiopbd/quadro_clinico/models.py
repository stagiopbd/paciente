from django.db import models
from paciente.models import Paciente


class QuadroClinico(models.Model):
    FREQUENCIAS = (
        ("nunca", "nunca"),
        ("raramente", "raramente"),
        ("normalmente", "normalmente"),
        ("frequentemente", "frequentemente"),
        ("sempre", "sempre")
    )
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    peso = models.FloatField()
    altura = models.FloatField()
    imc = models.CharField(max_length=120, blank=True, null=True)
    fuma = models.BooleanField()
    fuma_frequencia = models.CharField(
        max_length=120, blank=True, null=True, choices=FREQUENCIAS)
    bebe = models.BooleanField()
    bebe_frequencia = models.CharField(
        max_length=120, blank=True, null=True, choices=FREQUENCIAS)
    pratica_atividade = models.BooleanField()
    pratica_frequencia = models.CharField(
        max_length=120, blank=True, null=True, choices=FREQUENCIAS)

    class Meta:
        db_table = "quadro_clinico"
