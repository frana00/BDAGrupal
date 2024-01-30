import os
import pymongo
import pymysql
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Conexión a MySQL
def conectar_mysql():
    conexion_mysql = pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        db=os.getenv("MYSQL_DB")
    )
    return conexion_mysql

# Consultas a MySQL y obtención de datos
def empresa_mas_estaciones_terrestres_mysql():
    # Conectar a MySQL
    conexion = conectar_mysql()
    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    # Consulta SQL
    consulta_sql = """
    SELECT 
        e.NombreEmpresa, 
        COUNT(s.EstacionID) AS total_estaciones
    FROM 
        Estaciones AS s
    JOIN 
        Empresas AS e ON s.EmpresaID = e.EmpresaID
    WHERE 
        s.Tipo = 'Terrestre'
    GROUP BY 
        e.NombreEmpresa
    ORDER BY 
        total_estaciones DESC
    LIMIT 1;
    """
    

    # Ejecutar consulta
    cursor.execute(consulta_sql)
    resultado = cursor.fetchone()

    # Cerrar conexiones
    cursor.close()
    conexion.close()

    return resultado

# Conexión a MongoDB
def conectar_mongo(uri):
    uri_mongo = os.getenv("MONGO_URI")
    cliente_mongo = pymongo.MongoClient(uri_mongo, tls=True, tlsAllowInvalidCertificates=True)
    db = cliente_mongo["bbdda"]
    return db

# Empresa con más estaciones de servicio Terrestres, nombre de dicha empresa
def empresa_con_mas_estaciones(db):
    return db["Estaciones"].aggregate([
        {
            "$group": {
                "_id": "$EmpresaID",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 1
        },
        {
            "$lookup": {
                "from": "Empresas",
                "localField": "_id",
                "foreignField": "EmpresaID",
                "as": "empresa_info"
            }
        },
        {
            "$unwind": "$empresa_info"
        },
        {
            "$project": {
                "nombre_empresa": "$empresa_info.NombreEmpresa",
                "total_estaciones": "$count"
            }
        }
    ])

if __name__ == "__main__":
    # Conexión a MongoDB
    db_mongo = conectar_mongo(os.getenv("MONGO_URI"))
    resultado_mongo = empresa_con_mas_estaciones(db_mongo)

    # Conexión a MySQL
    resultado_mysql = empresa_mas_estaciones_terrestres_mysql()

    # Imprimir resultados
    print("Resultado de MongoDB:")
    for empresa in resultado_mongo:
        print(f"Nombre de la empresa: {empresa['nombre_empresa']}")


    print("\nResultado de MySQL:")
    if resultado_mysql:
        print(f"Nombre de la empresa: {resultado_mysql['NombreEmpresa']}")

    else:
        print("No se encontraron resultados en MySQL.")
