from membresia import Gratis, Basica, Familiar, SinConexión, Pro

def probar_cambio_membresia(membresia, tipos_validos, tipos_invalidos):
    print(f"\nProbando cambios de membresía para {type(membresia).__name__}:")
    for tipo in tipos_validos:
        nueva_membresia = membresia.cambiar_membresia(tipo)
        print(f"Cambio a {type(nueva_membresia).__name__} exitoso.")
    for tipo in tipos_invalidos:
        nueva_membresia = membresia.cambiar_membresia(tipo)
        print(f"Cambio a {type(nueva_membresia).__name__} no válido.")

def probar_cancelacion_membresia(membresia):
    print(f"\nProbando cancelación de membresía para {type(membresia).__name__}:")
    cancelada = membresia.cancelar_membresia()
    print(f"Membresía cancelada, ahora es {type(cancelada).__name__}.")

def probar_control_parental(familiar):
    print(f"\nProbando control parental para {type(familiar).__name__}:")
    familiar.modificar_control_parental()

def probar_contenido_sin_conexion(sin_conexion):
    print(f"\nProbando contenido sin conexión para {type(sin_conexion).__name__}:")
    sin_conexion.incrementar_contenido_sin_conexion()
    sin_conexion.incrementar_contenido_sin_conexion()

if __name__ == "__main__":
    # Crea una instancia de cada tipo de membresía
    gratis = Gratis("correo@ejemplo.com", "1234567890123456")
    basica = Basica("correo@ejemplo.com", "1234567890123456")
    familiar = Familiar("correo@ejemplo.com", "1234567890123456")
    sin_conexion = SinConexión("correo@ejemplo.com", "1234567890123456")
    pro = Pro("correo@ejemplo.com", "1234567890123456")

    # Prueba cambios de membresía
    probar_cambio_membresia(gratis, [1, 2, 3, 4], [0, 5])
    probar_cambio_membresia(basica, [2, 3, 4], [0, 1])
    probar_cambio_membresia(familiar, [1, 3, 4], [0, 2])
    probar_cambio_membresia(sin_conexion, [1, 2, 4], [0, 3])
    probar_cambio_membresia(pro, [1, 2, 3], [0, 4])

    # Prueba cancelación de membresía
    probar_cancelacion_membresia(basica)
    probar_cancelacion_membresia(familiar)
    probar_cancelacion_membresia(sin_conexion)
    probar_cancelacion_membresia(pro)

    # Prueba control parental (solo para Familiar y Pro)
    probar_control_parental(familiar)
    probar_control_parental(pro)

    # Prueba contenido sin conexión (solo para SinConexión y Pro)
    probar_contenido_sin_conexion(sin_conexion)
    probar_contenido_sin_conexion(pro)