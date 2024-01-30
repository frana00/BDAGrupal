import os
import pymongo
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
