
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def ermita(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://192.168.1.136:3005')
sio.wait()