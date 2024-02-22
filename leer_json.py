from luces_json import Luces
import json

def leer_json():
    nombre_archivo = 'luces.json'
    try:
        with open(nombre_archivo, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {nombre_archivo}.")
        return None

def cargar_luces_desde_json():
    try:
        data = leer_json()
        luces = Luces(data.get('encender'), data.get('apagar'))
        return luces
    except json.JSONDecodeError:
        print("Error al decodificar el JSON.")
        return None
