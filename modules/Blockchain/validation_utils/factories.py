from typing import List

from ..utils.Drivers.hash import HashManagerDriver
from ..validated_blockchain import Block, ValidatedBlockchain, Blockchain
from ..server_blockchain import ServerBlockchain

from ..validator import BlockchainValidator


class ValidatedBlockchainFactory:
    """Factory for Validated Blockchain."""

    def __init__(self) -> None:
        """Factory constructor."""

    def create(self, blocks: List[Block]) -> Blockchain:
        """Creates Validated Blockchain.
        
        Args:
            blocks: Blocks for Validated Blockchain.
            
        Returns:
            Constructed Validated Blockchain.
        """

        # Dependencies
        hash_manager = HashManagerDriver()

        return ValidatedBlockchain(hash_manager, blocks)


class ValidatorFactory:
    """Factory for Blockchain Validator."""

    def __init__(self) -> None:
        """Factory constructor."""

    def create(self) -> BlockchainValidator:
        """Creates Blockchain Validator.
        
        Returns:
            Constructed Blockchain Validator.
        """

        # Dependencies
        hash_manager = HashManagerDriver()

        return BlockchainValidator(hash_manager)


class ServerBlockchainFactory:
    """Factory for Server Blockchain."""

    def __init__(self) -> None:
        """Factory constructor."""

    def create(self, header: Blockchain) -> ServerBlockchain:
        """Creates Server Blockchain.
        
        Returns:
            Constructed Server Blockchain.
        """

        validator = ValidatorFactory().create()

        return ServerBlockchain(validator, header)