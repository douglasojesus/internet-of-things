from django.db import models

# Create your models here.
class DataConnection(models.Model):
    id_aplicacao = models.CharField(max_length=50)
    comando = models.CharField(max_length=50)
    data = models.CharField(max_length=50)

    def __str__(self):
        return self.id_aplicacao

