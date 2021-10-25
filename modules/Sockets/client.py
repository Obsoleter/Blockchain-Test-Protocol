import socket
import time

from modules.Sockets.server import SERVER_ADDRESS, SERVER_PORT


def main():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    
    server.connect((SERVER_ADDRESS, SERVER_PORT))
    # time.sleep(5)
    # server.send(b'Amogus among us!Amogus among us!Amogus among us!Amogus among us!Amogus among us!')
    # server.send(b'Amogus among us!Amogus among us!Amogus among us!Amogus among us!Amogus among us!')
    server.close()

    # data = server.recv(1024)
    # print(data)