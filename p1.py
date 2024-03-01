import socketio
import threading
import time
# Llamada a los sockets
sio = socketio.Client()
# Programas corriendo
programa_continuo_running = False
programa_por_tiempo_running = False
# Programar cada programa
def programa_continuo_function():
    global programa_continuo_running
    while programa_continuo_running:
        print('Ejecutando el programa continuo...')
        time.sleep(3)

def programa_por_tiempo_function():
    global programa_por_tiempo_running
    while programa_por_tiempo_running:
        print('Ejecutando el programa por tiempo...')
        time.sleep(300)  # 5 minutos de espera

@sio.event
def connect():
    print('Conectado al servidor')
    sio.emit('message', 'Hola desde Python')

@sio.event
def programacontinuo(data):
    print('Mensaje del servidor programa_continuo luces:', data)

@sio.event
def programaportiempo(data):
    print('Mensaje del servidor programa_por_tiempo luces:', data)

@sio.event
def disconnect():
    print('Desconectado del servidor')

if __name__ == "__main__":
    sio.connect('http://192.168.1.136:3005', wait_timeout=10)

    # thread_programa_continuo = threading.Thread(target=programa_continuo_function)
    # thread_programa_continuo.start()
    sio.wait()
    # thread_programa_por_tiempo = threading.Thread(target=programa_por_tiempo_function)
    # thread_programa_por_tiempo.start()