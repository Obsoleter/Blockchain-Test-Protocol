from ..base.header import BaseProtocolPacket


class BlockchainProtocolPacket(BaseProtocolPacket):
    """Class allowing Blockchain operations.

    Methods Validate fields.

    Structure:
        size: Tells how much bytes to receive to get the Respond.
            The size of operation + payload + delimiter fields.
            Field size itself is told by PACKET_SIZE_BYTES.
        operation: Determines the operation a Device wants to operate.
            Used to show what the Device wants to get or make completed.
        payload: Any information, corresponding to the Operation.
            Used to describe an exact thing a Device wants to achieve.
        delimiter: Used to mark the end of Packet.
    """

    ALLOWED_OPERATIONS = (
        *BaseProtocolPacket.ALLOWED_OPERATIONS,
        b'BLOCK_SPREAD',
        b'BLOCK_ADD',
        b'LEDGER_RESPOND_HEADER',
        b'LEDGER_RESPOND_BLOCK',
        b'LEDGER_ASK_HEADER',
        b'LEDGER_ASK_BLOCK',
        b'LEDGER_ASK',
    )
    """Protocol Allowed Operations."""

    PACKET_BLOCK_SIZE_BYTES = 2
    """Bytes Size of Block Size"""