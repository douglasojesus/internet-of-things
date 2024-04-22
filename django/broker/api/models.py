from django.db import models

# Create your models here.
class Dispositivo(models.Model):
    tipo_medicao = models.CharField(max_length=30)
    medicao_atual = models.FloatField(null=True, blank=True)
    esta_ativo = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Dispositivo: " + str(self.id) + " - Tipo de Medição: " + self.tipo_medicao + " - Medição atual: " + str(self.medicao_atual)

