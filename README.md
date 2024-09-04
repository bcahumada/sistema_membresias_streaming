# Sistema de Membresías para Streaming

Este repositorio contiene el código para un sistema de gestión de membresías para un servicio de streaming de películas y series chilenas. El código utiliza la herencia y el polimorfismo en Python para modelar diferentes tipos de membresías con sus características y comportamientos específicos.

* Como característica adicional se implementa un sistema de cifrado de datos sensibles que también permite guardar los datos ingresados de los clientes a pesar de salir del sistema. Cualdo vuelves a entrar los datos están disponibles *

## Tipos de Membresías:

* **Gratis:** Membresía básica con acceso limitado.
* **Básica:** Membresía con más funciones que la gratuita.
* **Familiar:** Membresía para varias personas en un hogar.
* **Sin Conexión:** Membresía para ver contenido sin conexión a internet.
* **Pro:** Membresía premium con acceso a todas las funciones.

## Características:

* **Registro de Clientes:** Permite registrar nuevos clientes con información personal (nombre completo, correo electrónico, número de tarjeta) y elegir un tipo de membresía.
* **Gestión de Membresías:** Permite cambiar de tipo de membresía, cancelar membresías y reactivar clientes.
* **Funciones Especiales:**  
    * Control Parental: (implementado para Familiar y Pro)
    * Contenido Sin Conexión: (implementado para Sin Conexión y Pro)
* **Interfaz de Consola:**  Proporciona un menú interactivo para gestionar las membresías.
* **Persistencia de Datos:** Guarda la información de los clientes en archivos cifrados con RSA al salir del programa, para que la información se mantenga entre ejecuciones.

## Estructura del Código:

* **membresia.py:** Define las clases de membresía y la lógica principal.
* **main_interfaz.py:** Define la interfaz de usuario en consola.
* **pruebas_unitarias.py:** Contiene pruebas para verificar que las clases funcionan correctamente.


## Cómo Ejecutar el Código:

1. **Clona el repositorio:** 
   ```bash
   git clone https://github.com/bcahumada/sistema-membresias-streaming


2. **Instala las dependencias:**
pip install cryptography
pip install bcrypt


3. **Uso:**

* Ejecuta el archivo `main_interfaz.py` para interactuar con el sistema de membresías a través de la consola.
* Ejecuta el archivo `pruebas_unitarias.py` para ejecutar pruebas unitarias que verifiquen la funcionalidad de las clases.

## Autor

Bárbara HA

**GitHub**: https://github.com/bcahumada

