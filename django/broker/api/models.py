from django.db import models

# Create your models here.
class Dispositivo(models.Model):
    medicao = models.CharField(max_length=30)
    temp_atual = models.FloatField()

    def __str__(self) -> str:
        return "Dispositivo: " + str(self.id) + " - Tipo de Medição: " + self.medicao + " - Medição atual: " + str(self.temp_atual)

