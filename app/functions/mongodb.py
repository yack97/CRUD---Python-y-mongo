# app/mongodb.py
from flask import request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

def connect_to_mongodb(uri):
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')  # Confirmar la conexión con un ping
        print("¡Conexión exitosa a MongoDB!")
        databases = client.list_database_names()
        return client, databases
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None, None

def handle_database_selection(client):
    selected_db_name = request.form.get('database')
    collections = []
    if selected_db_name:
        selected_db = client[selected_db_name]
        collections = selected_db.list_collection_names()
    return selected_db_name, collections

def handle_collection_selection(client, selected_db_name):
    selected_collection_name = request.form.get('collection')
    collection_info = None
    collection_preview = None
    documents = []

    if selected_collection_name:  # Verifica que se haya seleccionado una colección
        selected_db = client[selected_db_name]
        selected_collection = selected_db[selected_collection_name]

        try:
            # Obtén todos los documentos excluyendo el campo _id
            documents = list(selected_collection.find({}, {'_id': 0}))  # Excluimos el campo _id

            collection_info = {
                "total_documents": selected_collection.estimated_document_count(),
                "collection_name": selected_collection_name
            }

            if documents:
                # Convierte los documentos a un formato amigable para la vista previa
                collection_preview = pd.DataFrame(documents).to_dict(orient='records')

        except Exception as e:
            print(f"Error al obtener documentos de la colección {selected_collection_name}: {e}")

    return selected_collection_name, collection_info, collection_preview, documents