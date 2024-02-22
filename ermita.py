import time 
import requests
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom
from fixture_model import FixtureModel
from leer_json import cargar_luces_desde_json
from luces_json import Luces
# Cargar luces desde JSON
# luces = cargar_luces_desde_json()

# Ejemplo de uso
# if luces is not None:
#     print("Encender:", luces.encender)
#     print("Apagar:", luces.apagar)
# else:
#     print("No se pudieron cargar las luces desde el JSON.")

dmx = OpenDMXController()
# Big square fixture model
bsq_fixture_model = FixtureModel("DRGBWSEP")
custom_fixture = dmx.add_fixture(Custom,name="CustomFixture", start_channel=1, channels=500)
bsq_fixture_model.setup_fixture(custom_fixture)

guardar_luces_encendidas = None

def encender_luz(channel):
    custom_fixture.dim(255, 0, channel - 1)
def apagar_luz(channel):
    custom_fixture.dim(0, 0, channel - 1)

def ciclo_luces(luces):
    for channel in luces:
        encender_luz(channel)

def get_light_state_from_api():
    global guardar_configuracion
    try:
        response = requests.get("https://api.conectateriolobos.es/luces/ermita")
    except requests.exceptions.ConnectionError:
        return None

    # Datos de la api
    data = response.json()
    # If there is no command, return None
    if response.status_code != 200:
        return None
    if guardar_configuracion == None:
        guardar_configuracion = data
    else:
        if data == guardar_configuracion:
            print("Es igual")
            return None
    
    # def setChannelsFromColour(color):
    #     focos_encendidos = None
    #     colores = {
    #         'red': [1, 6, 11, 16],
    #         'green': [2, 7, 12, 17],
    #         'blue': [3, 8, 13, 18],
    #         'yellow': [1, 2, 6, 7, 11, 12, 16, 17],
    #         'orange': [1, [2, 170], 6, [7, 170], 11, [12, 170], 16, [17, 170] ],
    #         'purple': [[1, 170], 3, [6, 170], 8, [11, 170], 13, [16, 170], 18],
            
    #     }
    #     if color == 'red':
    #         focos_encendidos = colores['red']
    #     elif color == 'green':
    #         focos_encendidos = colores['green']
    #     elif color == 'blue':
    #         focos_encendidos = colores['blue']
    #     elif color == 'yellow':
    #         focos_encendidos = colores['yellow']
    #     elif color == 'orange':
    #         focos_encendidos = colores['orange']
    #     elif color == 'purple':
    #         focos_encendidos = colores['purple']
        
    #     return focos_encendidos
    # If there is a command, return it
    print(response)
    print(response.json())
    luces = Luces(data.get('encender'), data.get('apagar'))
    return luces

while True:
    luces = get_light_state_from_api()
    print(luces)
    if luces != None: 
        ciclo_luces(luces.encender)

    time.sleep(4)
    