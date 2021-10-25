import modules.Header.headers
import modules.Sockets.headers
import modules.Sockets.server

import threading
import time
import concurrent.futures


def print_header(header: modules.Header.headers.TestMessageHeader):
    print('==========')
    print(header.size)
    print(header.operation)
    print(header.payload)
    print(header.delimiter)
    print('==========')


server = modules.Sockets.server.server_listen()

client, addr = server.accept()

manager = modules.Sockets.headers.TestHeaderNetworkManager(client)

# Wait for CLIENT_CONNECT
header = manager.recv()
print_header(header)

# Send SERVER_CONNECTED
header = modules.Header.headers.TestOperationServerConnected()
manager.send(header)
print_header(header)

# Wait for CLIENT_GET
header = manager.recv()
print_header(header)

# Send SERVER_SENT
header = modules.Header.headers.TestOperationServerSent(b'Hello Susy Baka!')
manager.send(header)
print_header(header)

# Send SERVCER_DISCONNECTED
header = modules.Header.headers.TestOperationServerDisconnected()
manager.send(header)
client.close()
print_header(header)