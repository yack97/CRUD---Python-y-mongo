# app/functions/update.py
from pymongo import MongoClient, UpdateOne
import pandas as pd

def handle_update(selected_db_name, selected_collection_name, update_file, uri):
    # Conectar a MongoDB
    client = MongoClient(uri)
    
    # Seleccionar la base de datos y la colección
    selected_db = client[selected_db_name]
    selected_collection = selected_db[selected_collection_name]

    # Leer el archivo de Excel
    df = pd.read_excel(update_file)

    # Verificar si el DataFrame tiene al menos una columna
    if df.empty or df.shape[1] == 0:
        return "El archivo está vacío o no contiene columnas."

    # Tomar el nombre de la primera columna como el campo ID
    id_field_name = df.columns[0]

    # Convertir DataFrame a diccionarios
    documents = df.to_dict(orient='records')

    # Preparar operaciones de actualización usando la primera columna como ID
    operations = []
    for document in documents:
        doc_id = document[id_field_name]  # Usar el nombre de la primera columna como ID
        operations.append(UpdateOne({id_field_name: doc_id}, {'$set': document}, upsert=True))

    # Ejecutar las operaciones de actualización si hay alguna
    if operations:
        selected_collection.bulk_write(operations)
        return f"{len(operations)} documentos han sido insertados o actualizados."
    else:
        return "No hay documentos para actualizar o insertar."