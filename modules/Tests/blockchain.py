from modules.Blockchain.blockchain import Block, Blockchain
import modules.Blockchain.validation_utils.factories as factory
import modules.Blockchain.storage_utils.factory as storage_factory


def print_block(block: Block):
    print('==========')
    print(block.num)
    print(block.hash)
    print(block.prev_hash)
    print(block.data)
    print('==========')

def print_blockchain(chain: Blockchain):
    print('``````````')
    print(chain.num)
    print(chain.hash)
    for block in chain.blocks:
        print_block(block)
    print('``````````')



# Test Blockchain
# chain_factory = storage_factory.StoredBlockchainFactory()
# chain = chain_factory.create_storage()

# chain.append_block(Block(b'', b'', 2, b"Pog"))
# chain.append_block(Block(b'', b'', 2, b"Pog Champ!"))
# chain.append_block(Block(b'', b'', 2, b"Hi!"))

# chain.set_block(chain.get_block(3), 2)

# print_blockchain(chain)