import requests
import pytest
from unittest.mock import Mock

# Función que queremos probar
def get_product_info(product_id):
    url = f"https://api.mercadolibre.com/items/{product_id}"
    response = requests.get(url)
    response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
    return response.json()

# Prueba parametrizada con múltiples casos
@pytest.mark.parametrize(
    "product_id, mock_status_code, mock_json, expected_output",
    [
        (
            "MLA123456789",  # ID del producto
            200,  # Estado HTTP
            {"id": "MLA123456789", "title": "Smart Watch", "price": 100.0},  # Respuesta simulada
            {"id": "MLA123456789", "title": "Smart Watch", "price": 100.0},  # Resultado esperado
        ),
        (
            "MLA999999999",
            200,
            {"id": "MLA999999999", "title": "Notebook", "price": 320.0},
            {"id": "MLA999999999", "title": "Notebook", "price": 320.0},
        ),
        (
            "MLA111111111",
            200,
            {"id": "MLA111111111", "title": "Producto 3"},
            {"id": "MLA111111111", "title": "Producto 3"},
        ),
    ],
)
def test_get_product_info_multiple_cases(mocker, product_id, mock_status_code, mock_json, expected_output):
    # Crear un mock para la respuesta de la API
    mock_response = Mock()
    mock_response.status_code = mock_status_code
    mock_response.json.return_value = mock_json

    if mock_status_code >= 400:
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            f"{mock_status_code} Error"
        )

    # Mockear la función requests.get para devolver nuestra respuesta simulada
    mocker.patch("requests.get", return_value=mock_response)

    # Si esperamos una excepción, usamos pytest.raises
    if isinstance(expected_output, type) and issubclass(expected_output, Exception):
        with expected_output:
            get_product_info(product_id)
    else:
        # Si no, llamamos a la función y verificamos el resultado
        product_info = get_product_info(product_id)
        assert product_info == expected_output

# Ejecutar las pruebas con pytest
if __name__ == "__main__":
    pytest.main()