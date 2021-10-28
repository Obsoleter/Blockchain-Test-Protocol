"""Store Blockchain in files"""


from ...storage import StoredBlockchain
from ...blockchain import Block, Blockchain, HashManager
from ...utils.Drivers.hash import HASH_SIZE

import os


class BlockchainFileStorage(StoredBlockchain):
    """Driver for BlockchainStorage.
    
    Implements operations to store Blockchain in files.
    """

    def __init__(self, hash_manager: HashManager, path: str = 'blockchain'):
        """File Storage Constructor.
        
        Reads Blockchain from files. If they don't exist, created new ones.
        """

        self.path = path
        self.hash_manager = hash_manager

        # Read Blockchain from file
        chain = self.read_blockchain_header()

        blocks = []
        for n in range(1, chain.get_num() + 1):
            blocks.append(self.read_block(n))

        # Set up Blockchain
        super().__init__(hash_manager, blocks)

    # Methods to implement
    def get_block(self, num: int) -> Block:
        return super().get_block(num)

    def set_block(self, block: Block, num: int):
        super().set_block(block, num)
        block = super().get_block(num)
        self.write_block(block)
        self.update_header()

    def append_block(self, block: Block):
        super().append_block(block)
        block = super().get_block(len(self))
        self.write_block(block)
        self.update_header()

    def remove_block(self, num: int):
        super().remove_block(num)

        for n in range(num, len(self)):
            block = super().get_block(n)
            self.write_block(block)

        self.update_header()

    # Driver methods
    def update_header(self):
        last_block = super().get_block(len(self))
        header = Blockchain(last_block.get_hash(), last_block.get_num())
        self.write_blockchain_header(header)

    # Paths
    def get_header_path(self):
        path = os.path.join(self.path, 'blockchain')
        return os.path.join(os.getcwd(), path)

    def get_block_path(self, num: int):
        path = os.path.join(self.path, f'block{num}')
        return os.path.join(os.getcwd(), path)

    # Read
    def read_blockchain_header(self) -> Blockchain:
        try:
            with open(self.get_header_path(), 'rb') as header:
                hash = header.read(HASH_SIZE)
                num = int.from_bytes(header.read(4), 'little')

                return Blockchain(hash, num)

        except FileNotFoundError:
            with open(self.get_header_path(), 'wb') as header:
                hash = self.hash_manager.reserved_prev_hash()
                num = 0

                header.write(hash)
                header.write(int.to_bytes(num, 4, 'little'))

                return Blockchain(hash, num)

    def read_block(self, num: int) -> Block:
        with open(self.get_block_path(num), 'rb') as block:
            hash = block.read(HASH_SIZE)
            prev_hash = block.read(HASH_SIZE)
            num = int.from_bytes(block.read(4), 'little')
            data = b''

            byte = block.read(1)
            while byte:
                data += byte
                byte = block.read(1)

            return Block(hash, prev_hash, num, data)

    # Write
    def write_blockchain_header(self, chain: Blockchain):
        with open(self.get_header_path(), 'wb') as header:
            header.write(chain.hash)
            header.write(int.to_bytes(chain.num, 4, 'little'))

    def write_block(self, block: Block):
        with open(self.get_block_path(block.num), 'wb') as file:
            file.write(block.hash)
            file.write(block.prev_hash)
            file.write(int.to_bytes(block.num, 4, 'little'))
            file.write(block.data)