import pymysql
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

# Cargar variables de entorno
load_dotenv()

# Conexión a MySQL
conexion_mysql = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DB")
)

# Creación de un objeto de cursor
cursor = conexion_mysql.cursor(pymysql.cursors.DictCursor)

# Consultas a MySQL y obtención de datos
cursor.execute("SELECT EmpresaID, NombreEmpresa FROM Empresas")
lista_empresas = cursor.fetchall()

cursor.execute("SELECT EstacionID, EmpresaID, Provincia, Municipio, Localidad, CodigoPostal, Direccion, Latitud, Longitud, FechaActualizacion, Margen, Horario, Tipo FROM Estaciones")
lista_estaciones = cursor.fetchall()

# Convertir datos a float
for estacion in lista_estaciones:
    estacion['Latitud'] = float(estacion['Latitud']) if estacion['Latitud'] is not None else None # Si no hay latitud, se guarda como None
    estacion['Longitud'] = float(estacion['Longitud']) if estacion['Longitud'] is not None else None # Si no hay longitud, se guarda como None

cursor.execute("SELECT precioId, estacionID, tipoCombustible, precio, fechaActualizacion FROM PreciosCombustible")
lista_precios_combustible = cursor.fetchall()

# Convertir datos a float
for precio in lista_precios_combustible:
    precio['precio'] = float(precio['precio']) if precio['precio'] is not None else None

conexion_mysql.close()

# Conexión a MongoDB
uri_mongo = os.getenv("MONGO_URI")
cliente_mongo = pymongo.MongoClient(uri_mongo, tls=True, tlsAllowInvalidCertificates=True)
db = cliente_mongo["bbdda"]

# Crear colecciones
coleccion_empresas = db["Empresas"]
coleccion_estaciones = db["Estaciones"]
coleccion_precios_combustible = db["PreciosCombustible"]

# Insertar datos en MongoDB
resultado_empresas = coleccion_empresas.insert_many(lista_empresas)
resultado_estaciones = coleccion_estaciones.insert_many(lista_estaciones)
resultado_precios_combustible = coleccion_precios_combustible.insert_many(lista_precios_combustible)