
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def csermita(data):
    print('message received with ', data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://192.168.1.136:3005')
sio.wait()