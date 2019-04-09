from django.db import models
from paciente.models import Paciente


class Alergia(models.Model):
    principio_ativo = models.CharField(max_length=120)
    descricao = models.CharField(max_length=120)
    grau_risco = models.IntegerField()

    class Meta:
        db_table = "alergia"


class PacienteTemAlergia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    alergia = models.ForeignKey(Alergia, on_delete=models.CASCADE)
    consulta_id = models.IntegerField()

    class Meta:
        db_table = "paciente_tem_alergia"
