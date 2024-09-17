from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

def connect_to_mongodb(uri):
    try:
        # Crear el cliente de MongoDB
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')  # Confirmar la conexión con un ping
        print("¡Conexión exitosa a MongoDB!")

        # Listar todas las bases de datos disponibles
        databases = client.list_database_names()
        print("Bases de datos disponibles:", databases)

        # Solicitar al usuario que elija una base de datos
        selected_db_name = input("Escribe el nombre de la base de datos con la que deseas trabajar: ")

        if selected_db_name in databases:
            selected_db = client[selected_db_name]
            print(f"Conectado a la base de datos: {selected_db_name}")
            
            # Mostrar colecciones disponibles en la base de datos seleccionada
            collections = selected_db.list_collection_names()
            if collections:
                print(f"Colecciones disponibles en {selected_db_name}: {collections}")
                selected_collection_name = input("Escribe el nombre de la colección con la que deseas trabajar: ")
                
                if selected_collection_name in collections:
                    # Obtener la colección seleccionada
                    selected_collection = selected_db[selected_collection_name]
                    
                    # Recuperar todos los documentos de la colección
                    documents = list(selected_collection.find())

                    # Convertir los documentos a un DataFrame de pandas
                    df = pd.DataFrame(documents)

                    # Guardar el DataFrame en un archivo Excel
                    excel_file = f"{selected_collection_name}.xlsx"
                    df.to_excel(excel_file, index=False)
                    print(f"Datos exportados exitosamente a '{excel_file}'")
                else:
                    print(f"La colección '{selected_collection_name}' no existe.")
            else:
                print(f"No hay colecciones en la base de datos '{selected_db_name}'.")
        
        else:
            print(f"La base de datos '{selected_db_name}' no está disponible.")
        
    except Exception as e:
        print("Error al conectar a MongoDB:", e)


# Solicitar la URI de MongoDB
uri = input("Ingresa la URI de MongoDB: ")
connect_to_mongodb(uri)