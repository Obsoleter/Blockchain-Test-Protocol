from modules.Sockets.server import SERVER_PORT, SERVER_ADDRESS
import modules.Header.headers
import modules.Sockets.headers

import socket
import time


def print_header(header: modules.Header.headers.TestMessageHeader):
    print('==========')
    print(header.size)
    print(header.operation)
    print(header.payload)
    print(header.delimiter)
    print('==========')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
manager = modules.Sockets.headers.TestHeaderNetworkManager(server)

server.connect((SERVER_ADDRESS, SERVER_PORT))

# Connect
header = modules.Header.headers.TestOperationClientConnect()
manager.send(header)
print_header(header)

# Get answer
header = manager.recv()
print_header(header)

# Send Info Request
header = modules.Header.headers.TestOperationClientGet()
manager.send(header)
print_header(header)

# Get Info 3 Times
header = manager.recv()
print_header(header)

header = manager.recv()
print_header(header)

header = manager.recv()
print_header(header)

# Get Disconnect
header = manager.recv()
print_header(header)