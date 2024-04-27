from django.db import models

# Create your models here.
class Dispositivo(models.Model):
    tipo_medicao = models.CharField(max_length=30)
    medicao_atual = models.FloatField(null=True, blank=True)
    esta_ativo = models.BooleanField(default=False)
    porta = models.IntegerField()
    nome = models.CharField(max_length=50)
    ip = models.CharField(max_length=30)

    def __str__(self) -> str:
        return "Dispositivo: " + str(self.id) + " - Tipo de Medição: " + self.tipo_medicao + " - Porta: " + str(self.porta) + " - IP: " + self.ip

