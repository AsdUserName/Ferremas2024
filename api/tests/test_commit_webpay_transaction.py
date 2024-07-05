# Importar módulos y bibliotecas necesarias
from unittest.mock import MagicMock, patch

import pytest
from api.views import CommitWebpayTransaction  
from rest_framework import status  
from rest_framework.test import APIClient  
from transbank.error.transbank_error import TransbankError  


# Definir una clase de prueba con el decorador @pytest.mark.django_db
# Esto asegura que se utilice la base de datos de prueba para esta prueba
@pytest.mark.django_db
class TestCommitWebpayTransaction:
    # Definir un método de prueba con un argumento mock_transaction
    # Este objeto de simulación reemplazará la clase Transaction en el módulo api.views
    @patch("api.views.Transaction")
    def test_commit_webpay_transaction_success(self, mock_transaction):
        # Crear una instancia del cliente de prueba de API
        client = APIClient()
        
        # Definir un valor de token de Webpay de ejemplo
        token_ws = "01ab1b95d9458896414de079835c4486a5324d0aafb839ed22980e3afef12c10"
        
        # Definir la URL para la vista CommitWebpayTransaction
        # incluyendo el parámetro token_ws
        url = f"/commit-webpay-plus/?token_ws={token_ws}"
        
        # Establecer el método commit del objeto de simulación mock_transaction
        # para que devuelva un diccionario con un estado de "éxito" y un detalle de "Transacción comprometida"
        mock_transaction.return_value.commit.return_value = {
            "status": "success",
            "detail": "Transaction committed",
        }
        
        # Enviar una solicitud GET a la URL utilizando la instancia del cliente
        response = client.get(url)
        
        # Afirmar que el código de estado de la respuesta es 200 OK
        assert response.status_code == status.HTTP_200_OK
        
        # Afirmar que los datos de la respuesta son iguales a un diccionario
        # con un estado de "Éxito" y un detalle que contiene los valores de estado y detalle
        assert response.data == {
            "status": "Success",
            "detail": {"status": "success", "detail": "Transaction committed"},
        }
        
        # Afirmar que el método commit del objeto de simulación mock_transaction fue llamado una vez con el parámetro token_ws
        mock_transaction.return_value.commit.assert_called_once_with(token_ws)