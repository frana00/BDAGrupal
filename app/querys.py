import os
import pymongo

from app.main import db


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

# Imprime empresa con más estaciones de servicio Terrestres, solo 1 línea

def imprimir_empresa_con_mas_estaciones(db):
    while True:
        empresa = empresa_con_mas_estaciones(db)
        print(empresa)
        break

def imprimir_empresa_con_mas_estaciones(db):
    for empresa in empresa_con_mas_estaciones(db):
        print(empresa)

# Llamar a la función imprimir_empresa_con_mas_estaciones
imprimir_empresa_con_mas_estaciones(db)


