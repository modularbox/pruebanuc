
import threading
import time
import socketio
import sys
import luces_sockets
sio = socketio.Client()

thread_programa = False
request_programa = {}
thread_programa_por_tiempo = False
request_programa_por_tiempo = {}
# Obtener el primer argumento que sera el lugar donde estara la nuc
# Example: Correr programa python3 luces.py lugar
lugar = 'garaje'
if len(sys.argv) > 1:
    lugar = sys.argv[1]
    print("El valor del parámetro es:", lugar)

# Función para programar la ejecución del programa después de 10 segundos
def programa_ejecucion(request):
    global thread_programa
    global thread_programa_por_tiempo
    global request_programa
    request_programa = request
    if not thread_programa_por_tiempo:
        if not thread_programa:
            luces_sockets.off_all_channels()
            thread_programa = True
    
# Función para programar la ejecución del programa después de 10 segundos
def programa_por_tiempo_ejecucion(request):
    global thread_programa_por_tiempo
    global request_programa_por_tiempo
    request_programa_por_tiempo = request
    if thread_programa:
        thread_programa = False
    # Ejecutamos el programa en el tiempo especifico   
    if not thread_programa_por_tiempo:
        luces_sockets.off_all_channels()
        thread_programa_por_tiempo = True
        time.sleep(request.get('time'))
        thread_programa_por_tiempo = False
        luces_sockets.off_all_channels()
        thread_programa = True
    
# Ejecutar el programa
def ejecutar_programa():
    global thread_programa
    global request_programa
    print("Ejecutar programa")
    while thread_programa:
        print("Programa ejecutandose")
        luces_sockets.init_luces(request_programa)
        time.sleep(2)

# Ejecutar el programa
def ejecutar_programa_por_tiempo():
    global thread_programa_por_tiempo
    global request_programa_por_tiempo
    print("Ejecutar programa por tiempo")
    while thread_programa_por_tiempo:
        luces_sockets.programa_por_tiempo(request_programa_por_tiempo)
        time.sleep(2)

@sio.event
def connect():
    print('connection established')

@sio.on('programa' + lugar)
def programa(data):
    programa_ejecucion(data)

@sio.on('programa_por_tiempo' + lugar)
def programa_por_tiempo(data):
    programa_por_tiempo_ejecucion(data)

@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == "__main__":
    # Iniciar los hilos con programa por tiempo, y programa
    t_programa = threading.Thread(target=ejecutar_programa())
    t_programa.start()
    t_programa_por_tiempo = threading.Thread(target=ejecutar_programa_por_tiempo())
    t_programa_por_tiempo.start()

    # Iniciar los sockets
    sio.connect('http://192.168.1.136:3005')
    sio.wait()