from datetime import datetime, timedelta


class Usuario:
    def __init__(self, nombre, numero_cuenta, saldo=0):
        self.nombre = nombre
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo
        self.movimientos = []  # Historial de movimientos

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            self.registrar_movimiento(f"Depósito de ${monto}", "Ingreso")
            return True
        return False

    def retirar(self, monto):
        if 0 < monto <= self.saldo:
            self.saldo -= monto
            self.registrar_movimiento(f"Retiro de ${monto}", "Egreso")
            return True
        return False

    def registrar_movimiento(self, descripcion, tipo):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.movimientos.append(
            {"fecha": fecha, "tipo": tipo, "monto": descripcion.split('$')[1], "descripcion": descripcion})

    def ver_saldo(self):
        return f"Saldo actual: ${self.saldo}"

    def ver_movimientos(self):
        if not self.movimientos:
            return "No hay movimientos aún."
        return "\n".join([f"[{mov['fecha']}] {mov['tipo']} - ${mov['monto']}: {mov['descripcion']}" for mov in
                          self.movimientos[-30:]])


class Banco:
    def __init__(self):
        self.usuarios = {}

    def agregar_usuario(self, usuario):
        self.usuarios[usuario.numero_cuenta] = usuario

    def transferir(self, cuenta_origen, cuenta_destino, monto):
        if cuenta_origen in self.usuarios and cuenta_destino in self.usuarios:
            usuario_origen = self.usuarios[cuenta_origen]
            usuario_destino = self.usuarios[cuenta_destino]

            if usuario_origen.retirar(monto):
                usuario_destino.depositar(monto)
                usuario_origen.registrar_movimiento(f"Transferencia de ${monto} a cuenta {cuenta_destino}", "Egreso")
                usuario_destino.registrar_movimiento(f"Recepción de ${monto} de cuenta {cuenta_origen}", "Ingreso")
                return f"Transferencia de ${monto} realizada con éxito de {cuenta_origen} a {cuenta_destino}."
        return "Error en la transferencia. Verifique saldo y cuentas."


class PlazoFijo:
    def __init__(self, usuario, monto, dias, tasa_interes=0.05):
        self.usuario = usuario
        self.monto = monto
        self.dias = dias
        self.tasa_interes = tasa_interes
        self.fecha_vencimiento = datetime.now() + timedelta(days=dias)

    def calcular_ganancia(self):
        return self.monto * (1 + self.tasa_interes)

    def confirmar(self):
        if self.usuario.retirar(self.monto):
            self.usuario.registrar_movimiento(
                f"Plazo fijo de ${self.monto} a {self.dias} días con tasa {self.tasa_interes * 100}%", "Egreso")
            return f"Plazo fijo confirmado. Monto: ${self.monto}, Plazo: {self.dias} días, Interés: {self.tasa_interes * 100}%. Certificado generado."
        return "Fondos insuficientes para realizar el plazo fijo."