from django.db import models

from api.bcch_api import get_dolar

# Create your models here.

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=10, null=False)
    marca = models.CharField(max_length=20, blank=True)
    codigo = models.CharField(max_length=10, null=False, unique=True)
    nombre = models.CharField(max_length=35, null=False)

    def __str__(self):
        return self.nombre

class Precio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios', null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    valor_usd = models.FloatField()

    @property
    def valor_clp(self):
        dolar = get_dolar()
        return round(self.valor_usd * dolar)

    def __str__(self):
        return f'{self.producto.nombre} - {self.fecha}'
