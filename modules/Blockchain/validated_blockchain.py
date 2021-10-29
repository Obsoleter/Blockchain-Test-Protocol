from typing import List
from .blockchain import Block, Blockchain, HashManager


class ValidatedBlockchain(Blockchain):
    """Validated Blockchain class.
    
    Usage:
        Each operation with this class is validated to prevent invalid Blockchain.
        
        Could be used as Blockchain instance.
    """

    def recalculate_blockchain(self, start: int):
        """Recalculates blocks in a Blockchain from start to end.
        
        Args:
            start: Block number to start with.
        """

        index = start - 1
        self.check_index(index)

        if index == 0:
            prev_block = self.hash_manager.reserved_prev_hash()

        else:
            prev_block = self.blocks[index - 1]


        for i in range(index, len(self)):
            block = self.blocks[i]
            block.link_prev_block(prev_block)
            block.set_num(i + 1)
            block.hash = self.hash_manager.hash_block(block)

            prev_block = block


        self.hash = self.blocks[-1].hash
        self.num = self.blocks[-1].num

    def __init__(self, hash_manager: HashManager, blocks: List[Block] = []) -> None:
        """Validated Blockchain constructor.
        
        Args:
            blocks: List of Blocks to store. Blocks would be recalculated. Could be empty.
        """

        self.hash_manager = hash_manager

        if len(blocks) > 0:
            self.blocks = blocks
            self.recalculate_blockchain(1)

        else:
            self.hash = self.hash_manager.reserved_prev_hash()
            self.num = 0
            self.blocks = []

    def get_block(self, num: int) -> Block:
        """Get a Block in the Blockchain.
        
        Args:
            num: Number of block.
            
        Returns:
            Block by number.

        Raises:
            InvalidBlockNumber: Block number is out of bounds!
        """

        return super().get_block(num - 1)

    def set_block(self, block: Block, num: int):
        """Set a Block in the Blockchain.
        
        Args:
            block: New block.
            num: Number of block.

        Raises:
            InvalidBlockNumber: Block number is out of bounds!
        """

        super().set_block(block, num - 1)
        self.recalculate_blockchain(num)

    def append_block(self, block: Block):
        """Appends a block to the end of Blockchain.
        
        Args:
            block: Block to append.
        """

        super().append_block(block)
        self.recalculate_blockchain(len(self))

    def remove_block(self, num: int):
        """Removes a block from the Blockchain.
        
        Args:
            num: Number of block.
            
        Raises:
            InvalidBlockNumber: Block number is out of bounds!
        """

        super().remove_block(num - 1)
        
        if num <= len(self):
            self.recalculate_blockchain(num)

    def clear(self):
        """Clears Blockchain."""

        super().clear()
        self.hash = self.hash_manager.reserved_prev_hash()
        self.num = 0