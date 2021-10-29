from socket import socket
from typing import Literal, Type

from ..protocol import ProtocolNetworkManager

from modules.Blockchain.blockchain import Block, Blockchain, HashManager

from modules.Protocol.blockchain.header import BlockchainProtocolPacket
import modules.Protocol.blockchain.operations as ProtocolOperations
from modules.Protocol.header import ProtocolPacket


class BlockchainNetworkManager(ProtocolNetworkManager):
    """Class used to receive and send Blockchain through network."""

    def __init__(self, hash_manager: HashManager, socket: socket, PACKET: Type) -> None:
        """Manager constructor."""

        self.hash_manager = hash_manager
        super().__init__(socket, PACKET)

    def decode_header(self, packet: ProtocolPacket) -> Blockchain:
        """Decodes received Blockchain Header.
        
        Args:
            packet: Packet to decode.

        Raises:
            InvalidHash: Can't decode hash.
        """

        num = packet.payload[:BlockchainProtocolPacket.PACKET_BLOCK_SIZE_BYTES]
        num = int.from_bytes(num, 'little')

        hash = packet.payload[BlockchainProtocolPacket.PACKET_BLOCK_SIZE_BYTES:]

        return Blockchain(hash, num)

    def decode_block(self, packet: ProtocolPacket, num_only: bool = False) -> Block:
        """Decodes received Block.
        
        Args:
            packet: Packet to decode.
        """

        # Num
        start = 0
        end = BlockchainProtocolPacket.PACKET_BLOCK_SIZE_BYTES
        num = packet.payload[start:end]
        num = int.from_bytes(num, 'little')

        if num_only:
            return Block(b'', b'', num, b'')

        # Hash
        start = end
        end = start + self.hash_manager.get_hash_len()
        hash = packet.payload[start:end]

        # Previous hash
        start = end
        end = start + self.hash_manager.get_hash_len()
        prev_hash = packet.payload[start:end]

        # Data
        start = end
        data = packet.payload[start:]

        return Block(hash, prev_hash, num, data)