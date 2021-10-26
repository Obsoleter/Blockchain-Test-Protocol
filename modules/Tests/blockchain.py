from modules.Blockchain.blockchain import Block, Blockchain
import modules.Blockchain.blockchain_factory as factory


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


blocks = []

# Block 1
num = 1
data = b"Hello baka!"
block1 = factory.BlockFactory().create_block(num, data)
blocks.append(block1)


# Block 2
num = 2
data = b"Sussy baka!"
block2 = factory.BlockFactory().create_block(num, data, block1)
blocks.append(block2)


# Block 3
num = 3
data = b"Choosen one!"
block3 = factory.BlockFactory().create_block(num, data, block2)
blocks.append(block3)


# Blockchain
chain = factory.BlockchainFactory().create_blockchain(blocks)
print_blockchain(chain)