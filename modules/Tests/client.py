from modules.Protocol.header import ProtocolPacket
import modules.Protocol.blockchain.header as ProtocolHeader
import modules.Protocol.blockchain.operations as ProtocolOperations

import modules.Sockets.blockchain.protocol as BlockchainProtocol
from modules.Sockets.blockchain.protocol_factory import BlockchainNetworkManagerFactory, BlockchainNetworkManager

from modules.Blockchain.blockchain import Block, Blockchain
from modules.Blockchain.validation_utils.factories import ServerBlockchainFactory
from modules.Blockchain.storage_utils.factory import StoredBlockchainFactory

from modules.Network.servers import TRUSTED_SERVERS

from .blockchain import print_block, print_blockchain

import socket, sys


def print_header(header: ProtocolPacket):
    print('==========')
    print(header.size)
    print(header.operation)
    print(header.payload)
    print(header.delimiter)
    print('==========')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
manager = BlockchainNetworkManagerFactory.create(server, ProtocolHeader.BlockchainProtocolPacket)

is_connected = False
for addr in TRUSTED_SERVERS:
    try:
        server.connect(addr)

    except ConnectionRefusedError:
        pass

    else:
        is_connected = True
        break

if not is_connected:
    print("Can't connect any trusted server...")
    sys.exit()

# Ask Header
header = ProtocolOperations.LedgerAskHeader()
manager.send(header)

# Get Header
header = manager.recv()
chain = ServerBlockchainFactory().create(manager.decode_header(header))

# Ask Ledger
header = ProtocolOperations.LedgerAsk()
manager.send(header)

# Get Ledger
if chain.num > 0:
    block = manager.decode_block(manager.recv())
    
    while chain.insert_block(block):
        block = manager.decode_block(manager.recv())


stored_chain = StoredBlockchainFactory().create('client')
stored_chain.clear()

for n in range(0, chain.num):
    block = chain.get_block(n)
    stored_chain.append_block(block)

# stored_chain.append_block(Block(b'', b'', 0, b"Helol!"))

# block = stored_chain.get_block(stored_chain.get_num())

# header = ProtocolOperations.BlockAdd(block)
# manager.send(header)

# respond = manager.recv()
# print(f'Operation respond: {respond.operation}!')
# print(respond.payload)

print_blockchain(stored_chain)