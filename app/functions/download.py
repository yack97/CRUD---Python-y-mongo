# app/functions/download.py
import pandas as pd
from flask import make_response
from io import BytesIO

def handle_download(documents):
    # Convertir los documentos en un DataFrame de Pandas
    df = pd.DataFrame(documents)

    # Excluir el campo '_id'
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # Crear un objeto BytesIO para almacenar el archivo Excel en memoria
    output = BytesIO()
    
    # Crear un ExcelWriter usando openpyxl
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Dividir los documentos en bloques de 9000 filas
        for i in range(0, len(df), 9000):
            df_chunk = df.iloc[i:i + 9000]  # Obtener un bloque de 9000 filas
            sheet_name = f'Sheet{i // 9000 + 1}'  # Nombre de la hoja
            df_chunk.to_excel(writer, index=False, sheet_name=sheet_name)

    # Obtener el contenido del archivo Excel y preparar la respuesta
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=collection.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response