from typing import List
from .blockchain import Block, Blockchain, HashManager
from .Drivers.hash import HashManagerDriver
from .blockchain_validator import BlockchainValidator


# Classes
class BlockFactory:
    """Class used to instantiate Block class.
    
    Validates fields and throws exceptions if meets invalid arguments.
    """

    def __init__(self) -> None:
        """Block Factory constructor."""

        # Driver to use Hash Algorithm
        self.hash_manager: HashManager = HashManagerDriver()

        # Validator
        self.validator = BlockchainValidator(self.hash_manager)

    def create_block(self, num: int, data: bytes, prev_block: Block = None, hash: bytes = None) -> Block:
        """Creates a Block with field validation.
        
        Args:
            prev_block: The previous block to link.
                Could be none, in this case it would get reserver value.
                Could be a Block instance, in this case it would acquire a hash of this block.
            num: ID of block in a chain.
            data: Stored data.
            hash: Hash of block.
                Calculated itself if is None. Otherwise this field would be checked.

        Raises:
            InvalidHash: Thrown when a hash of a block doesn't match a hash in field
                or if prev_hash is invalid.
        """

        # Create a block instance to set up
        block = Block(b'', b'', num, data)

        # Bind arguments, hash must be last!
        self.link_prev_block(block, prev_block)

        if hash is None:
            hash = self.hash_manager.hash_block(block)
        block.hash = hash

        # Validate block
        self.validator.validate_block(block)

        return block

    def link_prev_block(self, block: Block, prev_block: Block = None):
        """Links the previous block to the current block.
        
        Args:
            block: Block prev_hash of which is set.
            prev_block: Previous Block to link.
                Could be none, in this case it would get reserver value.
                Could be a Block instance, in this case it would acquire a hash of this block.
        """

        if prev_block is None:
            block.prev_hash = self.hash_manager.reserved_prev_hash()

        else:
            block.prev_hash = prev_block.hash


class BlockchainFactory:
    """Class used to instantiate Blockchain class.
    
    Validates fields and throws exceptions if meets invalid arguments.

    Usage:
        Use if you have a whole Blockchain with every Block.
        Otherwise use another class that allows to validate the Blockchain
        sequentially by checking blocks One by One.
    """

    def __init__(self) -> None:
        """Blockchain Factory constructor."""

        # Driver to use Hash Algorithm
        self.hash_manager: HashManager = HashManagerDriver()

        # Validator
        self.validator = BlockchainValidator(self.hash_manager)

    def create_blockchain(self, blocks: List[Block], hash: bytes = None, num: int = None) -> Blockchain:
        """Create a Blockchain with fields and Blocks validation
        
        Args:
            hash: Hash of a Blockchain. Must match a hash of the last Block.
                Set automatically if None.
            num: Number of the last Block in a Blockchain. Argument must match it.
                Set automatically if None.
            blocks: List of Blocks in a Blockchain. List must be ordered in a ascending order.
                List must contain each Block of the Blockchain with no gaps or invalid connections.
                
        Returns:
            Validated Blockchain instance.
            
        Raises:
            InvalidHash: Hash of a Blockchain doesn't match a hash of the last Block.
            InvalidBlockchainNumber: Number of a Blockchain doesn't match a number of the last Block.
            InvalidBlockOrder: List with Blocks is not ascending ordered.
            InvalidLink: When one of blocks references invalid previous Block.
            """

        # Bind arguments
        last_block = blocks[-1]

        if hash is None:
            hash = last_block.hash

        if num is None:
            num = last_block.num

        # Create a Blockchain
        chain = Blockchain(hash, num, blocks)

        # Validate the Blockchain
        self.validator.validate_blockchain(chain)

        return chain