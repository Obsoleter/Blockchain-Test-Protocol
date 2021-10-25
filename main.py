import sys


# Choosing client or server
def client():
    import modules.Sockets.client as client
    client.main()

def server():
    import modules.Sockets.server as server
    server.main()


# Load function
if __name__ == '__main__':
    if sys.argv.__len__() != 2:
        print('Wrong number of arguments!')
        print('Usage be like: main.py [server|client]')
        sys.exit()

    argument = sys.argv[1]

    if argument == 'client':
        client()

    elif argument == 'server':
        server()

    else:
        print('Unknown type of device!')