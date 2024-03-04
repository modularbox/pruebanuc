
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
    NONE = 3

# Crea el evento
theared_program = threading.Event()

sio = socketio.Client()

class TimedEventThread(threading.Thread):
    def __init__(self, interval, event, programa, programa_por_tiempo, request_programa=None, request_programa_por_tiempo=None):
        super().__init__()
        self.interval = interval
        self.stopped = event
        self.programa_execute = Programas.NONE
        self.programa = programa
        self.programa_por_tiempo = programa_por_tiempo
        self.request_programa = request_programa or []
        self.request_programa_por_tiempo = request_programa_por_tiempo or []

    def run(self):
        while not self.stopped.wait(self.interval):
            if self.programa_execute == Programas.PROGRAMA:
                self.programa(request_programa)
            if self.programa_execute == Programas.PROGRAMA_POR_TIEMPO:
                self.programa_por_tiempo(request_programa_por_tiempo)
            if self.programa_execute == Programas.NONE:
                print("No hay ningun Programa")
            # Coloca aquí el código del evento que deseas ejecutar
            print("Evento ejecutado")
    
    def changePrograma(self, nuevo_programa):
        self.programa_execute = nuevo_programa
        

# Función para iniciar el evento
def start_event(event_thread):
    if not event_thread.is_alive():
        event_thread.start()
        print("Evento iniciado")
    else:
        print("El evento ya está en ejecución")

# Función para detener el evento
def stop_event(event_thread, event):
    if event_thread.is_alive():
        event.set()  # Indica al hilo que se detenga
        event_thread.join()  # Espera a que el hilo termine
        print("Evento detenido")
    else:
        print("El evento no está en ejecución")

# if __name__ == "__main__":
#     # Crea el hilo para el evento
#     event_thread = TimedEventThread(5, stop_flag)

#     # Ejemplo de uso: iniciar y detener el evento
#     start_event(event_thread, stop_flag)
#     time.sleep(10)  # Simula un período de tiempo
#     stop_event(event_thread, stop_flag)

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
    # print("Ejecutar programa")
    # while thread_programa:
    print("Programa ejecutandose")
    luces_sockets.init_luces(request_programa)
        # time.sleep(1)

# Ejecutar el programa
def ejecutar_programa_por_tiempo():
    global thread_programa_por_tiempo
    global request_programa_por_tiempo
    print("Ejecutar programa por tiempo")
    # while thread_programa_por_tiempo:
    print("Programa por tiempo")
    luces_sockets.programa_por_tiempo(request_programa_por_tiempo)
    
    # time.sleep(1)

# Función para programar la ejecución del programa después de 10 segundos
def programa_ejecucion(request):
    # global thread_programa
    # global thread_programa_por_tiempo
    # global request_programa
    # global t_programa
    # global theared_program
    # request_programa = request
    # print(thread_programa_por_tiempo)
    # print(thread_programa)
    global theared
    theared.request_programa = request
    if theared.programa_execute != Programas.PROGRAMA_POR_TIEMPO:
        luces_sockets.off_all_channels()
        theared.changePrograma(Programas.PROGRAMA)
    # stop_event(t_programa, theared_program)
    # if not thread_programa_por_tiempo:
    #     if not thread_programa:
    # luces_sockets.off_all_channels()
    # thread_programa = True
    # t_programa = iniciar_programa(ejecutar_programa)
        #     print("Peiridankjdnjn")
        # else:
        #     print("Llego una nueva configuracion")
        #     stop_event(t_programa, theared_program)
        #     luces_sockets.off_all_channels()
        #     thread_programa_por_tiempo = True
        #     t_programa = iniciar_programa(ejecutar_programa)
    
# Función para programar la ejecución del programa después de 10 segundos
def programa_por_tiempo_ejecucion(request):
    # global thread_programa_por_tiempo
    # global thread_programa
    # global request_programa_por_tiempo
    # global t_programa
    # global t_programa_por_tiempo
    # request_programa_por_tiempo = request
    # if thread_programa:
    #     thread_programa = False 
        # t_programa.join()
    # stop_event(t_programa, theared_program)
    # Ejecutamos el programa en el tiempo especifico   
    # if not thread_programa_por_tiempo:

    global theared
    theared.request_programa_por_tiempo = request
    luces_sockets.guardar_configuracion_luces = None
    luces_sockets.off_all_channels()
    theared.changePrograma(Programas.PROGRAMA_POR_TIEMPO)
    # luces_sockets.off_all_channels()
    # thread_programa_por_tiempo = True
    # t_programa = iniciar_programa(ejecutar_programa_por_tiempo)
    time.sleep(request.get('time'))
    # print("Termino el tiempo")
    # thread_programa_por_tiempo = False
    # stop_event(t_programa, theared_program)

    luces_sockets.off_all_channels()
    theared.changePrograma(Programas.PROGRAMA)
    # luces_sockets.off_all_channels()
    # thread_programa = True 
    # t_programa = iniciar_programa(ejecutar_programa)
   
# Función para iniciar el programa
# def iniciar_programa(funcion):
#     global theared_program
#     print("Iniciando programa...")
#     # Iniciar el programa utilizando el executor
#     # Crea el evento
#     # theared_program = threading.Event()

#     # Crea el hilo para el evento
#     theared = TimedEventThread(1, theared_program, funcion)
#     start_event(theared)
#     # theared = threading.Thread(target=funcion)
#     # theared.start()
#     return theared

# Funcion de los sockets
@sio.event
def connect():
    print('connection established')

@sio.on('programa' + lugar)
def programa(data):
    programa_ejecucion(data)

@sio.on('programa_por_tiempo' + lugar)
def programa_por_tiempo(data):
    global theared
    theared.changePrograma(Programas.PROGRAMA)
    programa_por_tiempo_ejecucion(data)

@sio.event
def disconnect():
    print('disconnected from server')

if __name__ == "__main__":
    # Iniciar los sockets
    sio.connect('http://192.168.1.136:3005')
    # Crea el hilo para el evento
    theared = TimedEventThread(1, theared_program, ejecutar_programa, ejecutar_programa_por_tiempo)
    start_event(theared)
    sio.wait()