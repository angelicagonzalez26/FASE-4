#---------------------------------------------------------------------------
#Grupo: JOHANNA PAOLA BRICENO MORENO - MARIA ANGELICA GONZALEZ ARTUNDUAGA  
#Grupo: 213023_468  
#Programa: Ingeniería Multimedia - Programación  
#Código Fuente: autoría propia
#Face 4 - Componente práctico - Prácticas simuladas
#---------------------------------------------------------------------------

from abc import ABC, abstractmethod
import logging

# CONFIGURACION DEL ARCHIVO DE REGISTRO DEL SISTEMA (LOG)
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
# EXCEPCIONES PERSONALIZADAS

class ErrorSistema(Exception):
    """Clase general para los errores del sistema."""
    pass


class DatoInvalidoError(ErrorSistema):
    pass


class ClienteNoEncontradoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaError(ErrorSistema):
    pass


class OperacionNoPermitidaError(ErrorSistema):
    pass
    
# AGREGAR CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):
    def __init__(self, identificacion):
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise DatoInvalidoError("La identificacion no puede estar vacia.")

        self.__identificacion = identificacion.strip()

    def get_identificacion(self):
        return self.__identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass
        
# AGREGAR CLASE CLIENTE

class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre no puede estar vacio.")

        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise DatoInvalidoError("El correo electronico no es valido.")

        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 7:
            raise DatoInvalidoError("El telefono debe tener al menos 7 digitos.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    def get_nombre(self):
        return self.__nombre

    def mostrar_informacion(self):
        return (
            f"Identificacion: {self.get_identificacion()} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Telefono: {self.__telefono}"
        )

# AGREGAR CLASE ABSTRACTA SERVICIO

class Servicio(ABC):
    def __init__(self, nombre, precio):
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")

        if not isinstance(precio, (int, float)) or isinstance(precio, bool) or precio <= 0:
            raise DatoInvalidoError("El precio debe ser un numero mayor que cero.")

        self._nombre = nombre.strip()
        self._precio = float(precio)
        self.__disponible = True

    def get_nombre(self):
        return self._nombre

    def esta_disponible(self):
        return self.__disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado debe ser verdadero o falso.")
        self.__disponible = estado

    def calcular_total(self, duracion, descuento=0, impuesto=0, **datos):
        """
        Metodo con parametros opcionales:
        - Solo duracion.
        - Duracion y descuento.
        - Duracion, descuento e impuesto.
        """
        self.validar_parametros(duracion, **datos)
        self.validar_porcentajes(descuento, impuesto)

        costo = self.calcular_costo(duracion, **datos)
        subtotal = costo - (costo * descuento / 100)
        total = subtotal + (subtotal * impuesto / 100)

        return round(total, 2)

    @staticmethod
    def validar_porcentajes(descuento, impuesto):
        if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100.")

        if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 100:
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 100.")

    def reservar_recursos(self, **datos):
        """Se puede sobrescribir en servicios que manejen cantidades."""
        if not self.esta_disponible():
            raise ServicioNoDisponibleError(
                f"El servicio {self._nombre} no esta disponible."
            )
        self.cambiar_disponibilidad(False)

    def liberar_recursos(self, **datos):
        self.cambiar_disponibilidad(True)

    @abstractmethod
    def calcular_costo(self, duracion, **datos):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion, **datos):
        pass

#SERVICIO DE RESERVA DE SALAS

class ReservaSala(Servicio):
    def __init__(self, precio_por_hora, capacidad):
        super().__init__("Reserva de sala", precio_por_hora)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")

        self.__capacidad = capacidad

    def validar_parametros(self, duracion, **datos):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatoInvalidoError("La duracion debe ser mayor que cero.")

        personas = datos.get("personas")
        if not isinstance(personas, int) or isinstance(personas, bool) or personas <= 0:
            raise DatoInvalidoError("Debe indicar una cantidad valida de personas.")

        if personas > self.__capacidad:
            raise DatoInvalidoError("La cantidad de personas supera la capacidad de la sala.")

    def calcular_costo(self, duracion, **datos):
        self.validar_parametros(duracion, **datos)
        return self._precio * duracion

    def describir_servicio(self):
        return (
            f"{self.get_nombre()} | Capacidad: {self.__capacidad} personas | "
            f"Precio por hora: ${self._precio:,.0f}"
        )

#FUNCION SERVICIO DE ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):
    def __init__(self, precio_por_dia, cantidad_disponible):
        super().__init__("Alquiler de equipos", precio_por_dia)

        if (
            not isinstance(cantidad_disponible, int)
            or isinstance(cantidad_disponible, bool)
            or cantidad_disponible <= 0
        ):
            raise DatoInvalidoError("La cantidad de equipos debe ser positiva.")

        self.__cantidad_disponible = cantidad_disponible

    def get_cantidad_disponible(self):
        return self.__cantidad_disponible

    def validar_parametros(self, duracion, **datos):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatoInvalidoError("La duracion del alquiler debe ser mayor que cero.")

        cantidad = datos.get("cantidad")
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            raise DatoInvalidoError("Debe indicar una cantidad entera de equipos.")

        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")

    def calcular_costo(self, duracion, **datos):
        self.validar_parametros(duracion, **datos)
        cantidad = datos["cantidad"]
        return self._precio * duracion * cantidad

    def reservar_recursos(self, **datos):
        cantidad = datos.get("cantidad")
        self.validar_parametros(1, cantidad=cantidad)
        self.__cantidad_disponible -= cantidad

    def liberar_recursos(self, **datos):
        cantidad = datos.get("cantidad", 0)
        self.__cantidad_disponible += cantidad

    def describir_servicio(self):
        return (
            f"{self.get_nombre()} | Equipos disponibles: "
            f"{self.__cantidad_disponible} | Precio por dia y equipo: "
            f"${self._precio:,.0f}"
        )
# =====================================================
# 8. SERVICIO DE ASESORIAS
# =====================================================


