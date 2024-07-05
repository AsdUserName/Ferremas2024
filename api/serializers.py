from rest_framework import serializers
from .models import Producto, Precio

class PrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precio
        fields = ['id', 'fecha', 'valor_usd', 'valor_clp']


class ProductoSerializer(serializers.ModelSerializer):
    precios = PrecioSerializer(many=True)

    class Meta:
        model = Producto
        fields = ['id', 'codigo_producto', 'marca', 'codigo', 'nombre', 'precios']