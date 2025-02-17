from datetime import datetime, timedelta
import unittest
import time

from TPO2.BancoTPO import Usuario, Banco


class TestBanco(unittest.TestCase):
    def setUp(self):
        self.usuario1 = Usuario("Juan", "1234", 1000)
        self.usuario2 = Usuario("Maria", "5678", 500)
        self.banco = Banco()
        self.banco.agregar_usuario(self.usuario1)
        self.banco.agregar_usuario(self.usuario2)

    def test_deposito(self):
        self.assertTrue(self.usuario1.depositar(500))
        self.assertEqual(self.usuario1.saldo, 1500)

    def test_retiro_exitoso(self):
        self.assertTrue(self.usuario1.retirar(500))
        self.assertEqual(self.usuario1.saldo, 500)

    def test_retiro_insuficiente(self):
        self.assertFalse(self.usuario1.retirar(2000))
        self.assertEqual(self.usuario1.saldo, 1000)

    def test_transferencia_exitosa(self):
        resultado = self.banco.transferir("1234", "5678", 200)
        self.assertEqual(resultado, "Transferencia de $200 realizada con éxito de 1234 a 5678.")
        self.assertEqual(self.usuario1.saldo, 800)
        self.assertEqual(self.usuario2.saldo, 700)

    def test_transferencia_sin_fondos(self):
        resultado = self.banco.transferir("1234", "5678", 2000)
        self.assertEqual(resultado, "Error en la transferencia. Verifique saldo y cuentas.")
        self.assertEqual(self.usuario1.saldo, 1000)
        self.assertEqual(self.usuario2.saldo, 500)

    def test_ver_movimientos(self):
        self.usuario1.depositar(300)
        self.usuario1.retirar(100)
        movimientos = self.usuario1.ver_movimientos()
        self.assertIn("Depósito de $300", movimientos)
        self.assertIn("Retiro de $100", movimientos)


if __name__ == "__main__":
    unittest.main()
