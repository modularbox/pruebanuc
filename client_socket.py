# cliente.py
import socketio
sio = socketio.Client()

@sio.event
def connect():
    print('Conectado al servidor')
    sio.emit('message', 'Hola desde Python')

@sio.event
def encender(data):
    print('Mensaje del servidor Encender luces:', data)

@sio.event
def ermita(data):
    print('Mensaje del servidodskjbfjisdbjsbdjkbkjfdbskj luces:', data)

@sio.event
def disconnect():
    print('Desconectado del servidor')

sio.connect('http://192.168.1.136:3005')
# sio.connect('http://192.168.1.136:3001', wait_timeout=10)
sio.wait()
