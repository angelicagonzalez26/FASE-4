#Proyecto Face 4 - Grupo: JOHANNA PAOLA BRICENO MORENO - MARIA ANGELICA GONZALEZ ARTUNDUAGA

from abc import ABC, abstractmethod
import logging

# =========================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS (EXCEPCIONES Y ERRORES)
# =========================================================
logging.basicConfig(
    filename='sistema_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================================================
# 1. EXCEPCIONES PERSONALIZADAS
# =========================================================
class ErrorNegocio(Exception):
    """Excepción base para errores de negocio en el sistema."""
    pass

class ErrorClienteInvalido(ErrorNegocio):
    """Se lanza cuando los datos del cliente no son válidos."""
    pass


# =========================================================
# 2. CLASE CLIENTE (Validaciones y Encapsulación)
# =========================================================
class Cliente:
    def __init__(self, nombre: str, identificacion: str):
        self.nombre = nombre
        self.identificacion = identificacion

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor.isdigit():
            logging.error(f"Intento de registro con ID no numérica: {valor}")
            raise ErrorClienteInvalido("El documento de identidad debe contener solo números.")
        self._identificacion = valor

    def obtener_info(self) -> str:
        return f"Cliente: {self.nombre} (ID: {self.identificacion})"


# =========================================================
# 3. CLASE ABSTRACTA BASE (Servicios)
# =========================================================
class Servicio(ABC):
    """
    Clase abstracta que sirve como plantilla general para los servicios
    de la empresa Software FJ.
    """
    def __init__(self, nombre_servicio: str, costo_base: float):
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self) -> float:
        """Método abstracto que cada clase hija implementará obligatoriamente."""
        pass

    def obtener_descripcion(self) -> str:
        return f"Servicio: {self.nombre_servicio} | Costo Base: ${self.costo_base}"


# =========================================================
# 4. CLASES HIJAS DE SERVICIOS (Herencia y Polimorfismo)
# =========================================================
class ReservaSala(Servicio):
    def __init__(self, nombre_servicio: str, costo_base: float, horas: int):
        super().__init__(nombre_servicio, costo_base)
        self.horas = horas

    def calcular_costo(self) -> float:
        return self.costo_base * self.horas


class AlquilerEquipo(Servicio):
    def __init__(self, nombre_servicio: str, costo_base: float, dias: int):
        super().__init__(nombre_servicio, costo_base)
        self.dias = dias

    def calcular_costo(self) -> float:
        # Descuento del 10% si alquila por más de 3 días
        if self.dias > 3:
            return (self.costo_base * self.dias) * 0.90
        return self.costo_base * self.dias


class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre_servicio: str, costo_base: float, nivel_complexidad: str):
        super().__init__(nombre_servicio, costo_base)
        self.nivel_complexidad = nivel_complexidad

    def calcular_costo(self) -> float:
        # Recargo del 20% si la asesoría es avanzada
        if self.nivel_complexidad.lower() == "avanzada":
            return self.costo_base * 1.20
        return self.costo_base


# =========================================================
# 5. BLOQUE PRINCIPAL DE PRUEBAS (Simulación de Operaciones)
# =========================================================
if __name__ == "__main__":
    print("=== INICIANDO SISTEMA DE GESTIÓN SOFTWARE FJ ===")
    
    # Prueba 1: Manejo de errores con excepciones personalizadas y Try/Except
    try:
        print("\nIntentando registrar un cliente con datos inválidos...")
        c_invalido = Cliente("Maria Gomez", "123ABC45") # Disparará error por letras
    except ErrorClienteInvalido as e:
        print(f"[ERROR CAPTURADO EXITOSAMENTE]: {e}")
        print("El sistema continúa funcionando de forma estable.")

    # Prueba 2: Registro exitoso de Cliente y Servicios con Polimorfismo
    try:
        print("\nRegistrando cliente y servicios correctos...")
        cliente_valido = Cliente("Carlos Perez", "1020304050")
        print(cliente_valido.obtener_info())

        # Creación de servicios polimórficos
        servicios = [
            ReservaSala("Sala de Juntas Principal", 50.0, 4),
            AlquilerEquipo("Laptop Dell Core i7", 35.0, 5),
            AsesoriaEspecializada("Consultoría de Arquitectura Python", 120.0, "avanzada")
        ]

        # Recorremos la lista aplicando polimorfismo con un solo ciclo
        for serv in servicios:
            print(f"- {serv.obtener_descripcion()} | Total a pagar: ${serv.calcular_costo():.2f}")

    except Exception as ex:
        print(f"Error inesperado: {ex}")

    print("\n=== PRUEBA FINALIZADA CON ÉXITO ===")
