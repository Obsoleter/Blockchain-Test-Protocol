import sys
from modules.Network.servers import TRUSTED_SERVERS


# Choosing client or server
def client(path: str):
    import modules.Client.client as client
    client.main(path)

def server(path: str, index: int):
    import modules.Server.server as server
    server.main(path, index)


# Load function
if __name__ == '__main__':
    if sys.argv.__len__() < 3:
        print('Wrong number of arguments!')
        print('Usage be like: main.py <blockchain path> [server|client]')
        sys.exit()

    path = sys.argv[1]

    mode = sys.argv[2]

    if mode == 'client':
        client(path)

    elif mode == 'server':
        if len(sys.argv) < 4:
            raise TypeError("Didn't find index argument for server!\n" + "Use: 'py main.py <blockchain path> server <index>")

        else:
            index = int(sys.argv[3])
            if index < 0 or index >= len(TRUSTED_SERVERS):
                raise IndexError("No trusted server with this index!\n" + f"Use index from {0} to {len(TRUSTED_SERVERS) - 1}")

            server(path, index)

    else:
        print('Unknown type of mode!')