#---------------------------------------------------------------------------
#Grupo: JOHANNA PAOLA BRICEÑO MORENO - MARIA ANGELICA GONZALEZ ARTUNDUAGA  
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
# SERVICIO DE ASESORIAS ESPECIALIZADAS


class Asesoria(Servicio):
    def __init__(self, precio_por_hora, especialidad):
        super().__init__("Asesoria especializada", precio_por_hora)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("Debe indicar la especialidad de la asesoria.")

        self.__especialidad = especialidad.strip()

    def validar_parametros(self, duracion, **datos):
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DatoInvalidoError("La duracion de la asesoria debe ser mayor que cero.")

        modalidad = datos.get("modalidad")
        if modalidad not in ("Virtual", "Presencial"):
            raise DatoInvalidoError("La modalidad debe ser Virtual o Presencial.")

    def calcular_costo(self, duracion, **datos):
        self.validar_parametros(duracion, **datos)
        return self._precio * duracion

    def describir_servicio(self):
        return (
            f"{self.get_nombre()} | Especialidad: {self.__especialidad} | "
            f"Precio por hora: ${self._precio:,.0f}"
        )


# GESTION DE RESERVAS

class Reserva:
    contador = 1

    def __init__(self, cliente, servicio, duracion, **datos):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Debe seleccionar un cliente valido.")

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Debe seleccionar un servicio valido.")

        servicio.validar_parametros(duracion, **datos)

        self.__codigo = Reserva.contador
        Reserva.contador += 1

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__datos = datos.copy()
        self.__estado = "Pendiente"
        self.__total = 0.0

    def get_codigo(self):
        return self.__codigo

    def get_estado(self):
        return self.__estado

    def get_total(self):
        return self.__total

    def confirmar(self):
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__servicio.reservar_recursos(**self.__datos)
        self.__estado = "Confirmada"

        logging.info("Reserva %s confirmada.", self.__codigo)

    def cancelar(self):
        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas confirmadas."
            )

        self.__servicio.liberar_recursos(**self.__datos)
        self.__estado = "Cancelada"

        logging.info("Reserva %s cancelada.", self.__codigo)

    def procesar(self, descuento=0, impuesto=0):
        try:
            if self.__estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "La reserva no se encuentra pendiente."
                )

            self.__total = self.__servicio.calcular_total(
                self.__duracion,
                descuento,
                impuesto,
                **self.__datos
            )

            self.confirmar()

        except ErrorSistema as error:
            logging.exception(
                "No se pudo procesar la reserva %s.", self.__codigo
            )
            raise ReservaError(
                "No fue posible procesar la reserva."
            ) from error

        except Exception as error:
            logging.exception(
                "Error inesperado en la reserva %s.", self.__codigo
            )
            raise ReservaError(
                "Ocurrio un error inesperado al procesar la reserva."
            ) from error

        return self.__total

    def mostrar_reserva(self):
        return (
            f"Codigo: {self.__codigo}\n"
            f"Cliente: {self.__cliente.get_nombre()}\n"
            f"Servicio: {self.__servicio.get_nombre()}\n"
            f"Duracion: {self.__duracion}\n"
            f"Estado: {self.__estado}\n"
            f"Total: ${self.__total:,.2f}"
        )


# CONTROLADOR PRINCIPAL DEL SISTEMA (SOFTWARE FJ)

class SistemaSoftwareFJ:
    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El objeto no es un cliente valido.")

        for cliente_guardado in self.__clientes:
            if (
                cliente_guardado.get_identificacion()
                == cliente.get_identificacion()
            ):
                raise DatoInvalidoError("El cliente ya esta registrado.")

        self.__clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.get_nombre())

    def buscar_cliente(self, identificacion):
        for cliente in self.__clientes:
            if cliente.get_identificacion() == identificacion:
                return cliente

        raise ClienteNoEncontradoError("No se encontro el cliente.")

    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El objeto no es un servicio valido.")

        self.__servicios.append(servicio)
        logging.info("Servicio agregado: %s", servicio.get_nombre())

    def crear_reserva(self, cliente, servicio, duracion, **datos):
        if cliente not in self.__clientes:
            raise ClienteNoEncontradoError(
                "El cliente no esta registrado en el sistema."
            )

        if servicio not in self.__servicios:
            raise ServicioNoDisponibleError(
                "El servicio no esta registrado en el sistema."
            )

        reserva = Reserva(cliente, servicio, duracion, **datos)
        self.__reservas.append(reserva)

        logging.info("Reserva creada: %s", reserva.get_codigo())
        return reserva

    def listar_clientes(self):
        return self.__clientes.copy()

    def listar_servicios(self):
        return self.__servicios.copy()

    def listar_reservas(self):
        return self.__reservas.copy()


# 11. FUNCION PARA EJECUTAR Y CONTROLAR OPERACIONES

def ejecutar_operacion(numero, descripcion, funcion):
    print("\n" + "=" * 55)
    print(f"OPERACION {numero}: {descripcion}")

    try:
        resultado = funcion()

    except ErrorSistema as error:
        print("Error controlado:", error)
        logging.error("Operacion %s: %s", numero, error)

    except Exception as error:
        print("Error inesperado:", error)
        logging.exception("Error inesperado en la operacion %s", numero)

    else:
        print("Operacion realizada correctamente.")
        if resultado is not None:
            print(resultado)

    finally:
        print("Fin de la operacion.")
        logging.info("Finalizo la operacion %s.", numero)


# SIMULACION DE PRUEBAS DEL SISTEMA == 15 OPERACIONES

def main():
    sistema = SistemaSoftwareFJ()

    # Crear los servicios
    sala = ReservaSala(50000, 15)
    equipos = AlquilerEquipo(30000, 5)
    asesoria = Asesoria(80000, "Desarrollo de software")

    # 1. Registrar un cliente valido
    cliente1 = Cliente(
        "1001", "Carlos Perez", "carlos@gmail.com", "3001234567"
    )
    ejecutar_operacion(
        1, "Registrar cliente Carlos",
        lambda: sistema.registrar_cliente(cliente1)
    )

    # 2. Registrar otro cliente valido
    cliente2 = Cliente(
        "1002", "Maria Lopez", "maria@gmail.com", "3101234567"
    )
    ejecutar_operacion(
        2, "Registrar cliente Maria",
        lambda: sistema.registrar_cliente(cliente2)
    )

    # 3. Intentar registrar un cliente con correo incorrecto
    def registrar_cliente_invalido():
        cliente = Cliente(
            "1003", "Juan Torres", "correo_incorrecto", "3001234567"
        )
        sistema.registrar_cliente(cliente)

    ejecutar_operacion(
        3, "Registrar cliente con correo incorrecto",
        registrar_cliente_invalido
    )

    # 4. Intentar registrar un cliente repetido
    ejecutar_operacion(
        4, "Registrar un cliente duplicado",
        lambda: sistema.registrar_cliente(cliente1)
    )

    # 5, 6 y 7. Agregar los tres servicios
    ejecutar_operacion(
        5, "Agregar servicio de reserva de salas",
        lambda: sistema.agregar_servicio(sala)
    )
    ejecutar_operacion(
        6, "Agregar servicio de alquiler de equipos",
        lambda: sistema.agregar_servicio(equipos)
    )
    ejecutar_operacion(
        7, "Agregar servicio de asesoria",
        lambda: sistema.agregar_servicio(asesoria)
    )

    # 8. Intentar agregar un servicio incorrecto
    ejecutar_operacion(
        8, "Intentar agregar un servicio no valido",
        lambda: sistema.agregar_servicio("Servicio desconocido")
    )

    # 9. Crear y procesar una reserva de sala
    def reservar_sala():
        reserva = sistema.crear_reserva(
            cliente1, sala, 2, personas=10
        )
        reserva.procesar(descuento=10, impuesto=19)
        return reserva.mostrar_reserva()

    ejecutar_operacion(
        9, "Crear reserva correcta de sala",
        reservar_sala
    )

    # 10. Intentar reservar la misma sala otra vez
    def reservar_sala_ocupada():
        reserva = sistema.crear_reserva(
            cliente2, sala, 1, personas=5
        )
        reserva.procesar()
        return reserva.mostrar_reserva()

    ejecutar_operacion(
        10, "Intentar reservar una sala ocupada",
        reservar_sala_ocupada
    )

    # 11. Alquilar dos equipos correctamente
    def reservar_equipos():
        reserva = sistema.crear_reserva(
            cliente2, equipos, 2, cantidad=2
        )
        reserva.procesar(descuento=5, impuesto=19)
        return reserva.mostrar_reserva()

    ejecutar_operacion(
        11, "Alquilar equipos correctamente",
        reservar_equipos
    )

    # 12. Solicitar mas equipos de los disponibles
    def reservar_demasiados_equipos():
        reserva = sistema.crear_reserva(
            cliente1, equipos, 1, cantidad=10
        )
        reserva.procesar()
        return reserva.mostrar_reserva()

    ejecutar_operacion(
        12, "Solicitar mas equipos de los disponibles",
        reservar_demasiados_equipos
    )

    # 13. Reservar una asesoria
    def reservar_asesoria():
        reserva = sistema.crear_reserva(
            cliente1, asesoria, 2, modalidad="Virtual"
        )
        reserva.procesar(impuesto=19)
        return reserva.mostrar_reserva()

    ejecutar_operacion(
        13, "Reservar una asesoria especializada",
        reservar_asesoria
    )

    # 14. Buscar un cliente que no existe
    ejecutar_operacion(
        14, "Buscar un cliente inexistente",
        lambda: sistema.buscar_cliente("9999")
    )

    # 15. Intentar crear una reserva con duracion negativa
    def reserva_con_duracion_invalida():
        return sistema.crear_reserva(
            cliente1, asesoria, -2, modalidad="Virtual"
        )

    ejecutar_operacion(
        15, "Crear una reserva con duracion negativa",
        reserva_con_duracion_invalida
    )

# INFORME FINAL DE OPERACIONES

    print("\n" + "=" * 55)
    print("SOFTWARE FJ - INFORME FINAL")
    print("=" * 55)

    print("\nCLIENTES REGISTRADOS:")
    for cliente in sistema.listar_clientes():
        print(cliente.mostrar_informacion())

    print("\nSERVICIOS REGISTRADOS:")
    for servicio in sistema.listar_servicios():
        print(servicio.describir_servicio())

    print("\nRESERVAS REALIZADAS:")
    for reserva in sistema.listar_reservas():
        print(reserva.mostrar_reserva())
        print("-" * 35)

    print("\nEl sistema termino todas las operaciones.")
    print("Consulta el archivo software_fj.log para ver los eventos y errores.")


# PUNTO DE ENTRADA DEL PROGRAMA

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logging.exception("Error general del programa.")
        print("El programa encontro un error general:", error)
    finally:
        logging.info("Ejecucion del sistema finalizada.")
