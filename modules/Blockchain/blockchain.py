from typing import List


# Raises
class InvalidHash(Exception):
    """Thrown when an invalid hash is met."""

class InvalidBlockchain(Exception):
    """Base class for any Blockchain related raise."""

class InvalidBlockchainNumber(InvalidBlockchain):
    """Thrown when a number of a Blockchain differs from a number of the last Block."""

class InvalidBlockOrder(InvalidBlockchain):
    """Thrown when Blocks are not ordered in the list
    or when there's a gap between blocks.
    """

class InvalidLink(InvalidBlockchain):
    """Thrown when an invalid link with the previous block is met."""


# Classes
class Block:
    """Class representing a Block.

    Usage:
        This class is present as a Structure.
        It's not recommended to instantiate this class
        as internally it doesn't both validate fields and throw exceptions.
        Use only with some kind of wrapper!

    Use other classes that instantiate it for you.
    
    Structure:
        hash: Hash of the Block.
        prev_hash: Hash of the previous Block.
            Zero if the first Block.
        num: Number of the Block starting from 1.
        data: Data stored in the Block.
        """

    def __init__(self, hash: bytes, prev_hash: bytes, num: int, data: bytes) -> None:
        """Block constructor.
        
        Args:
            hash: Hash of the Block.
            prev_hash: Hash of the previous Block.
                Zero if the first Block.
            num: Number of the Block starting from 1.
            data: Data storing in the Block.
        """

        self.hash = hash
        self.prev_hash = prev_hash
        self.num = num
        self.data = data


class Blockchain:
    """Class representing a whole Blockchain.
    
    Usage:
        This class is present as a Structure.
        It's not recommended to instantiate this class
        as internally it doesn't both validate fields and throw exceptions.
        Use only with some kind of wrapper!
    
    Structure:
        hash: Hash of the Blockchain.
            This is the Hash of the last Block in the Blockchain.
        num: Number of the last Block in the Blockchain.
        blocks: Tied up Blocks chain.
            Use get method for using Blocks.
    """

    def __init__(self, hash: bytes, num: int, blocks: List[Block]) -> None:
        """Blockchain constructor.
        
        Used by Blockchain readers and writers to instantiate and fill with appropriate data.
        """

        self.hash = hash
        self.num = num
        self.blocks = blocks


# Interfaces
class HashManager:
    """Abstract class used to present the interface
    for Blockchain related classes.

    Usage:
        Use Concrete Drivers instead that implement this class
        or make your own Driver if needed.
    """

    def hash(self, data: bytes) -> bytes:
        """Hash function using the current Hash algorithm.

        Args:
            data: Data to Hash.
            
        Returns:
            Encoded bytes array.
        """

    def is_valid_hash(self, hash: bytes) -> bool:
        """Function used to check if presented Hash corresponds
        to the current Hash algorithm.
        
        Args:
            hash: Hash to validate.
            
        Returns:
            True whenever Hash is valid and False otherwise."""

    def hash_block(self, block: Block) -> bytes:
        """Function to calculate a Hash of a Block.
        
        Uses the current Hash Algorithm.
        
        Args:
            block: Block to hash.
        """

    def reserved_prev_hash(self) -> bytes:
        """Function returns reserved previous hash value.
        
        Used for prev_hash field of the first Block in the chain.
        """