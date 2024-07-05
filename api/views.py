from .serializers import PrecioSerializer, ProductoSerializer
from .models import Producto, Precio

from rest_framework import viewsets, status
from rest_framework.response import Response

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType

from django.shortcuts import redirect, HttpResponse

import random

class PrecioViewSet(viewsets.ModelViewSet):
    queryset = Precio.objects.all()
    serializer_class = PrecioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        Precio.objects.filter(producto=instance).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class WebpayPlusCreate(APIView):

    def post(self, request):
        print("Webpay Plus Transbank.create")
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = str(random.randrange(1000000, 99999999))
        amount = str(random.randrange(1000000, 99999999))
        return_url = "http://127.0.0.1:8000/commit-webpay-plus/"

        tx = Transaction(WebpayOptions(settings.TRANBANK_COMMERCE_CODE, settings.TRANBANK_API_KEY, IntegrationType.TEST))
        response = tx.create(buy_order, session_id, amount, return_url)
        if response:
            return redirect(response['url'] + "?token_ws=" + response['token'])
        else:
            return HttpResponse("No se recibió respuesta de Transbank.")

class CommitWebpayTransaction(APIView):
    def get(self, request):
        #GET /api/webpay-plus/commit/?token_ws=01ab1b95d9458896414de079835c4486a5324d0aafb839ed22980e3afef12c10

        token_ws = request.query_params.get('token_ws')
        print(token_ws)
        if token_ws:
            try:
                result = (Transaction()).commit(token_ws)
                return Response({"status": "Success", "detail": result})
            except TransbankError as e:
                return Response({"error": str(e)}, status=500)
        else:
            return Response({"error": "Token not provided"}, status=400)