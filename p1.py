
import threading
import concurrent.futures
import time
import socketio
import sys
import luces_sockets
sio = socketio.Client()

# Theared para terminar los programas
thread_programa = False
thread_programa_por_tiempo = False
# La respuesta de cada socket
request_programa = {}
request_programa_por_tiempo = {}
# Obtener el primer argumento que sera el lugar donde estara la nuc
t_programa = None
t_programa_por_tiempo = None
# Example: Correr programa python3 luces.py lugar
lugar = 'garaje'
if len(sys.argv) > 1:
    lugar = sys.argv[1]
    print("El valor del parámetro es:", lugar)

# Ejecutar el programa
def ejecutar_programa():
    global thread_programa
    global request_programa
    print("Ejecutar programa")
    while thread_programa:
        print("Programa ejecutandose")
        luces_sockets.init_luces(request_programa)
        time.sleep(1)

# Ejecutar el programa
def ejecutar_programa_por_tiempo():
    global thread_programa_por_tiempo
    global request_programa_por_tiempo
    print("Ejecutar programa por tiempo")
    while thread_programa_por_tiempo:
        print("Programa por tiempo")
        luces_sockets.programa_por_tiempo(request_programa_por_tiempo)
        time.sleep(1)

# Función para programar la ejecución del programa después de 10 segundos
def programa_ejecucion(request):
    global thread_programa
    global thread_programa_por_tiempo
    global request_programa
    global t_programa
    request_programa = request
    if not thread_programa_por_tiempo:
        if not thread_programa:
            luces_sockets.off_all_channels()
            thread_programa = True
            t_programa = iniciar_programa(ejecutar_programa)
            print("Peiridankjdnjn")
        else:
            t_programa.cancel()
            luces_sockets.off_all_channels()
            thread_programa = True
            t_programa = iniciar_programa(ejecutar_programa)
    
# Función para programar la ejecución del programa después de 10 segundos
def programa_por_tiempo_ejecucion(request):
    global thread_programa_por_tiempo
    global thread_programa
    global request_programa_por_tiempo
    global t_programa
    global t_programa_por_tiempo
    request_programa_por_tiempo = request
    if thread_programa:
         t_programa.cancel()
    # Ejecutamos el programa en el tiempo especifico   
    if not thread_programa_por_tiempo:
        luces_sockets.off_all_channels()
        t_programa_por_tiempo = iniciar_programa(ejecutar_programa_por_tiempo)
        time.sleep(request.get('time'))
        t_programa_por_tiempo.cancel()
        luces_sockets.off_all_channels()
        t_programa = iniciar_programa(ejecutar_programa)
   
# Función para iniciar el programa
def iniciar_programa(funcion):
    print("Iniciando programa...")
    # Iniciar el programa utilizando el executor
    theared = concurrent.futures.ThreadPoolExecutor().submit(funcion)
    return theared

# Iniciar los hilos con programa por tiempo, y programa
# t_programa = threading.Thread(target=ejecutar_programa)
# Iniciar el programa utilizando el executor
# t_programa = iniciar_programa(ejecutar_programa)
# t_programa_por_tiempo = threading.Thread(target=ejecutar_programa_por_tiempo)
# Iniciar el programa utilizando el executor
# t_programa_por_tiempo = iniciar_programa(ejecutar_programa_por_tiempo)

# Funcion de los sockets
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
    # Iniciar los sockets
    sio.connect('http://192.168.1.136:3005')
    sio.wait()