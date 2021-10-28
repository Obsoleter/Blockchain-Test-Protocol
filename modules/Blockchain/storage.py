from typing import List
from .validated_blockchain import Block, Blockchain, ValidatedBlockchain, HashManager


class StoredBlockchain(ValidatedBlockchain):
    """Abstract class that implements abstract storage for Blockchain.
    
    Syncronizes every operation of Blockchain with storage.

    If operation doesn't throw an exception, changes would be applied to the storage.
    """

    def __init__(self, hash_manager: HashManager, blocks: List[Block]):
        """Loads Blockchain from the storage.
        
        If nothing found, creates the new one.
        """
        super().__init__(hash_manager, blocks)

    def get_block(self, num: int) -> Block:
        """Get a Block in the Blockchain.
        
        Args:
            index: Number of block.
            
        Returns:
            Block by index.

        Raises:
            InvalidBlockNumber: Block number is out of bounds!
        """

        return super().get_block(num)

    def set_block(self, block: Block, num: int):
        """Set a Block in the Blockchain.
        
        Args:
            block: New block.
            index: Number of block.

        Raises:
            InvalidBlockNumber: Block number is out of bounds!
        """

        super().set_block(block, num)

    def append_block(self, block: Block):
        """Appends a block to the end of Blockchain.
        
        Args:
            block: Block to append.
        """

        super().append_block(block)

    def remove_block(self, num: int):
        """Removes a block from the Blockchain.
        
        Args:
            num: Number of block.
            
        Raises:
            InvalidBlockNumber: Block number is out of bounds!
        """

        super().remove_block(num)