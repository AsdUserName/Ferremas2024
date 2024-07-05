import random
from django.test import TestCase
from ..serializers import PrecioSerializer, ProductoSerializer


class SerializerTestCase(TestCase):

    def test_precio_serializer(self):
        precio_data = {'fecha': '2022-01-01', 'valor_usd': 100.0, 'valor_clp': 80000.0}
        serializer = PrecioSerializer(data=precio_data)
        self.assertTrue(serializer.is_valid())

    def test_producto_serializer(self):
        precio_data = {'fecha': '2022-01-01', 'valor_usd': 100.0, 'valor_clp': 80000.0}
        producto_data = {
            'codigo_producto': 'TP001',
            'arca': 'Test Marca',
            'codigo': str(random.randrange(1000000, 99999999)),
            'nombre': 'Test Producto',
            'precios': [precio_data]  # Add a list of precios
        }
        serializer = ProductoSerializer(data=producto_data)
        self.assertTrue(serializer.is_valid())