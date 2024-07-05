from django.urls import path, include
from rest_framework import routers
from .views import ProductoViewSet, PrecioViewSet

router = routers.DefaultRouter()
router.register(r'precios', PrecioViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
