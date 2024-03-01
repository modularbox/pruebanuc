import socketio
import threading
import time
# Llamada a los sockets
sio = socketio.AsyncClient(logger=True, engineio_logger=True)
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
    sio.emit('mensaje', 'Hola desde Python')

@sio.on('mensaje')
async def on_mensaje(data):
    print('Mensaje del servidor programa_continuo luces:', data)

@sio.on('programacontinuo')
async def on_programacontinuo(data):
    print("Dsjfnkjsdnfkdmfsklm")
    print('I received a message!', data)
# @sio.event
# def programacontinuo(data):
#     print('Mensaje del servidor programa_continuo luces:', data)

@sio.on('programaportiempo2')
async def on_programacontinuo(data):
    print('Mensaje del servidor programa_por_tiempo luces:', data)

@sio.event
def disconnect():
    print('Desconectado del servidor')

async def main():
    await sio.connect('http://192.168.1.136:3005', wait_timeout=10)
if __name__ == "__main__":
    main()

    # thread_programa_continuo = threading.Thread(target=programa_continuo_function)
    # thread_programa_continuo.start()
    # sio.wait()
    # thread_programa_por_tiempo = threading.Thread(target=programa_por_tiempo_function)
    # thread_programa_por_tiempo.start()