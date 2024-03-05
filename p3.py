
import threading
import concurrent.futures
import time
import socketio
import sys
import luces_sockets
from enum import Enum

# Definir una enumeración simple
class Programas(Enum):
    PROGRAMA = 1
    PROGRAMA_POR_TIEMPO = 2

# Crea el evento
theared_program = threading.Event()

# Cliente de los sockets
sio = socketio.Client()

class TimedEventThread(threading.Thread):
    def __init__(self, interval, event, programa, programa_por_tiempo, request_programa=None, request_programa_por_tiempo=None):
        super().__init__()
        self.interval = interval
        self.stopped = event
        self.programa_execute = Programas.PROGRAMA
        self.programa = programa
        self.programa_por_tiempo = programa_por_tiempo
        self.request_programa = request_programa or {}
        self.request_programa_por_tiempo = request_programa_por_tiempo or {}

    def run(self):
        while not self.stopped.wait(self.interval):
            if self.programa_execute == Programas.PROGRAMA:
                self.programa(self.request_programa)
            if self.programa_execute == Programas.PROGRAMA_POR_TIEMPO:
                self.programa_por_tiempo(self.request_programa_por_tiempo)
            if self.programa_execute == Programas.NONE:
                print("No hay ningun Programa")
    
    def changePrograma(self, nuevo_programa):
        self.programa_execute = nuevo_programa

    def changeRequestPrograma(self, nuevo_request):
        self.request_programa = nuevo_request

    def changeRequestProgramaPorTiempo(self, nuevo_request):
        self.request_programa_por_tiempo = nuevo_request
        
# Función para iniciar el evento
def start_event(event_thread):
    if not event_thread.is_alive():
        event_thread.start()
        print("Evento iniciado")
    else:
        print("El evento ya está en ejecución")

# Example: Correr programa python3 luces.py lugar
lugar = 'garaje'
if len(sys.argv) > 1:
    lugar = sys.argv[1]
    print("El valor del parámetro es:", lugar)

# Ejecutar el programa
def ejecutar_programa(request):
    print("Programa ejecutandose")
    luces_sockets.init_luces(request)

# Ejecutar el programa
def ejecutar_programa_por_tiempo(request):
    print("Ejecutar programa por tiempo")
    luces_sockets.programa_por_tiempo(request)
    
# Función para programar la ejecución del programa después de 10 segundos
def programa_ejecucion(request):
    global theared
    theared.changeRequestPrograma(request)
    if theared.programa_execute != Programas.PROGRAMA_POR_TIEMPO:
        luces_sockets.off_all_channels()
        theared.changePrograma(Programas.PROGRAMA)
    
# Función para programar la ejecución del programa después de 10 segundos
def programa_por_tiempo_ejecucion(request):
    global theared
    theared.changeRequestProgramaPorTiempo(request)
    luces_sockets.guardar_configuracion_luces = None
    luces_sockets.off_all_channels()
    theared.changePrograma(Programas.PROGRAMA_POR_TIEMPO)
    time.sleep(request.get('time'))
    luces_sockets.off_all_channels()
    theared.changePrograma(Programas.PROGRAMA)

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
    # Crea el hilo para el evento
    theared = TimedEventThread(1, theared_program, ejecutar_programa, ejecutar_programa_por_tiempo)
    # Iniciar Evento
    start_event(theared)
    sio.wait()