from .blockchain import Blockchain, Block, HashManager

# Import Raises
from .blockchain import InvalidHash, InvalidBlockOrder, InvalidBlockchainNumber, InvalidLink, InvalidBlockNumber


class BlockchainValidator:
    """Class checking a Blockchain or a Block for Validity"""

    def __init__(self, hash_manager: HashManager) -> None:
        """Blockchain Validator constructor.
        
        Args:
            hash_manager: Hash Manager to use for validation
        """

        self.hash_manager = hash_manager

    def validate_block_by_number(self, chain: Blockchain, num: int):
        """Checks if a block number is valid and not out of bounds.
        
        Throws exception if is not.
        
        Args:
            chain: Blockchain to find a block in.
            num: Number of block to check.
            
        Raises:
            InvalidBlockNumber: Invalid block number was given or block with this num doesn't exist.
        """

        if num < 1 or num > chain.num:
            raise InvalidBlockNumber(f"Invalid block number: {num}!")

    def validate_block(self, block: Block):
        """Function validating a block.
        
        If block hasn't passed the validation, function will throw an exception.
        
        Args:
            block: Block to validate.
            
        Raises:
            InvalidBlockNumber: Thrown when a block has an invalid number.
            InvalidHash: Thrown when a hash of a block doesn't match a hash in field
                or if some of hashes is invalid.
        """

        # Check num
        if block.num < 1:
            raise InvalidBlockNumber("New number of block is less than 1!")

         # Check prev_hash
        if not self.hash_manager.is_valid_hash(block.prev_hash):
            raise InvalidHash('prev_field hash format is not appropriated for the current algorithm!')

        # Check hash
        if block.hash != self.hash_manager.hash_block(block):
            raise InvalidHash('Hash argument doesn\'t match a hash of block!')

    def validate_blockchain(self, chain: Blockchain):
        """Function validating a blockchain.
        
        If blockchain hasn't passed the validation, function will throw an exception.
        
        Args:
            chain: Blockchain to validate.
            
        Raises:
            InvalidHash: Hash of a Blockchain doesn't match a hash of the last Block.
            InvalidBlockchainNumber: Number of a Blockchain doesn't match a number of the last Block.
            InvalidBlockOrder: List with Blocks is not ascending ordered or with gaps.
            InvalidLink: When one of blocks references invalid previous Block.
        """

        # Handle empty Blockchain
        if len(chain.blocks) == 0:
            if chain.hash != self.hash_manager.reserved_prev_hash():
                raise InvalidHash("Hash of a Blockchain has invalid value.")

            if chain.num != 0:
                raise InvalidBlockchainNumber("Number of a Blockchain is invalid.")

            return

        # Get the last Block and validate fields
        last_block = chain.blocks[-1]

        if chain.hash != last_block.hash:
            raise InvalidHash("Hash of a Blockchain doesn't match a hash of the last Block.")

        if chain.num != last_block.num:
            raise InvalidBlockchainNumber("Number of a Blockchain doesn't match a number of the last Block.")

        # Check the chain for blocks order and links
        prev_hash = None
        try:
            for n in range(chain.num, 0, -1):
                block = chain.blocks[n - 1]

                # Check block order
                if n != block.num:
                    raise InvalidBlockOrder("List of blocks is not ordered!")

                # Check the link
                elif prev_hash is None:
                    pass
                
                elif prev_hash != block.hash:
                    raise InvalidLink(f"Found invalid pointer from block {block.num + 1} to block {block.num}!")

                # Check the block
                self.validate_block(block)

                # Save hash for links validation
                prev_hash = block.prev_hash

        except (InvalidBlockOrder, InvalidLink, InvalidHash):
            raise

        except Exception as e:
            raise InvalidBlockOrder("List of blocks is not ordered or with gaps!") from e

        # Check the first block prev_hash field
        if chain.blocks[0].prev_hash != self.hash_manager.reserved_prev_hash():
            raise InvalidLink("Invalid Previous Hash value of the First block!")