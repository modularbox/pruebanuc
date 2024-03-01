import asyncio
import socketio

# Crear un cliente de socket.io
sio = socketio.AsyncClient()

# Evento que se activa cuando se establece la conexión con el servidor
@sio.event
async def connect():
    print('Conectado al servidor de Socket.IO')

# Evento que se activa cuando se recibe un mensaje del servidor
@sio.event
async def message(data):
    print('Mensaje del servidor:', data)

async def main():
    # Conectar al servidor de Socket.IO
    await sio.connect('http://192.168.1.136:3005')

    # Mantener un bucle infinito para recibir mensajes continuamente
    while True:
        await asyncio.sleep(1)  # Esperar un poco antes de continuar

if __name__ == '__main__':
    asyncio.run(main())
