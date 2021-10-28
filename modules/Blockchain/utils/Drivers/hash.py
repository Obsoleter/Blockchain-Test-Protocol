import hashlib
from ...blockchain import Block, HashManager


HASH_ALGORITHM = hashlib.sha1
"""Represents the Constructor for Hash algorithm."""

HASH_SIZE = HASH_ALGORITHM().digest_size
"""Size of Hash algorithm"""


class HashManagerDriver(HashManager):
    """Concrete class for Blockchain Hash Manager abstract class.

    Implements the Driver for using hashlib Hash Algorithms.
    
    Implements abstract HashManager class.
    """

    def hash(self, data: bytes) -> bytes:
        hash = HASH_ALGORITHM(data)
        return hash.digest()


    def is_valid_hash(self, hash: bytes) -> bool:
        return len(hash) == HASH_SIZE


    def hash_block(self, block: Block) -> bytes:
        hash = HASH_ALGORITHM(block.prev_hash + int.to_bytes(block.num, 2, 'little') + block.data).digest()
        return hash

    def reserved_prev_hash(self) -> bytes:
        return b'\x00' * HASH_SIZE