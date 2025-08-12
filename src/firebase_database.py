import firebase_admin
import sys
import os

from firebase_admin import credentials, firestore
from datetime import *
from dotenv import load_dotenv

load_dotenv()

#This credential is from FIREBASE DATABASE
crediantial_firebase = os.getenv('CRED_FIREBASE')


cred = credentials.Certificate(crediantial_firebase)
firebase_admin.initialize_app(cred)
if not firebase_admin._apps:
    firebase_admin.initialize_app()

fdb = firestore.client()


def get_packaged_files_path():
    """Location of relative paths """
    if getattr(sys, 'frozen', False):
        path = sys._MEIPASS  # pylint: disable=no-member
    else:
        path = '.'

    return path


def get_data_fdb():

    dict_document = {}

    # Obtener los documentos de la colección
    docs = fdb.collection('inventory_history').stream()

    for doc in docs:
        if doc.id == "0":  # Omitir el documento con ID "0"
            continue
        dict_document[doc.id] = doc.to_dict()

    # Imprimir cada documento con los datos requeridos
    for doc_id, data in dict_document.items():
        cantidad = data.get("cantidad", "N/A")
        descripcion = data.get("descripción", "N/A")
        equipo = data.get("equipo", "N/A")
        fecha = data.get("fecha", "N/A")
        justificacion = data.get("justificación", "N/A")


def get_maintenance_history(address: str = ''):
    address = address.upper()
    doc_ref = fdb.collection("sdaci").document(address)

    collections = doc_ref.collections()
    dictionary_maintenance = {
        "device_address": address  # Se guarda el nombre del documento
    }

    for collection in collections:
        collection_name = collection.id
        dictionary_maintenance[collection_name] = []

        for doc in collection.stream():
            dictionary_maintenance[collection_name].append({
                "id": doc.id,
                **doc.to_dict()
            })

    return dictionary_maintenance


def upload_history_maintenance(address: str = '',
                                type_maintenance: str = '',
                                date: datetime = None,
                                description: str = '',
                                action: str = ''):
    
    # Referencia a la subcolección de historial
    doc_ref = fdb.collection("sdaci").document(address.upper()).collection("maintenance_history")
    
    # Obtener todos los documentos existentes para contar el último número
    docs = doc_ref.stream()

    max_index = 0
    for doc in docs:
        try:
            doc_id = int(doc.id)
            if doc_id > max_index:
                max_index = doc_id
        except ValueError:
            continue  # Ignora IDs que no son números
    
    new_id = str(max_index + 1)

    data = {
        'type_maintenance': type_maintenance,
        'date': date,
        'description': description,
        'action': action
    }

    # Agregar el nuevo documento con ID numérico
    doc_ref.document(new_id).set(data)


def delete_data_maintenance (address: str = '', doc_id: str = ''):
    doc_ref = fdb.collection("sdaci").document(address.upper()).collection("maintenance_history").document(doc_id)
    doc_ref.delete()

