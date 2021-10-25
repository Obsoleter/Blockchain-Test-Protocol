import socket
import threading
import time
from modules.Header.headers import TestOperationClientConnect

from modules.Sockets.server import SERVER_ADDRESS, SERVER_PORT
import modules.Sockets.headers as TestHeaders


def client_receive(manager: TestHeaders.TestHeaderNetworkManager):
    while True:
        respond = manager.recv()
        if respond.operation == b'SERVER_SENT':
            print(f'[Server Message]: {respond.payload}')

        elif respond.operation == b'SERVER_DISCONNECTED':
            print(f'[Server Disconnected]: Closing connection...')
            break

        else:
            print(f'[Server Respond]: {respond.operation}')


def main():
    # Connect Server Socket
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.connect((SERVER_ADDRESS, SERVER_PORT))
    manager = TestHeaders.TestHeaderNetworkManager(server)

    # Try to Send Connection Packet
    time.sleep(3)
    manager.send(TestOperationClientConnect())

    # Get the Respond
    respond = manager.recv()

    # Get Server Data until SERVER_DISCONNECTED operation
    if respond.operation == b'SERVER_CONNECTED':
        print('[Client Info]: Successfully connected to the server! Start receiving info...')
        receiver = threading.Thread(target=client_receive, args=(manager,))
        receiver.start()
        receiver.join()

    else:
        print('[Client Info]: Couldn\'t establish connection!')