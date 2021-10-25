import socket
import threading
import concurrent.futures


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
        try:
            respond = executor.submit(client.recv, 32)
            payload = respond.result(2).decode('utf-8')
            
        except concurrent.futures.TimeoutError:
            payload = 'Client doesn\'t send anything!'
            client.send(b'Sussy baka!')

        else:
            client.send(b'OK')

        finally:
            print(f'[Client: {addr}] ' + f'\'{payload}\'')
            client.close()


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
        
        if console == 'quit':
            break

        elif console == 'clear' or console == 'cls':
            import os
            os.system('cls')

        elif console == 'threads' or console == 'thr':
            print(f'Current threads count: {threading.active_count()}')

        elif console == 'help':
            print('\nquit - Shuts down the server.')
            print('threads(thr) - Current Threads count.')
            print('clear(cls) - Clears the console.\n')

        elif console == 'sus':
            print('Amogus')

        else:
            print('Unknown command!')
            print('Type "help" to get commands list')