import requests
import os

def read_credentials_from_file(file_path: str = os.path.join(os.path.dirname(__file__), "credentials/credentials.txt")) -> tuple[str, str]:
    with open(file_path, "r") as file:
        username, password = file.read().strip().split(":")
    return username, password


def connect_to_api(user: str, password: str):
    API_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    TODAY_DOLAR_VALUE_TIMESERIES_CODE = "F073.TCO.PRE.Z.D"
    GET_SERIES_FUNCTION_NAME = "GetSeries"
    params = {
        "user": user,
        "pass": password,
        "timeseries": TODAY_DOLAR_VALUE_TIMESERIES_CODE,
        "function": GET_SERIES_FUNCTION_NAME,
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()

username, password = read_credentials_from_file()
api_data = connect_to_api(username, password)

def get_dolar(api_data):
    if api_data is not None and "Series" in api_data and "Obs" in api_data["Series"]:
        series_data = api_data["Series"]["Obs"]
        if series_data:
            last_dolar_obs = series_data[-1]
            dolar = float(last_dolar_obs["value"])
            print(dolar)
            return dolar
        else:
            print("No se encontraron observaciones en los datos de la serie.")
    else:
        print("No se pudo obtener los datos de la API.")
    

