from .header import BlockchainProtocolPacket
from modules.Blockchain.blockchain import Block, Blockchain


# New Block related operations
class BlockAdd(BlockchainProtocolPacket):
    """Offer new Block operation."""

    def __init__(self, block: Block) -> None:
        """Operation constructor."""

        data = b''
        data += int.to_bytes(block.get_num(), 2, 'little')
        data += block.get_hash()
        data += block.get_prev_hash()
        data += block.get_data()

        super().__init__(b'BLOCK_ADD', data)


class BlockSpread(BlockchainProtocolPacket):
    """Spread Block operation."""

    def __init__(self, block: Block) -> None:
        """Operation constructor."""

        data = b''
        data += int.to_bytes(block.get_num(), 2, 'little')
        data += block.get_hash()
        data += block.get_prev_hash()
        data += block.get_data()

        super().__init__(b'BLOCK_SPREAD', data)


# Ledger related operations
class LedgerAskHeader(BlockchainProtocolPacket):
    """Get Ledger information operation."""

    def __init__(self) -> None:
        """Operation constructor."""

        super().__init__(b'LEDGER_ASK_HEADER')


class LedgerRespondHeader(BlockchainProtocolPacket):
    """Give Ledger information operation."""

    def __init__(self, header: Blockchain) -> None:
        """Operation constructor."""

        data = b''
        data += int.to_bytes(header.get_num(), 2, 'little')
        data += header.get_hash()

        super().__init__(b'LEDGER_RESPOND_HEADER', data)


# Ledger transfering operations
class LedgerAsk(BlockchainProtocolPacket):
    """Ledger Ask operation.
    
    Sends All Blocks from the end.
    """

    def __init__(self) -> None:
        """Operation constructor."""

        super().__init__(b'LEDGER_ASK')


class LedgerAskBlock(BlockchainProtocolPacket):
    """Ledger Ask Block operation.
    
    Asks for Block with specific number.
    """

    def __init__(self, block: Block) -> None:
        """Operation constructor."""

        data = b''
        data += int.to_bytes(block.get_num(), 2, 'little')

        super().__init__(b'LEDGER_ASK_BLOCK', data)


class LedgerRespondBlock(BlockchainProtocolPacket):
    """Ledger Ask Block operation.
    
    Asks for Block with specific number.
    """

    def __init__(self, block: Block) -> None:
        """Operation constructor."""

        data = b''
        data += int.to_bytes(block.get_num(), 2, 'little')
        data += block.get_hash()
        data += block.get_prev_hash()
        data += block.get_data()

        super().__init__(b'LEDGER_RESPOND_BLOCK', data)