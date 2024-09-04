from abc import ABC, abstractmethod

class Membresia(ABC):
    """
    Clase abstracta que define los atributos y métodos comunes para todos los tipos de membresías.
    """

    def __init__(self, correo: str, numero_tarjeta: str):
        """
        Inicializa una nueva instancia de Membresia.

        Args:
            correo (str): Correo electrónico del suscriptor.
            numero_tarjeta (str): Número de tarjeta del suscriptor.
        """
        self._correo = correo
        self._numero_tarjeta = numero_tarjeta

    @property
    def correo(self):
        """
        Devuelve el correo electrónico del suscriptor.
        """
        return self._correo

    @property
    def numero_tarjeta(self):
        """
        Devuelve el número de tarjeta del suscriptor.
        """
        return self._numero_tarjeta

    @abstractmethod
    def cambiar_membresia(self, tipo_membresia: int) -> 'Membresia':
        """
        Cambia la membresía actual a un nuevo tipo.

        Args:
            tipo_membresia (int): Identificador numérico del tipo de membresía a la que se desea cambiar.

        Returns:
            Membresia: Nueva membresía, si el cambio fue exitoso.
                        Membresía actual, si el cambio no fue exitoso.
        """
        pass

    @abstractmethod
    def cancelar_membresia(self) -> 'Membresia':
        """
        Cancela la membresía actual.

        Returns:
            Membresia: Nueva membresía gratuita.
        """
        pass

    def _crear_nueva_membresia(self, nueva_membresia: int):
        """
        Crea una nueva membresía según el tipo solicitado.

        Args:
            nueva_membresia (int): Identificador numérico del tipo de membresía a crear.

        Returns:
            Membresia: Nueva membresía creada.
        """
        if nueva_membresia == 1:
            return Basica(self.correo, self.numero_tarjeta)
        elif nueva_membresia == 2:
            return Familiar(self.correo, self.numero_tarjeta)
        elif nueva_membresia == 3:
            return SinConexión(self.correo, self.numero_tarjeta)
        elif nueva_membresia == 4:
            return Pro(self.correo, self.numero_tarjeta)
        else:
            return self

class Gratis(Membresia):
    """
    Clase que representa una membresía gratuita.
    """

    _costo = 0
    _dispositivos = 1

    def cambiar_membresia(self, tipo_membresia: int) -> 'Membresia':
        """
        Cambia la membresía gratuita a otro tipo.

        Args:
            tipo_membresia (int): Identificador numérico del tipo de membresía a la que se desea cambiar.

        Returns:
            Membresia: Nueva membresía, si el cambio fue exitoso.
                        Membresía actual, si el cambio no fue exitoso.
        """
        if 1 <= tipo_membresia <= 4:
            return self._crear_nueva_membresia(tipo_membresia)
        return self

    def cancelar_membresia(self) -> 'Membresia':
        """
        Cancela la membresía gratuita.

        Returns:
            Membresia: Membresía gratuita (no se aplica la cancelación).
        """
        return self


class Basica(Membresia):
    """
    Clase que representa una membresía básica.
    """

    _costo = 3000
    _dispositivos = 2

    def cambiar_membresia(self, tipo_membresia: int) -> 'Membresia':
        """
        Cambia la membresía básica a otro tipo.

        Args:
            tipo_membresia (int): Identificador numérico del tipo de membresía a la que se desea cambiar.

        Returns:
            Membresia: Nueva membresía, si el cambio fue exitoso.
                        Membresía actual, si el cambio no fue exitoso.
        """
        if 2 <= tipo_membresia <= 4:
            return self._crear_nueva_membresia(tipo_membresia)
        return self

    def cancelar_membresia(self) -> 'Membresia':
        """
        Cancela la membresía básica.

        Returns:
            Membresia: Nueva membresía gratuita.
        """
        return self._crear_nueva_membresia(0)


class Familiar(Membresia):
    """
    Clase que representa una membresía familiar.
    """

    _costo = 5000
    _dispositivos = 5

    def __init__(self, correo: str, numero_tarjeta: str):
        """
        Inicializa una nueva instancia de Membresia Familiar.

        Args:
            correo (str): Correo electrónico del suscriptor.
            numero_tarjeta (str): Número de tarjeta del suscriptor.
        """
        super().__init__(correo, numero_tarjeta)
        self._dias_regalo = 7

    def cambiar_membresia(self, tipo_membresia: int) -> 'Membresia':
        """
        Cambia la membresía familiar a otro tipo.

        Args:
            tipo_membresia (int): Identificador numérico del tipo de membresía a la que se desea cambiar.

        Returns:
            Membresia: Nueva membresía, si el cambio fue exitoso.
                        Membresía actual, si el cambio no fue exitoso.
        """
        if tipo_membresia in [1, 3, 4]:
            return self._crear_nueva_membresia(tipo_membresia)
        return self

    def cancelar_membresia(self) -> 'Membresia':
        """
        Cancela la membresía familiar.

        Returns:
            Membresia: Nueva membresía gratuita.
        """
        return self._crear_nueva_membresia(0)

    def modificar_control_parental(self):
        """
        Método para modificar el control parental.
        """
        print("Control parental modificado.")

class SinConexión(Membresia):
    """
    Clase que representa una membresía sin conexión.
    """

    _costo = 3500
    _dispositivos = 2

    def __init__(self, correo: str, numero_tarjeta: str):
        """
        Inicializa una nueva instancia de Membresia Sin Conexión.

        Args:
            correo (str): Correo electrónico del suscriptor.
            numero_tarjeta (str): Número de tarjeta del suscriptor.
        """
        super().__init__(correo, numero_tarjeta)
        self._dias_regalo = 7
        self._contenido_sin_conexion = 0

    def cambiar_membresia(self, tipo_membresia: int) -> 'Membresia':
        """
        Cambia la membresía sin conexión a otro tipo.

        Args:
            tipo_membresia (int): Identificador numérico del tipo de membresía a la que se desea cambiar.

        Returns:
            Membresia: Nueva membresía, si el cambio fue exitoso.
                        Membresía actual, si el cambio no fue exitoso.
        """
        if tipo_membresia in [1, 2, 4]:
            return self._crear_nueva_membresia(tipo_membresia)
        return self

    def cancelar_membresia(self) -> 'Membresia':
        """
        Cancela la membresía sin conexión.

        Returns:
            Membresia: Nueva membresía gratuita.
        """
        return self._crear_nueva_membresia(0)

    def incrementar_contenido_sin_conexion(self):
        """
        Método para incrementar la cantidad máxima de contenido disponible para ver sin conexión.
        """
        self._contenido_sin_conexion += 1
        print(f"Contenido sin conexión aumentado a {self._contenido_sin_conexion}.")

class Pro(Familiar, SinConexión):
    """
    Clase que representa una membresía Pro. Hereda de Familiar y Sin Conexión.
    """

    _costo = 7000
    _dispositivos = 6

    def __init__(self, correo: str, numero_tarjeta: str):
        """
        Inicializa una nueva instancia de Membresia Pro.

        Args:
            correo (str): Correo electrónico del suscriptor.
            numero_tarjeta (str): Número de tarjeta del suscriptor.
        """
        Familiar.__init__(self, correo, numero_tarjeta)
        self._dias_regalo = 15

    def cambiar_membresia(self, tipo_membresia: int) -> 'Membresia':
        """
        Cambia la membresía Pro a otro tipo.

        Args:
            tipo_membresia (int): Identificador numérico del tipo de membresía a la que se desea cambiar.

        Returns:
            Membresia: Nueva membresía, si el cambio fue exitoso.
                        Membresía actual, si el cambio no fue exitoso.
        """
        if 1 <= tipo_membresia <= 3:
            return self._crear_nueva_membresia(tipo_membresia)
        return self

    def cancelar_membresia(self) -> 'Membresia':
        """
        Cancela la membresía Pro.

        Returns:
            Membresia: Nueva membresía gratuita.
        """
        return self._crear_nueva_membresia(0)