# Bases de datos Avanzadas - Actividad grupal

## Descripción
Este proyecto consiste en la implementación de un sistema de gestión de bases de datos que involucra la transferencia de datos desde MySQL a MongoDB utilizando Python.

## Características
- **MySQL**: Utilizado para almacenar y gestionar datos estructurados.
- **MongoDB**: Base de datos NoSQL elegida para facilitar consultas dinámicas y almacenamiento de datos no estructurados.
- **Python**: Lenguaje de programación utilizado para la manipulación de datos y conexión entre MySQL y MongoDB.

## Proceso ETL
1. **Extracción de Datos**: Los datos se extraen de MySQL, donde se almacenan datos de empresas, estaciones y precios de combustibles.
2. **Transformación**: Los datos se transforman a un formato adecuado para su inserción en MongoDB, convirtiendo tipos de datos como `decimal.Decimal` a `float`.
3. **Carga en MongoDB**: Los datos transformados se cargan en MongoDB para su análisis y acceso rápido.

## Seguridad
Las credenciales y URIs sensibles se manejan mediante variables de entorno para mejorar la seguridad y la gestión de configuraciones.

## Requisitos
- Python 3.x
- PyMySQL
- PyMongo
- Biblioteca `dotenv` para la gestión de variables de entorno

## Instalación y Ejecución

1. **Clonar el Repositorio**:
   Clona este repositorio a tu máquina local utilizando `git clone [url-del-repositorio]`.

2. **Instalar Dependencias**:
   Antes de ejecutar el script, instala las dependencias necesarias. Si no tienes un archivo `requirements.txt`, puedes crear uno incluyendo las bibliotecas necesarias como `pymysql`, `pymongo`, `python-dotenv`, etc. Luego, ejecuta `pip install -r requirements.txt` para instalarlas.

3. **Configurar Variables de Entorno**:
   Crea un archivo `.env` en la raíz del proyecto y establece tus variables de entorno allí.

4. **Ejecutar el Script**:
   Una vez configurado, ejecuta el script principal con `python main.py` para realizar la transferencia de datos.


## Autores
- `Francisca Illanes`: [frana00] - https://github.com/frana00
- `Daniel Prol`: [dprol] - https://github.com/dprol
- `Daniela Díaz`: [dasniela] - https://github.com/dasniela
- `Daniela González`: [fraychella] - https://github.com/fraychella
- `Alejandro Cano`: [aknodr] - https://github.com/aknodr
