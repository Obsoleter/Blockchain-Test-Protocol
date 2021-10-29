import socket
from typing import Type

from modules.Blockchain.utils.Drivers.hash import HashManagerDriver
from .protocol import BlockchainNetworkManager


class BlockchainNetworkManagerFactory:
    """Factory for BlockchainNetworkManager class."""

    @staticmethod
    def create(socket: socket.socket, PACKET: Type) -> BlockchainNetworkManager:
        """Creates BlockchainNetworkManager."""

        hash_manager = HashManagerDriver()

        return BlockchainNetworkManager(hash_manager, socket, PACKET)