
import asyncio
import websockets

async def recibir_mensajes():
    uri = 'ws://192.168.1.136:3005'
    async with websockets.connect(uri) as websocket:
        while True:
            mensaje = await websocket.recv()
            print(f"Mensaje recibido: {mensaje}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(recibir_mensajes())