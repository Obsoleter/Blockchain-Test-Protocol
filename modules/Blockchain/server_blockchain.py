from typing import List
from .blockchain import Block, Blockchain
from .validator import BlockchainValidator


class ServerBlockchain(Blockchain):
    """Class for Downloadling Blockchain.
    
    It implements operation Insert Block that inserts blocks
    from the end and validates insertion.
    """

    def __init__(self, validator: BlockchainValidator, header: Blockchain) -> None:
        """Class constructor.
        
        Sets up everything for downloading Blockchain.
        
        Args:
            header: Blockchain header to start to download which.
        """

        self.validator = validator
        super().__init__(header.hash, header.num)

    def insert_block(self, block: Block) -> bool:
        """Inserts downloaded block to the start of blocks list.
        
        Validates block insertion.
        
        Args:
            block: Block to insert in the Blockchain.

        Returns:
            True if Blockchain still needs to be downloaded.
            False if Blockchain is filled and it was the first block.

        Raises:
            InvalidLink: Inserted block doesn't match blockchain.
            InvalidHash: Inserted block has invalid hash.
        """

        self.validator.validate_block(block)

        if len(self) == 0:
            self.validator.validate_link(block, self)

        else:
            next_block = self.blocks[0]
            self.validator.validate_link(block, next_block)

        self.blocks.insert(0, block)

        return block.num != 1