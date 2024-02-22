import time 
import requests
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom
from fixture_model import FixtureModel
from leer_json import cargar_luces_desde_json
from luces_json import Luces
import sys
# Cargar luces desde JSON
# luces = cargar_luces_desde_json()

# Ejemplo de uso
# if luces is not None:
#     print("Encender:", luces.encender)
#     print("Apagar:", luces.apagar)
# else:
#     print("No se pudieron cargar las luces desde el JSON.")

# ------------------ Todo el codigo de las luces ------------------
dmx = OpenDMXController()
# Big square fixture model
bsq_fixture_model = FixtureModel("DRGBWSEP")
custom_fixture = dmx.add_fixture(Custom,name="CustomFixture", start_channel=1, channels=500)
bsq_fixture_model.setup_fixture(custom_fixture)

guardar_configuracion_luces = None
luces_encendidas = True
def encender_luz(channel):
    custom_fixture.dim(255, 0, channel - 1)
def apagar_luz(channel):
    custom_fixture.dim(0, 0, channel - 1)
def off_all_channels():
    for i in range(500):
        custom_fixture.dim(0, 0, i)
def ciclo_luces(luces):
    for channel in luces:
        encender_luz(channel)
# ------------------ Aqui termina el codigo ------------------
# ------------------ Codigo para la programacion de las luces en horas ------------------
        
# Función que comprueba si la hora actual está dentro del rango especificado
def verificar_hora(hora_inicio, hora_fin, min_inicio, min_fin):
    hora_actual = time.localtime().tm_hour
    min_actual = time.localtime().tm_min
    print(f"HoraActual: {hora_actual}, MinutoActual: {min_actual}, -  Hora inicio: {hora_inicio}, Minuto inicio: {min_inicio}, - Hora fin: {hora_fin}, Minuto fin: {min_fin}")
    if hora_inicio <= hora_actual <= hora_fin: 
        return min_inicio <= min_actual <= min_fin
    
def verificar_horarios(horarios):
    if isinstance(horarios, list):
        for horario in horarios:
            if verificar_hora(horario.get('hora_inicio'), horario.get('hora_fin'), horario.get('min_inicio'), horario.get('min_fin')):
                print("Esta en el horario") 
                return True
        return False
# ------------------ Termina la programacion de las luces en horas ------------------

def get_light_state_from_api():
    global guardar_configuracion_luces
    global luces_encendidas
    try:

        # Obtener el primer argumento de la línea de comandos
        parametro = 'ermita'
        if len(sys.argv) > 1:
            parametro = sys.argv[1]
            print("El valor del parámetro es:", parametro)

        response = requests.get(f"https://api.conectateriolobos.es/luces/{parametro}")
    except requests.exceptions.ConnectionError:
        return None

    # If there is no command, return None
    if response.status_code != 200:
        return None
    
    # Datos de la api
    data = response.json()
    # Verificar el horario para encender las luces o apagarlas

    if verificar_horarios(data.get('horarios')):
        luces_encendidas = True
    else:
        if luces_encendidas:
            luces_encendidas = False
            guardar_configuracion_luces = None
            print("ApagarLuces")
            off_all_channels()
        return None
        
    # Encender las luces
    luces = Luces(data.get('encender'), data.get('apagar'))
    if isinstance(guardar_configuracion_luces, Luces): 
        if luces.encender == guardar_configuracion_luces.encender:
            return None
        else:
            guardar_configuracion_luces = luces
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