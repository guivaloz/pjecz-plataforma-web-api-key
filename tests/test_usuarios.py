"""
Unit tests for usuarios
"""

import unittest

import requests

from tests.load_env import config


class TestUsuarios(unittest.TestCase):
    """Tests for usuarios category"""

    def test_get_usuarios(self):
        """Test GET method for usuarios"""
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/usuarios",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(f"Connection error: {error}")
        except requests.exceptions.Timeout as error:
            self.fail(f"Timeout error: {error}")
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual(contenido["success"], True)
        self.assertEqual("message" in contenido, True)
        self.assertEqual("total" in contenido, True)
        self.assertEqual("limit" in contenido, True)
        self.assertEqual("offset" in contenido, True)
        self.assertEqual("items" in contenido, True)
        for item in contenido["items"]:
            self.assertEqual("id" in item, True)
            self.assertEqual("email" in item, True)
            self.assertEqual("nombres" in item, True)
            self.assertEqual("apellido_paterno" in item, True)
            self.assertEqual("apellido_materno" in item, True)

    def test_get_usuario_by_email(self):
        """Test GET method for usuario by email"""
        try:
            response = requests.get(
                url=f"{config['api_base_url']}/usuarios/no.existe@servidor.com",
                headers={"X-Api-Key": config["api_key"]},
                timeout=config["timeout"],
            )
        except requests.exceptions.ConnectionError as error:
            self.fail(f"Connection error: {error}")
        except requests.exceptions.Timeout as error:
            self.fail(f"Timeout error: {error}")
        self.assertEqual(response.status_code, 200)
        contenido = response.json()
        self.assertEqual("success" in contenido, True)
        self.assertEqual(contenido["success"], False)


if __name__ == "__main__":
    unittest.main()
