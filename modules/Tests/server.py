from modules.Protocol.header import ProtocolPacket

# Blockchain protocol
import modules.Protocol.blockchain.header as ProtocolHeader
import modules.Protocol.blockchain.operations as ProtocolOperations

# Networking
import modules.Sockets.protocol as protocol
import modules.Server.server

# Blockchain storage
import modules.Blockchain.storage_utils.factory as BlockchainFactory

import threading
import time
import concurrent.futures


def print_header(header: ProtocolPacket):
    print('==========')
    print(header.size)
    print(header.operation)
    print(header.payload)
    print(header.delimiter)
    print('==========')


chain = BlockchainFactory.StoredBlockchainFactory().create()


server = modules.Server.server.server_listen()

client, addr = server.accept()

manager = protocol.ProtocolNetworkManager(client, ProtocolHeader.BlockchainProtocolPacket)

# Wait for LEDGER_ASK
header = manager.recv()
print_header(header)

# Send LEDGER_RESPOND_BLOCK
for n in range(chain.num, 0, -1):
    block = chain.get_block(n)
    header = ProtocolOperations.LedgerRespondBlock(block)
    manager.send(header)
    print_header(header)