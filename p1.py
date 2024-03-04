
import threading
import time
import socketio
import sys
import luces_sockets
sio = socketio.Client()

thread_programa = None
# Obtener el primer argumento que sera el lugar donde estara la nuc
# Example: Correr programa python3 luces.py lugar
lugar = 'garaje'
if len(sys.argv) > 1:
    lugar = sys.argv[1]
    print("El valor del parámetro es:", lugar)
#
def ejecutar_programa(res):
    luces_sockets.init_luces(res)

# Función para programar la ejecución del programa después de 10 segundos
def programar_ejecucion(res):
    global thread_programa
    # Apagar las luces
    luces_sockets.luces_encendidas = False
    t = threading.Thread(target=ejecutar_programa(res))
    t.start()
    thread_programa = t

@sio.event
def connect():
    print('connection established')

@sio.on('programa' + lugar)
def programa(data):
    programar_ejecucion(data)

@sio.on('programa_por_tiempo' + lugar)
def programa_por_tiempo(data):
    # req: Es la informacion que recibe y es un json
    req = str(data).json()
    print('message received with ', req)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://192.168.1.136:3005')
sio.wait()