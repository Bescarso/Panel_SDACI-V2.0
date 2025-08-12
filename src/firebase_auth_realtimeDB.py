import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
auth_domain = os.getenv('AUTH_DOMAIN')
project_id = os.getenv('PROJECT_ID')
storage_bucket = os.getenv('STORAGE_BUCKET')
messaging_sender_id = os.getenv('MESSAGING_SENDER_ID')
app_id = os.getenv('APP_ID')
measurement_id = os.getenv('MEASUREMENT_ID')
database_url = os.getenv('DATABASE_URL')


# Firebase setup to connect to the Realtime Database
firebase_config = {
    'apiKey': api_key,
    'authDomain': auth_domain,
    'projectId': project_id,
    'storageBucket': storage_bucket,
    'messagingSenderId': messaging_sender_id,
    'appId': app_id,
    'measurementId': measurement_id,
    "databaseURL": database_url
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

def login_access (email, password):
    access_confirm = False
    try:
        # Autenticar usuario
        user = auth.sign_in_with_email_and_password(email, password)
        if user.get("registered"):
            print("El usuario/contraseña es correcto.")
            access_confirm = True
            return access_confirm

    except Exception as e:

        print('Fail authtentication')
        print(f"Error: {e}")


def update_db (category, device_name, new_quantity):
    try: 
        new_quantity = int(new_quantity)

        db.child(category).child(device_name).update({'Cantidad':new_quantity})

    except Exception as e:
        print(f"Error al leer la base de datos: {str(e)}")
        return []
    

def read_db(category=None):
    if category:
        category = category.capitalize()

    try:
        if category is None:
            values = db.get()
            data = [value.key() for value in values.each()] if values.each() else []
           
            return data
        
        elif category in ['Equipos', 'Herramientas', 'Insumos']:
            values = db.child(category).get()
            data_name = [value.key() for value in values.each()] if values.each() else []
            data_property = [value.val() for value in values.each()] if values.each() else []

            #print(data_name + data_property)
            return data_name, data_property

        else:
            #print(f'No existe la categoría "{category}" en la base de datos.')
            return []

    except Exception as e:
        print(f"Error al leer la base de datos: {str(e)}")
        return []


def get_category(devices_to_find: list) -> str:
    dict_categories = {}

    categories = db.get()  # Obtengo las categorías
  
    # Inicializamos el diccionario con listas vacías para cada categoría
    for category in categories.each():
        dict_categories[category.key()] = []  # Cada categoría tendrá su lista de dispositivos

    # Iteramos sobre las categorías para obtener sus dispositivos
    for category in categories.each():
        # Obtener los dispositivos específicos de la categoría actual
        devices = db.child(category.key()).get()  
        
        if devices.each():  # Verificar si hay dispositivos en la categoría
            for device in devices.each():
                dict_categories[category.key()].append(device.key())  # Agregar el dispositivo a la lista correspondiente


    # Buscar el grupo al que pertenece cada dispositivo en la lista `devices_to_find`
    result = {}
    for device in devices_to_find:
        found = False
        for category, device_list in dict_categories.items():
            if device in device_list:  # Si el dispositivo está en la lista de esta categoría
                result[device] = category  # Asignar la categoría al dispositivo
                found = True
                break
        if not found:  # Si el dispositivo no se encuentra en ninguna categoría
            result[device] = "No encontrado"

    return result


def read_db_sdaci(category: str = 'SDACI', address: str = None) -> dict:
    values = db.child(category).get()

    address_value = [value.key() for value in values.each()] if values.each() else []
    address_information = [value.val() for value in values.each()] if values.each() else []

    try:
        if address in address_value:
            idx = address_value.index(address)

            info = address_information[idx]

            return info
        else:
            print('Dirección no encontrada')
            return None
        
    except Exception as e:
        print(f"Error: {e}")

