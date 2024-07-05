from unittest.mock import mock_open, patch

import pytest
from api.bcch_api import connect_to_api, get_dolar, read_credentials_from_file


@patch("builtins.open", new_callable=mock_open, read_data="gonzalo:misuperpassword")
def test_read_credentials(mock_file):
    user, password = read_credentials_from_file("credentials/credentials.txt")
    assert user == "gonzalo"
    assert password == "misuperpassword"


@patch("requests.get")
def test_connect_to_api(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"mock_data": "test_data"}
    mock_response.status_code = 200

    api_data = connect_to_api("test_user", "test_password")
    assert api_data == {"mock_data": "test_data"}


def test_get_dolar():
    api_data = {
        "Series": {
            "Obs": [
                {"value": "1.2345"},
                {"value": "1.2346"},
                {"value": "1.2347"}
            ]
        }
    }
    dolar = get_dolar(api_data)
    assert dolar == 1.2347
