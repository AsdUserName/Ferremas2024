from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from api.models import Producto, Precio
from api.bcch_api import get_dolar

class ProductoModelTestCase(TestCase):
    def test_create_producto(self):
        producto = Producto.objects.create(codigo_producto="TP001", marca="Test Marca", codigo="TP001", nombre="Test Producto")
        self.assertEqual(producto.codigo_producto, "TP001")
        self.assertEqual(producto.marca, "Test Marca")
        self.assertEqual(producto.codigo, "TP001")
        self.assertEqual(producto.nombre, "Test Producto")

    def test_producto_str_representation(self):
        producto = Producto.objects.create(codigo_producto="TP001", marca="Test Marca", codigo="TP001", nombre="Test Producto")
        self.assertEqual(str(producto), "Test Producto")

    def test_producto_codigo_unique_constraint(self):
        Producto.objects.create(codigo_producto="TP001", marca="Test Marca", codigo="TP001", nombre="Test Producto")
        with self.assertRaises(IntegrityError):
            Producto.objects.create(codigo_producto="TP002", marca="Test Marca", codigo="TP001", nombre="Test Producto 2")

class PrecioModelTestCase(TestCase):
    def test_create_precio(self):
        producto = Producto.objects.create(codigo_producto="TP001", marca="Test Marca", codigo="TP001", nombre="Test Producto")
        precio = Precio.objects.create(producto=producto, valor_usd=100.0)
        self.assertEqual(precio.producto, producto)
        self.assertEqual(precio.valor_usd, 100.0)
        self.assertIsInstance(precio.fecha, timezone.datetime)

    def test_precio_str_representation(self):
        producto = Producto.objects.create(codigo_producto="TP001", marca="Test Marca", codigo="TP001", nombre="Test Producto")
        precio = Precio.objects.create(producto=producto, valor_usd=100.0)
        self.assertEqual(str(precio), f'Test Producto - {precio.fecha}')