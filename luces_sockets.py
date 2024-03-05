from datetime import datetime, timedelta
import time 
import requests
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom
from fixture_model import FixtureModel
from leer_json import cargar_luces_desde_json
from luces_json import Luces
import sys
# Cargar luces desde JSON
# ------------------ Todo el codigo de las luces ------------------
dmx = OpenDMXController()
# Big square fixture model
bsq_fixture_model = FixtureModel("DRGBWSEP")
custom_fixture = dmx.add_fixture(Custom,name="CustomFixture", start_channel=1, channels=500)
bsq_fixture_model.setup_fixture(custom_fixture)

guardar_configuracion_luces = None
luces_encendidas = False
def encender_luz(channel):
    custom_fixture.dim(255, 0, channel - 1)
def encender_con_value_luz(value, channel):
    custom_fixture.dim(value, 0, channel - 1)
def apagar_luz(channel):
    custom_fixture.dim(0, 0, channel - 1)
def off_all_channels():
    print("Apgar todos los canales s")
    for i in range(500):
        custom_fixture.dim(0, 0, i)
def ciclo_luces(luces):
    for channel in luces:
        if isinstance(channel, list):
            encender_con_value_luz(channel[1], channel[0])
        else:
            encender_luz(channel)
# ------------------ Aqui termina el codigo ------------------
# ------------------ Codigo para la programacion de las luces en horas ------------------
        
# Programa para ejecutar el programa por tiempo
def programa_por_tiempo(data):
    global guardar_configuracion_luces
    luces = Luces(data.get('encender'), data.get('apagar'))
    if isinstance(guardar_configuracion_luces, Luces): 
        if luces.encender == guardar_configuracion_luces.encender:
            return None
    else:
        guardar_configuracion_luces = luces
    ciclo_luces(luces.encender)

# Función que comprueba si la hora actual está dentro del rango especificado
def verificar_hora(hora_inicio, hora_fin):
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()

    # Convertir la hora específica a un objeto datetime
    fecha_hora_inicio = datetime.strptime(hora_inicio, "%H:%M:%S")
    fecha_hora_fin = datetime.strptime(hora_fin, "%H:%M:%S")

    # Asignar una hora específica (por ejemplo, 15:30:00)
    fecha_inicio = fecha_hora_inicio.replace(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    fecha_fin = fecha_hora_fin.replace(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    
    # Esto es para que no se apage un minuto y se vuelva a encender
    if fecha_actual.hour == 23 and fecha_actual.minute == 59:
        return True
    if fecha_inicio <= fecha_actual <= fecha_fin: 
        return True
    return False

    
def verificar_horarios(horarios):
    if isinstance(horarios, list):
        for horario in horarios:
            if verificar_hora(horario.get('horario_inicio'), horario.get('horario_fin')):
                print("Esta en el horario") 
                return True
        return False
# ------------------ Termina la programacion de las luces en horas ------------------

def get_light_state_from_api(data, lugar):
    global guardar_configuracion_luces
    global luces_encendidas
    # try:

    #     # Obtener el primer argumento de la línea de comandos
    #     parametro = 'ermita'
    #     if len(sys.argv) > 1:
    #         parametro = sys.argv[1]
    #         print("El valor del parámetro es:", parametro)

    #     response = requests.get(f"https://api.conectateriolobos.es/luces/{parametro}")
    # except requests.exceptions.ConnectionError:
    #     return None

    # # If there is no command, return None
    # if response.status_code != 200:
    #     return None
    
    # Datos de la api
    # data = response.json()

    # Existe el cliente
    # if data.get('cliente') != None:
    #     luces = Luces(data.get('encender'), [])
    #     print("Si existe")
    #     time.sleep(60)

    # Encender las luces
    # if isinstance(guardar_configuracion_luces, Luces): 
        # if luces.encender != guardar_configuracion_luces.encender:
    # luces_encendidas = False 
            # guardar_configuracion_luces = luces
    # else:
        # guardar_configuracion_luces = luces
    
    # Verificar el horario para encender las luces o apagarlas
    if verificar_horarios(data.get('horarios')):
        if not luces_encendidas:
            off_all_channels()
        luces_encendidas = True 
    else:
        if luces_encendidas:
            luces_encendidas = False
            off_all_channels()
        return None
    
    # Guardar las luces
    luces = Luces(data.get('encender'), lugar)
    return luces

#Iniciar el programa
def init_luces(response, lugar):
    luces = get_light_state_from_api(response)
    if luces != None:  
        ciclo_luces(luces.encender)
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