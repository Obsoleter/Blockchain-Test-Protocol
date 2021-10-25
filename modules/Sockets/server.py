import socket
import threading
import concurrent.futures

import modules.Sockets.headers as TestHeaders
import modules.Header.headers as ProtocolHeaders


# Server settings
SERVER_ADDRESS = 'localhost'
"""Server Address
"""

SERVER_PORT = 7777
"""Server Port
"""

SERVER_MAX_LISTEN = 5
"""Max count of client connected
"""


# Set up Server Socket to listen
def server_listen():
    """Sets up the Server to listen for connections

    Returns:
        Server associated socket
    """

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind(
        (SERVER_ADDRESS, SERVER_PORT)
    )

    server.listen(SERVER_MAX_LISTEN)

    return server


# Server connection
def server_connection(client: socket.socket, addr: str):
    """Handles and determines a connection with client.

    Args:
        client: Socket of a client connected
        addr: Address of a client connected
    """

    print(f'[Client: {addr}] Connected!')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        manager = TestHeaders.TestHeaderNetworkManager(client)
        info_result = 'None'
        
        # Handle client behaviour
        try:
            respond = executor.submit(manager.recv).result(2)
            info_result = 'Connection established!'
            
        # Handle client Time Out
        except concurrent.futures.TimeoutError:
            info_result = 'Client doesn\'t send anything!'

        # Handle client
        else:
            if respond.operation == b'CLIENT_CONNECT':
                manager.send(ProtocolHeaders.TestOperationServerConnected())
                manager.send(ProtocolHeaders.TestOperationServerSent(b'19 dollar Fortnine card...'))
                manager.send(ProtocolHeaders.TestOperationServerSent(b'Who wants it?'))
                manager.send(ProtocolHeaders.TestOperationServerSent(b'And yes, I\'m giving it away.'))

        # Close connection with client
        finally:
            manager.send(ProtocolHeaders.TestOperationServerDisconnected())
            client.close()
            print(f'[Client: {addr}] {info_result}')


# Server loop
def server_loop(server: socket.socket):
    """Represents Looping function for the Server.
    
    Infinite loop, accepting client connections.

    Args:
        server: Socket representing the Server
    """

    while True:
        connection = threading.Thread(target=server_connection, daemon=True, args=server.accept())
        connection.start()


# Server set up & Handle console commands
def main():
    server = server_listen()
    listen_thread = threading.Thread(target=server_loop, daemon=True, args=(server,))
    listen_thread.start()

    while True:
        console = input().lower()

        if console == 'help':
            print('\nquit - Shuts down the server.')
            print('threads(thr) - Current Threads count.')
            print('clear(cls) - Clears the console.\n')
        
        elif console == 'quit':
            break

        elif console == 'threads' or console == 'thr':
            print(f'Current threads count: {threading.active_count()}')

        elif console == 'clear' or console == 'cls':
            import os
            os.system('cls')

        else:
            print('Unknown command!')
            print('Type "help" to get commands list')