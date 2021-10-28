from typing import List, Union
import copy


# Raises
class InvalidHash(Exception):
    """Thrown when an invalid hash is met."""

class InvalidBlockNumber(Exception):
    """Thrown when Block has an invalid number."""

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
        Use this class with any data.
        Data in class is not validated.
    
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

    # Hash
    def get_hash(self) -> bytes:
        """Gets a Hash of Block.
        
        Returns:
            Hash of Block.
        """

        return self.hash

    def set_hash(self, hash: bytes):
        """Sets a Hash of Block.
        
        Args:
            hash: New Hash of Block.
        """

        self.hash = hash

    # Previous Hash
    def get_prev_hash(self) -> bytes:
        """Gets a Previous Hash of Block.
        
        Returns:
            Previous Hash of Block.
        """

        return self.prev_hash

    def link_prev_block(self, prev: Union['Block', bytes] = None):
        """Links the previous block to the current block.
        
        Args:
            prev: Previous Hash to link. Can have different types.
                Could be a Block instance, in this case it would acquire a Hash of this block.

                Could be a Hash or None to unlink.

        Raises:
            TypeError: Invalid argument type.
        """

        if isinstance(prev, Block):
            self.prev_hash = prev.hash
        elif isinstance(prev, bytes) or prev is None:
            self.prev_hash = prev
        else:
            raise TypeError("Argument 'prev' doesn't match allowed argument type!")

    # Num
    def get_num(self) -> int:
        """Gets a Number of Block.
        
        Returns:
            Number of Block.
        """

        return self.num

    def set_num(self, num: int):
        """Sets a Number of Block.
        
        Args:
            num: New Number of Block.
        """

        self.num = num

    # Data
    def get_data(self) -> bytes:
        """Gets a Data of Block.
        
        Returns:
            Data of Block.
        """

        return self.data

    def set_data(self, data: bytes):
        """Sets a Data of Block.
        
        Args:
            data: New Data of Block.
        """

        self.data = data


class Blockchain:
    """Class representing a whole Blockchain.
    
    Usage:
        This class is present as a Structure.
        Use this class with any data.
        Data in class is not validated.
    
    Structure:
        hash: Hash of the Blockchain.
            This is the Hash of the last Block in the Blockchain.
        num: Number of the last Block in the Blockchain.
        blocks: Tied up Blocks chain.
            Use get method for using Blocks.
    """

    def __init__(self, hash: bytes, num: int, blocks: List[Block] = []) -> None:
        """Blockchain constructor.
        
        Used by Blockchain readers and writers to instantiate and fill with appropriate data.
        """

        self.hash = hash
        self.num = num
        self.blocks = copy.deepcopy(blocks)

    # Hash
    def get_hash(self) -> bytes:
        """Gets a Hash of Blockchain.
        
        Returns:
            Hash of Blockchain.
        """

        return self.hash

    def set_hash(self, hash: bytes):
        """Sets a Hash of Blockchain.
        
        Args:
            hash: New Hash of Blockchain.
        """

        self.hash = hash

    # Num
    def get_num(self) -> int:
        """Gets a Number of Blockchain.
        
        Returns:
            Number of Blockchain.
        """

        return self.num

    def set_num(self, num: int):
        """Sets a Number of Blockchain.
        
        Args:
            num: New Number of Blockchain.
        """

        self.num = num

    # Blocks
    def __len__(self) -> int:
        """Overrides len().
        
        Returns:
            Length of blockchain.
        """
        return len(self.blocks)

    def check_index(self, index: int):
        """Checks if index is in blocks range.
        
        Args:
            index: Index to check.

        Raises:
            InvalidBlockNumber: Block index is out of bounds!
        """

        if index < 0 or index >= len(self):
            raise InvalidBlockNumber(f"Block index {index} is out of range!")

    def get_block(self, index: int) -> Block:
        """Get a Block in the Blockchain.
        
        Args:
            index: Index of block.
            
        Returns:
            Block by index.

        Raises:
            InvalidBlockNumber: Block index is out of bounds!
        """

        self.check_index(index)

        return copy.deepcopy(self.blocks[index])

    def set_block(self, block: Block, index: int):
        """Set a Block in the Blockchain.
        
        Args:
            block: New block.
            index: Index of block.

        Raises:
            InvalidBlockNumber: Block index is out of bounds!
        """

        self.check_index(index)

        self.blocks[index] = copy.deepcopy(block)

    def append_block(self, block: Block):
        """Appends a block to the end of Blockchain.
        
        Args:
            block: Block to append.
        """

        self.blocks.append(copy.deepcopy(block))

    def remove_block(self, index: int):
        """Removes a block from the Blockchain.
        
        Args:
            index: Index of block.
            
        Raises:
            InvalidBlockNumber: Block index is out of bounds!
        """

        self.check_index(index)

        block = self.blocks[index]
        self.blocks.remove(block)


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

        Returns:
            Hash of block.
        """

    def reserved_prev_hash(self) -> bytes:
        """Function returns reserved previous hash value.
        
        Used for prev_hash field of the first Block in the chain.

        Returns:
            Reserved hash value.
        """