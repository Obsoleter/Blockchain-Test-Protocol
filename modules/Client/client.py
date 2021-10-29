import socket, threading, time, sys, os

from modules.Blockchain.blockchain import Blockchain, Block
from modules.Blockchain.validation_utils.factories import ServerBlockchainFactory

from modules.Network.servers import TRUSTED_SERVERS

from modules.Sockets.blockchain.protocol_factory import BlockchainNetworkManagerFactory
import modules.Protocol.blockchain.header as ProtocolHeader
import modules.Protocol.blockchain.operations as ProtocolOperations

from modules.Blockchain.utils.Drivers.hash import HashManagerDriver



def print_header(header: Blockchain):
    print('==========')
    print(f'Number: {header.num}')
    print(f'Hash: {header.hash}')
    print('==========')

def print_block(block: Block):
    print('==========')
    print(f'Number: {block.num}')
    print(f'Hash: {block.hash}')
    print(f'Previous Hash: {block.prev_hash}')
    print(f'Data: {block.data}')
    print('==========')


def request_scan():
    """Scans ledgers of trusted servers.
    
    Args:
        client: Client socket.
    """

    # Create socket for server
    # server = socket.socket(
    #     socket.AF_INET,
    #     socket.SOCK_STREAM
    # )

    # Get header of each trusted server
    for trusted_server in TRUSTED_SERVERS:
        try:
            # Init socket for server and connect
            server = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            server.connect(trusted_server)

        except ConnectionRefusedError:
            print(f'Trusted server: {trusted_server} doesn\'t answer!')

        else:
            manager = BlockchainNetworkManagerFactory.create(server, ProtocolHeader.BlockchainProtocolPacket)
            manager.send(ProtocolOperations.LedgerAskHeader())
            respond = manager.recv()
            print(f"Trusted server: {trusted_server} responded with header!")
            print_header(manager.decode_header(respond))
            server.close()


def request_header(index: int):
    """Asks ledger header of trusted server.
    
    Args:
        client: Client socket.
        index: Index of trusted server.
    """

    # Check index
    if index < 0 or index >= len(TRUSTED_SERVERS):
        print("Invelid trusted server index! Try again...")
        return

    # Get header of trusted server
    trusted_server = TRUSTED_SERVERS[index]

    try:
        # Create socket for server
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        server.connect(trusted_server)

    except ConnectionRefusedError:
        print(f'Trusted server: {trusted_server} doesn\'t answer!')

    else:
        manager = BlockchainNetworkManagerFactory.create(server, ProtocolHeader.BlockchainProtocolPacket)
        manager.send(ProtocolOperations.LedgerAskHeader())
        respond = manager.recv()
        print(f"Trusted server: {trusted_server} responded with header!")
        print_header(manager.decode_header(respond))
        server.close()


def request_get_block(index: int, num: int):
    """Asks server for block.
    
    Args:
        index: Index of trusted server.
        num: Number of block.
    """

    # Check index
    if index < 0 or index >= len(TRUSTED_SERVERS):
        print("Invelid trusted server index! Try again...")
        return

    # Get block of trusted server
    trusted_server = TRUSTED_SERVERS[index]

    try:
        # Create socket for server
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        server.connect(trusted_server)

    except ConnectionRefusedError:
        print(f'Trusted server: {trusted_server} doesn\'t answer!')

    else:
        manager = BlockchainNetworkManagerFactory.create(server, ProtocolHeader.BlockchainProtocolPacket)
        manager.send(ProtocolOperations.LedgerAskBlock(Block(b'', b'', num, b'')))
        respond = manager.recv()
        if respond.operation == b"SERVER_DENY":
            print(f"Trusted server: {trusted_server} denied!")
            print(respond.payload)

        elif respond.operation == b"LEDGER_RESPOND_BLOCK":
            print(f"Trusted server: {trusted_server} responded with block!")
            print_block(manager.decode_block(respond))

        server.close()


def request_add_block(index: int, data: bytes):
    """Asks to add new block in blockchain.
    
    Args:
        index: Index of server to add block.
        data: Data of block.
    """

    # Check index
    if index < 0 or index >= len(TRUSTED_SERVERS):
        print("Invelid trusted server index! Try again...")
        return

    # Get the Last Block
    # Get block of trusted server
    trusted_server = TRUSTED_SERVERS[index]
    hash_manager = HashManagerDriver()

    try:
        # Create socket for server
        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        server.connect(trusted_server)

    except ConnectionRefusedError:
        print(f'Trusted server: {trusted_server} doesn\'t answer!')

    else:
        # Get Header
        manager = BlockchainNetworkManagerFactory.create(server, ProtocolHeader.BlockchainProtocolPacket)
        manager.send(ProtocolOperations.LedgerAskHeader())
        header = manager.decode_header(manager.recv())

        # Generate valid block with given data
        block = Block(b'', header.get_hash(), header.get_num() + 1, data)
        block.set_hash(hash_manager.hash_block(block))

        # Send new block to the server
        manager.send(ProtocolOperations.BlockAdd(block))

        # Handle Respond
        respond = manager.recv()

        if respond.operation == b"SERVER_DENY":
            print(f"Trusted server: {trusted_server} denied!")
            print(respond.payload)

        elif respond.operation == b"SERVER_ACCEPT":
            print(f"Trusted server: {trusted_server} accepted new block!")

        server.close()


def main(path: str):
    while True:
        try:
            # Get command and arguments
            args = input().split(' ')
            command = args[0]

            # Handle command
            if command == 'help':
                print('')
                print('help - Commands description.')
                print('clear(cls) - Clean console.')
                print('quit - Exit client programm.')
                print('scan [<index> | None] - Scans trusted servers.')
                print('get_block <index> <number of block> - Downloads block from server.')
                print('generate <server index> <data> - Generates new block.')
                print('')

            elif command == 'clear' or command == 'cls':
                os.system('cls')

            elif command == 'quit':
                break

            elif command == 'scan':
                if len(args) == 1:
                    request_scan()

                elif len(args) == 2:
                    request_header(int(args[1]))

                else:
                    print("Invalid number of arguments!")

            elif command == 'get_block':
                if len(args) != 3:
                    print("Invalid arguments number!")

                else:
                    index = int(args[1])
                    num = int(args[2])
                    request_get_block(index, num)

            elif command == 'generate':
                if len(args) < 3:
                    print("Invalid arguments number!")

                else:
                    index = int(args[1])

                    data = args[2].encode('utf-8')
                    for i in range(3, len(args)):
                        data += b' ' + args[i].encode('utf-8')

                    request_add_block(index, data)

            else:
                print(f"Unknown command: '{command}'! Type 'help' to get commands list.")

        except Exception as exc:
            print("Invalid input! Try again...")
            print(exc)


if __name__ == '__main__':
    main('client')