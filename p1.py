
import threading
import time
import socketio
import sys
import luces_sockets
sio = socketio.Client()

thread_programa = True
thread_programa_por_tiempo = True
# Obtener el primer argumento que sera el lugar donde estara la nuc
# Example: Correr programa python3 luces.py lugar
lugar = 'garaje'
if len(sys.argv) > 1:
    lugar = sys.argv[1]
    print("El valor del parámetro es:", lugar)

# Ejecutar el programa
def ejecutar_programa(res):
    global thread_programa
    while thread_programa:
        luces_sockets.init_luces(res)
        time.sleep(2)

# Función para programar la ejecución del programa después de 10 segundos
def programa_ejecucion(res):
    global thread_programa
    thread_programa = True
    # Apagar las luces
    luces_sockets.luces_encendidas = False
    t = threading.Thread(target=ejecutar_programa(res))
    t.start()
    thread_programa = t


# Ejecutar el programa
def ejecutar_programa_por_tiempo(res):
    global thread_programa_por_tiempo
    print("Ejecutar programa por tiempo")
    while thread_programa_por_tiempo:
        luces_sockets.programa_por_tiempo(res)

# Función para programar la ejecución del programa después de 10 segundos
def programa_por_tiempo_ejecucion(res):
    global thread_programa
    global thread_programa_por_tiempo
    thread_programa = False
    # Apagar las luces
    luces_sockets.off_all_channels()
    thread_programa_por_tiempo = True
    t = threading.Thread(target=ejecutar_programa_por_tiempo(res))
    t.start()
    time.sleep(res.get('time'))
    thread_programa_por_tiempo = False

@sio.event
def connect():
    print('connection established')

@sio.on('programa' + lugar)
def programa(data):
    programa_ejecucion(data)

@sio.on('programa_por_tiempo' + lugar)
def programa_por_tiempo(data):
    ejecutar_programa_por_tiempo(data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://192.168.1.136:3005')
sio.wait()