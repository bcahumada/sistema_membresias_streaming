import pickle
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from membresia import Gratis, Basica, Familiar, SinConexión, Pro
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import bcrypt

# Archivos de datos
archivo_activos = "clientes_activos.pickle"
archivo_inactivos = "clientes_inactivos.pickle"
archivo_clave_privada = "clave_privada.pem"
archivo_clave_publica = "clave_publica.pem"

# Define las variables globales
clientes_activos = []
clientes_inactivos = []
clave_privada_rsa = None
clave_publica_rsa = None

def generar_claves_rsa():
    """Genera un par de claves RSA: clave pública y clave privada."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def guardar_clave_privada(private_key, archivo_clave):
    """Guarda la clave privada en un archivo."""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(archivo_clave, "wb") as f:
        f.write(pem)

def guardar_clave_publica(public_key, archivo_clave):
    """Guarda la clave pública en un archivo."""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(archivo_clave, "wb") as f:
        f.write(pem)

def cargar_clave_privada(archivo_clave):
    """Carga la clave privada desde un archivo."""
    with open(archivo_clave, "rb") as f:
        pem = f.read()
    private_key = serialization.load_pem_private_key(
        pem,
        password=None,
        backend=default_backend()
    )
    return private_key

def cargar_clave_publica(archivo_clave):
    """Carga la clave pública desde un archivo."""
    with open(archivo_clave, "rb") as f:
        pem = f.read()
    public_key = serialization.load_pem_public_key(
        pem,
        backend=default_backend()
    )
    return public_key

def cifrar_datos_rsa(datos, public_key):
    """Cifra los datos usando la clave pública RSA."""
    max_chunk_size = public_key.key_size // 8 - 42  
    datos_cifrados = b''
    for i in range(0, len(datos), max_chunk_size):
        chunk = datos[i:i+max_chunk_size]
        datos_cifrados += public_key.encrypt(
            chunk,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    return datos_cifrados

def descifrar_datos_rsa(datos_cifrados, private_key):
    """Descifra los datos usando la clave privada RSA."""
    max_chunk_size = private_key.key_size // 8
    datos_descifrados = b''
    for i in range(0, len(datos_cifrados), max_chunk_size):
        chunk = datos_cifrados[i:i+max_chunk_size]
        datos_descifrados += private_key.decrypt(
            chunk,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    return datos_descifrados

def cifrar_datos_hibrido(datos, public_key):
    """Cifra los datos usando cifrado híbrido (RSA + AES)."""
    # Genera una clave simétrica aleatoria
    clave_simetrica = os.urandom(32)  # 256-bit key for AES-256

    # Cifra los datos con la clave simétrica
    datos_cifrados = cifrar_datos_simetricos(datos, clave_simetrica)

    # Cifra la clave simétrica con la clave pública RSA
    clave_simetrica_cifrada = cifrar_datos_rsa(clave_simetrica, public_key)

    # Devuelve los datos cifrados y la clave simétrica cifrada
    return datos_cifrados, clave_simetrica_cifrada

def descifrar_datos_hibrido(datos_cifrados, clave_simetrica_cifrada, private_key):
    """Descifra los datos usando cifrado híbrido (RSA + AES)."""
    # Descifra la clave simétrica con la clave privada RSA
    clave_simetrica = descifrar_datos_rsa(clave_simetrica_cifrada, private_key)

    # Descifra los datos con la clave simétrica
    datos_descifrados = descifrar_datos_simetricos(datos_cifrados, clave_simetrica)

    return datos_descifrados

def cifrar_datos_simetricos(datos, clave_simetrica):
    """Cifra datos usando una clave simétrica AES."""
    iv = os.urandom(16)  # IV aleatorio para cada cifrado
    cipher = Cipher(algorithms.AES(clave_simetrica), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    datos_padded = padder.update(datos) + padder.finalize()  # Asegúrate de que los datos estén en bytes
    datos_cifrados = encryptor.update(datos_padded) + encryptor.finalize()
    return iv + datos_cifrados  # IV al dato cifrado

def descifrar_datos_simetricos(datos_cifrados, clave_simetrica):
    """Descifra datos usando una clave simétrica AES."""
    iv = datos_cifrados[:16]  # Extrae el IV del inicio
    datos_cifrados = datos_cifrados[16:]  # Resto de los datos cifrados
    cipher = Cipher(algorithms.AES(clave_simetrica), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    datos_descifrados_padded = decryptor.update(datos_cifrados) + decryptor.finalize()
    datos_descifrados = unpadder.update(datos_descifrados_padded) + unpadder.finalize()
    return datos_descifrados

'''def guardar_datos():
    """Guarda los datos de clientes activos en un archivo cifrado."""
    with open(archivo_activos, "wb") as f:
        clientes_activos_cifrado, clave_simetrica_cifrada = cifrar_datos_hibrido(
            pickle.dumps(clientes_activos), clave_publica_rsa
        )
        pickle.dump((clientes_activos_cifrado, clave_simetrica_cifrada), f)

def cargar_datos():
    """Carga los datos de clientes activos desde un archivo cifrado."""
    if os.path.exists(archivo_activos):
        with open(archivo_activos, "rb") as f:
            clientes_activos_cifrado, clave_simetrica_cifrada = pickle.load(f)
        global clientes_activos
        clientes_activos = pickle.loads(descifrar_datos_hibrido(clientes_activos_cifrado, clave_simetrica_cifrada, clave_privada_rsa))'''




# --- Funciones del negocio (cliente, menú, etc) ---

def registrar_cliente():
    """Solicita la información del cliente y crea una nueva membresía."""
    while True:
        primer_nombre = input("Ingresa el primer nombre del cliente: ")
        if primer_nombre.strip() == "":
            print("El primer nombre no puede estar vacío. Intenta de nuevo.")
        elif not all(c.isalpha() or c.isspace() for c in primer_nombre):  # Validación: solo letras y espacios
            print("El primer nombre solo debe contener letras y espacios. Intenta de nuevo.")
        else:
            break

    segundo_nombre = input("Ingresa el segundo nombre del cliente (opcional): ")
    if segundo_nombre.strip() != "" and not all(c.isalpha() or c.isspace() for c in segundo_nombre):
        print("El segundo nombre solo debe contener letras y espacios. Intenta de nuevo.")
        segundo_nombre = ""  # limpiar para vaciar str si es invpalido

    while True:
        apellido_paterno = input("Ingresa el apellido paterno del cliente: ")
        if apellido_paterno.strip() == "":
            print("El apellido paterno no puede estar vacío. Intenta de nuevo.")
        elif not all(c.isalpha() or c.isspace() for c in apellido_paterno):
            print("El apellido paterno solo debe contener letras y espacios. Intenta de nuevo.")
        else:
            break

    apellido_materno = input("Ingresa el apellido materno del cliente (opcional): ")
    if apellido_materno.strip() != "" and not all(c.isalpha() or c.isspace() for c in apellido_materno):
        print("El apellido materno solo debe contener letras y espacios. Intenta de nuevo.")
        apellido_materno = ""

    nombre_completo = f"{primer_nombre} {' ' + segundo_nombre if segundo_nombre.strip() else ''} {apellido_paterno} {' ' + apellido_materno if apellido_materno.strip() else ''}"

    while True:
        correo = input("Ingresa el correo electrónico: ")
        if correo.strip() == "":
            print("El correo electrónico no puede estar vacío. Intenta de nuevo.")
        elif len(correo) < 6 or "@" not in correo:
            print("El correo electrónico debe tener al menos 6 caracteres e incluir '@'. Intenta de nuevo.")
        elif correo.index(".") <= correo.index("@") + 1:
            print("El correo electrónico debe tener un '.' al menos dos posiciones después del '@'. Intenta de nuevo.")
        elif " " in correo:
            print("El correo electrónico no puede contener espacios. Intenta de nuevo.")
        else:
            break

    while True:
        numero_tarjeta = input("Ingresa el número de tarjeta (16 dígitos sin espacios): ")
        if numero_tarjeta.strip() == "":
            print("El número de tarjeta no puede estar vacío. Intenta de nuevo.")
        elif not numero_tarjeta.isdigit() or len(numero_tarjeta) != 16:
            print("El número de tarjeta debe tener 16 dígitos sin espacios. Intenta de nuevo.")
        else:
            break

    while True:
        try:
            tipo_membresia = int(input(
                "Elige el tipo de membresía:\n"
                "1: Básica\n"
                "2: Familiar\n"
                "3: Sin Conexión\n"
                "4: Pro\n"
                "Ingresa el número: "
            ))
            if 1 <= tipo_membresia <= 4:
                break
            else:
                print("Tipo de membresía inválido. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido. Intenta de nuevo.")

    if tipo_membresia == 1:
        membresia = Basica(correo, numero_tarjeta)
    elif tipo_membresia == 2:
        membresia = Familiar(correo, numero_tarjeta)
    elif tipo_membresia == 3:
        membresia = SinConexión(correo, numero_tarjeta)
    elif tipo_membresia == 4:
        membresia = Pro(correo, numero_tarjeta)

    print(f"\nCliente registrado exitosamente!")
    print(f"Nombre: {nombre_completo}")
    print(f"Correo: {membresia.correo}")
    print(f"Membresía: {type(membresia).__name__}")

    # Agrega la membresía a la lista de clientes activos
    clientes_activos.append((nombre_completo, membresia))
    return membresia

def mostrar_opciones():
    """Muestra las opciones disponibles al usuario."""
    print("\nBienvenido/a al Sistema de Membresías Streaming! \n Menú de Opciones:")
    print("1: Registrar nuevo cliente")
    print("2: Ver listado de clientes")
    print("3: Administrar membresías")
    print("4: Salir")

def mostrar_clientes(lista_clientes):
    """Muestra la información de los clientes registrados."""
    if not lista_clientes:
        print("\nNo hay clientes registrados.")
        return

    print("\nClientes Registrados:")
    for i, (nombre, membresia) in enumerate(lista_clientes):
        print(f"{i+1}. {nombre} - {type(membresia).__name__}")

def administrar_membresias():
    """Menú para administrar membresías."""
    global clientes_activos, clientes_inactivos  # Define las variables globales

    # Verificar si hay clientes registrados
    if not clientes_activos and not clientes_inactivos:
        print("\nNo existen clientes registrados aún.")
        return  # Sale de la función si no hay clientes

    while True:
        print("\nAdministración de Membresías:")
        print("1: Cambiar membresía")
        print("2: Cancelar membresía")
        print("3: Reactivar cliente")
        print("4: Volver al menú principal")

        opcion_membresia = input("Ingresa la opción deseada: ")

        if opcion_membresia == "1":
            cambiar_membresia()
        elif opcion_membresia == "2":
            cancelar_membresia()
        elif opcion_membresia == "3":
            reactivar_cliente()
        elif opcion_membresia == "4":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción inválida.")

def cambiar_membresia():
    """Permite al usuario cambiar el tipo de membresía de un cliente."""
    global clientes_activos
    mostrar_clientes(clientes_activos)

    if not clientes_activos:
        return

    while True:
        try:
            index = int(input("Ingresa el número del cliente: ")) - 1
            if 0 <= index < len(clientes_activos):
                break
            else:
                print("Número de cliente inválido. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido. Intenta de nuevo.")

    nombre, membresia_actual = clientes_activos[index]

    print("\nTipos de membresía disponibles:")
    print("1: Básica")
    print("2: Familiar")
    print("3: Sin Conexión")
    print("4: Pro")

    while True:
        try:
            tipo_membresia = int(input("Elige el nuevo tipo de membresía: "))
            if 1 <= tipo_membresia <= 4:
                break
            else:
                print("Tipo de membresía inválido. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido. Intenta de nuevo.")

    nueva_membresia = membresia_actual.cambiar_membresia(tipo_membresia)
    if nueva_membresia:
        clientes_activos[index] = (nombre, nueva_membresia)
        print(f"\nMembresía cambiada exitosamente a {type(nueva_membresia).__name__}.")
    else:
        print("Cambio de membresía no válido.")

def cancelar_membresia():
    """Permite al usuario cancelar la membresía de un cliente."""
    global clientes_activos, clientes_inactivos
    mostrar_clientes(clientes_activos)

    if not clientes_activos:
        return

    while True:
        try:
            index = int(input("Ingresa el número del cliente: ")) - 1
            if 0 <= index < len(clientes_activos):
                break
            else:
                print("Número de cliente inválido. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido. Intenta de nuevo.")

    nombre, membresia_actual = clientes_activos[index]
    cancelada = membresia_actual.cancelar_membresia()

    # Mueve al cliente a la lista de inactivos
    clientes_inactivos.append((nombre, cancelada))
    # Elimina el cliente de la lista de activos
    del clientes_activos[index]

    print(f"\nMembresía cancelada para {nombre}.")

def reactivar_cliente():
    """Permite al usuario reactivar la membresía de un cliente."""
    global clientes_inactivos  # Define la variable global clientes_inactivos

    mostrar_clientes(clientes_inactivos)

    if not clientes_inactivos:
        print("\nNo hay clientes inactivos en este momento.")
        return

    while True:
        try:
            index = int(input("Ingresa el número del cliente: ")) - 1
            if 0 <= index < len(clientes_inactivos):
                break
            else:
                print("Número de cliente inválido. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido. Intenta de nuevo.")

    nombre, membresia_actual = clientes_inactivos[index]

    print("\nTipos de membresía disponibles:")
    print("1: Básica")
    print("2: Familiar")
    print("3: Sin Conexión")
    print("4: Pro")

    while True:
        try:
            tipo_membresia = int(input("Elige el nuevo tipo de membresía: "))
            if 1 <= tipo_membresia <= 4:
                break
            else:
                print("Tipo de membresía inválido. Intenta de nuevo.")
        except ValueError:
            print("Ingresa un número válido. Intenta de nuevo.")

    # Crea una nueva membresía con el tipo seleccionado
    if tipo_membresia == 1:
        nueva_membresia = Basica(membresia_actual.correo, membresia_actual.numero_tarjeta)
    elif tipo_membresia == 2:
        nueva_membresia = Familiar(membresia_actual.correo, membresia_actual.numero_tarjeta)
    elif tipo_membresia == 3:
        nueva_membresia = SinConexión(membresia_actual.correo, membresia_actual.numero_tarjeta)
    elif tipo_membresia == 4:
        nueva_membresia = Pro(membresia_actual.correo, membresia_actual.numero_tarjeta)

    # Mueve el cliente a la lista de activos
    clientes_activos.append((nombre, nueva_membresia))
    # Elimina el cliente de la lista de inactivos
    del clientes_inactivos[index]

    print(f"\nMembresía reactivada para {nombre} con tipo {type(nueva_membresia).__name__}.")

# --- Funciones de guardado y carga ---

def guardar_datos():
    """Guarda los datos en un archivo binario."""
    with open("datos_clientes.pkl", "wb") as archivo:
        pickle.dump((clientes_activos, clientes_inactivos), archivo)

def cargar_datos():
    """Carga los datos desde un archivo binario."""
    if os.path.exists("datos_clientes.pkl"):
        with open("datos_clientes.pkl", "rb") as archivo:
            global clientes_activos, clientes_inactivos
            clientes_activos, clientes_inactivos = pickle.load(archivo)

# --- Programa Principal ---

# Inicializa listas
clientes_activos = []
clientes_inactivos = []

# Carga datos guardados

## .pem opcional
cargar_datos()

# Menú principal
while True:
    mostrar_opciones()
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        registrar_cliente()
    elif opcion == "2":
        mostrar_clientes(clientes_activos)
    elif opcion == "3":
        administrar_membresias()
    elif opcion == "4":
        guardar_datos()
        print("Datos guardados. Saliendo del sistema...")
        break
    else:
        print("Opción no válida. Inténtalo de nuevo.")
