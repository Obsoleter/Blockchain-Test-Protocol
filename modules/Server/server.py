import socket
import threading
import concurrent.futures

from modules.Sockets.blockchain.protocol_factory import BlockchainNetworkManagerFactory, BlockchainNetworkManager

from modules.Protocol.header import UnknownOperation
from modules.Protocol.base.operations import ServerAccept, ServerDeny
import modules.Protocol.blockchain.header as ProtocolHeader
import modules.Protocol.blockchain.operations as ProtocolOperations

from modules.Blockchain.blockchain import Blockchain, Block
from modules.Blockchain.storage_utils.factory import StoredBlockchainFactory
from modules.Blockchain.validation_utils.factories import ValidatorFactory

from modules.Network.servers import TRUSTED_SERVERS


# Server settings
# SERVER_ADDRESS = 'localhost'
# """Server Address
# """

# SERVER_PORT = 27012
# """Server Port
# """

SERVER_MAX_LISTEN = 5
"""Max count of client connected
"""

global server_address

TRUSTED_IPS = [ip for ip, port in TRUSTED_SERVERS]


def spread_block(block: Block):
    for trusted_server in TRUSTED_SERVERS:
        # Don't send us
        if trusted_server == server_address:
            continue

        try:
            # Init socket for server and connect
            server = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            server.connect(trusted_server)

            # Send block
            manager = BlockchainNetworkManagerFactory.create(server, ProtocolHeader.BlockchainProtocolPacket)
            manager.send(ProtocolOperations.BlockSpread(block))
            server.close()

        # Server doesn't answer
        except ConnectionRefusedError:
            print(f'Trusted server: {trusted_server} doesn\'t answer!')
            

# Set up Server Socket to listen
def server_listen(index: int):
    """Sets up the Server to listen for connections

    Returns:
        Server associated socket
    """

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind(
        TRUSTED_SERVERS[index]
    )

    server.listen(SERVER_MAX_LISTEN)

    return server


# Server connection
def server_connection(client: socket.socket, addr, chain: Blockchain):
    """Handles and determines a connection with client.

    Args:
        client: Socket of a client connected
        addr: Address of a client connected
    """

    print(f'[Client: {addr}] Connected!')

    manager = BlockchainNetworkManagerFactory.create(client, ProtocolHeader.BlockchainProtocolPacket)
    validator = ValidatorFactory().create()

    while client:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            info_result = 'None'
            
            # Handle client behaviour
            try:
                respond = executor.submit(manager.recv).result(2)
                
            # Handle client Time Out
            except concurrent.futures.TimeoutError:
                info_result = 'Client doesn\'t send anything! Stop connection...'
                break

            except (ConnectionResetError, UnknownOperation):
                info_result = 'Client closed connection!'
                break

            # Handle client
            else:
                if respond.operation == b'LEDGER_ASK_HEADER':
                    manager.send(ProtocolOperations.LedgerRespondHeader(chain))
                    info_result = 'Operation: LEDGER_ASK_HEADER'

                elif respond.operation == b'LEDGER_ASK_BLOCK':
                    block = manager.decode_block(respond, True)
                    if block.num < 1 or block.num > chain.num:
                        manager.send(ServerDeny(b"Invalid block number!"))
                        info_result = f"Asked for invalid block with number: {block.num}!"

                    else:
                        block = chain.get_block(block.num)
                        manager.send(ProtocolOperations.LedgerRespondBlock(block))
                        info_result = f"Asked for valid block with number: {block.num}! Responding with block..."

                elif respond.operation == b'LEDGER_ASK':
                    for n in range(chain.num, 0, -1):
                        block = chain.get_block(n)
                        manager.send(ProtocolOperations.LedgerRespondBlock(block))
                    info_result = 'Operation: LEDGER_ASK'

                elif respond.operation == b'BLOCK_ADD':
                    try:
                        block = manager.decode_block(respond)
                        validator.validate_block(block)

                        last_block = chain.get_block(chain.get_num())
                        validator.validate_link(last_block, block)

                    except Exception as exc:
                        info_result = 'Operation: BLOCK_ADD - Received invalid block.'
                        header = ServerDeny(str(exc).encode('utf-8'))
                        manager.send(header)
                        break

                    else:
                        header = ServerAccept()
                        manager.send(header)
                        info_result = 'Operation: BLOCK_ADD - Received valid block. Adding to Blockchain.'
                        chain.append_block(block)

                        #Spread block
                        spread_block(block)

                # Spread block
                elif respond.operation == b'BLOCK_SPREAD':
                    if addr[0] not in TRUSTED_IPS:
                        info_result = 'Operation: BLOCK_SPREAD - Requested from untrusted source!'
                        break

                    block = manager.decode_block(respond)

                    if block.get_num() != chain.get_num():
                        try:
                            block = manager.decode_block(respond)
                            validator.validate_block(block)

                            last_block = chain.get_block(chain.get_num())
                            validator.validate_link(last_block, block)

                        except Exception:
                            info_result = 'Operation: BLOCK_SPREAD - Received invalid block!'
                            break

                        else:
                            info_result = 'Operation: BLOCK_SPREAD - Received valid block!'
                            chain.append_block(block)
                            spread_block(block)

                else:
                    info_result = 'Client closed connection!'
                    break

            # Print result of query
            finally:
                print(f'[Client: {addr}] {info_result}')
                
    client.close()


# Server loop
def server_loop(server: socket.socket, chain: Blockchain):
    """Represents Looping function for the Server.
    
    Infinite loop, accepting client connections.

    Args:
        server: Socket representing the Server
    """

    while True:
        connection = threading.Thread(target=server_connection, daemon=True, args=(*server.accept(), chain))
        connection.start()


# Server set up & Handle console commands
def main(path: str, index: int):
    server = server_listen(index)
    global server_address
    server_address = TRUSTED_SERVERS[index]

    chain = StoredBlockchainFactory().create(path)

    listen_thread = threading.Thread(target=server_loop, daemon=True, args=(server, chain))
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