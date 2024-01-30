import pymysql
import pymongo
import os
from dotenv import load_dotenv
from pymongo import UpdateOne

# Función para dividir una lista en lotes
def dividir_en_lotes(lista, tamano_lote):
    for i in range(0, len(lista), tamano_lote):
        yield lista[i:i + tamano_lote]

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

# Empresas
tamano_lote = 5000
contador = 0
for lote_empresas in dividir_en_lotes(lista_empresas, tamano_lote):
    operaciones = [UpdateOne({"EmpresaID": empresa["EmpresaID"]}, {"$set": empresa}, upsert=True) for empresa in lote_empresas]
    coleccion_empresas.bulk_write(operaciones)
    contador += len(lote_empresas)
    print(f"Empresas procesadas: {contador} de {len(lista_empresas)}")

# Estaciones
contador = 0
for lote_estaciones in dividir_en_lotes(lista_estaciones, tamano_lote):
    operaciones = [UpdateOne({"EstacionID": estacion["EstacionID"]}, {"$set": estacion}, upsert=True) for estacion in lote_estaciones]
    coleccion_estaciones.bulk_write(operaciones)
    contador += len(lote_estaciones)
    print(f"Estaciones procesadas: {contador} de {len(lista_estaciones)}")

# Precios Combustible
contador = 0
for lote_precios in dividir_en_lotes(lista_precios_combustible, tamano_lote):
    operaciones = [UpdateOne({"precioId": precio["precioId"]}, {"$set": precio}, upsert=True) for precio in lote_precios]
    coleccion_precios_combustible.bulk_write(operaciones)
    contador += len(lote_precios)
    print(f"Precios procesados: {contador} de {len(lista_precios_combustible)}")

cliente_mongo.close()