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

guardar_configuracion_luces = None

def encender_luz(channel):
    custom_fixture.dim(255, 0, channel - 1)
def apagar_luz(channel):
    custom_fixture.dim(0, 0, channel - 1)

def off_all_channels():
    for i in range(500):
        custom_fixture.dim(255, 0, i)
    

def ciclo_luces(luces):
    for channel in luces:
        encender_luz(channel)

def get_light_state_from_api():
    global guardar_configuracion_luces
    try:
        response = requests.get("https://api.conectateriolobos.es/luces/ermita")
    except requests.exceptions.ConnectionError:
        return None

    # If there is no command, return None
    if response.status_code != 200:
        return None
    # Datos de la api
    data = response.json()
    print(data)
    luces = Luces(data.get('encender'), data.get('apagar'))
    if isinstance(guardar_configuracion_luces, Luces): 
        if luces.encender == guardar_configuracion_luces.encender:
            print("Es igual")
            return None
        else:
            print("ApagarLuces")
            off_all_channels()
    else:
        guardar_configuracion_luces = luces
    return luces

while True:
    luces = get_light_state_from_api()
    print(luces)
    if luces != None: 
        ciclo_luces(luces.encender)

    time.sleep(4)
print("LucesTermino")
"""
 FT232R USB UART:

                  Product ID: 0x6001
                  Vendor ID: 0x0403  (Future Technology Devices International Limited)
                  Version: 6.00
                  Serial Number: AL0409WG
                  Speed: Up to 12 Mb/s
                  Manufacturer: FTDI
                  Location ID: 0x00113000 / 6
                  Current Available (mA): 500
                  Current Required (mA): 90
                  Extra Operating Current (mA): 0
"""