from simple_socket_client import SimpleSocketClient

client = SimpleSocketClient('192.168.1.136', 3005)
client.connect(timeout=10)

client.send('Test'.encode()) # if you don't need an answer
answer = client.ask('Hi!'.encode())
print(answer.decode())

client.disconnect()