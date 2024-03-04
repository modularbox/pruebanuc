
import socketio
import sys
sio = socketio.Client()

# Obtener el primer argumento que sera el lugar donde estara la nuc
# Example: Correr programa python3 luces.py lugar
lugar = 'garage'
if len(sys.argv) > 1:
    lugar = sys.argv[1]
    print("El valor del parámetro es:", lugar)

@sio.event
def connect():
    print('connection established')

@sio.on('programa' + lugar)
def programa(data):
    print('message received with ', data)

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