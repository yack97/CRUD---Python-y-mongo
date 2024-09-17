# app/routes.py
from flask import render_template, request, send_file, abort, redirect, url_for
from .functions.mongodb import connect_to_mongodb, handle_database_selection, handle_collection_selection
from .functions.download import handle_download
from .functions.update import handle_update
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    client, databases, collections, selected_db_name, selected_collection_name, collection_info, collection_preview = initialize_context()

    if request.method == 'POST':
        uri = request.form.get('uri')  # Obtener la URI del formulario
        if uri:
            # Conectarse a MongoDB usando la URI proporcionada
            client, databases = connect_to_mongodb(uri)
            selected_db_name, collections = handle_database_selection(client)

            if selected_db_name:
                # Obtener la colección seleccionada
                selected_collection_name, collection_info, collection_preview, documents = handle_collection_selection(client, selected_db_name)

                # Comprobamos si el usuario solicitó la descarga de la colección
                if request.form.get('download') == 'excel':
                    if documents:
                        return handle_download(documents)
                    else:
                        abort(404, description="No se encontraron documentos para descargar")

                # Opción para actualizar la colección
                if 'update' in request.form:
                    update_file = request.files.get('update_file')  # Obtener el archivo para la actualización
                    if update_file:
                        return handle_update(selected_db_name, selected_collection_name, update_file, uri)
                    else:
                        abort(400, description="No se proporcionó un archivo válido para la actualización.")

                # Opción para desconectar
                if 'disconnect' in request.form:
                    # Limpiar las variables de contexto y redirigir
                    return redirect(url_for('main.index'))

                # Opción para refrescar información
                if 'refresh' in request.form:
                    return redirect(url_for('main.index'))

    # Si no hay petición POST, o si no se encuentra nada, se renderiza el formulario
    return render_template(
        'form.html',
        databases=databases,
        collections=collections,
        selected_db_name=selected_db_name,
        selected_collection_name=selected_collection_name,
        collection_info=collection_info,
        collection_preview=collection_preview,
        uri=request.form.get('uri')  # Para mantener la URI en el formulario
    )

def initialize_context():
    """
    Inicializar las variables en None para evitar errores si no hay información disponible.
    """
    return None, None, None, None, None, None, None