# Protocol Raises
class ProtocolException(Exception):
    """Base Test Protocol Exception.

    Every Test Protocol Exception Class inherits this class.
    
    Used to catch any Exception related to the Protocol
    """

class UnknownOperation(ProtocolException):
    """Used unknown operation in the operation field."""

class PayloadSizeIsOutOfBounds(ProtocolException):
    """The size of the payload is greater than HEADER_PAYLOAD_MAX_SIZE."""

class PacketEndDelimiterIsMissing(ProtocolException):
    """There's no HEADER_PACKET_END_DELIMITER determined.
    This highly likely tells that packet was corrupted.
    """

class PacketSizeIsOutOfBounds(ProtocolException):
    """The size of a Packet is greater than PACKET_MAX_SIZE"""

class PacketSizeDiffersFromGivenValue(ProtocolException):
    """Thrown when size of received packet doesn't matcn received
    packet size field.
    """


class ProtocolPacket:
    """Structure Class determining the structure of a protocol packet.

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

    HEADER_OPERATION_MAX_SIZE = 32
    """Maximum Operation field size."""

    HEADER_PAYLOAD_MAX_SIZE = 1024
    """Maximum Payload size.

    Affected payload field only.
    """

    HEADER_PACKET_END_DELIMITER = b'\r\n'
    """Sign showing the end of Packet.

    Message counts as valid if End Delimiter is met.
    Otherwise a Packet is thrown away.
    """

    PACKET_MAX_SIZE = (
                HEADER_OPERATION_MAX_SIZE + 
                HEADER_PAYLOAD_MAX_SIZE + 
                len(HEADER_PACKET_END_DELIMITER)
                )
    """Determines the Maximum size of Packet."""

    PACKET_SIZE_BYTES = 2
    """The Size of Size Field itself.

    This constant is used for Packet transfer.
    """

    HEADER_DATA_CODING = 'utf-8'
    """Determines used Coding for a packet transfer."""

    def __init__(self, size: int, operation: bytes, payload: bytes = b'', delimiter: bytes = HEADER_PACKET_END_DELIMITER) -> None:
        """Packet constructor.
        
        Args:
            size: Tells how much bytes to receive to get the Respond.
                The size of operation + payload + delimiter fields.
                Field size itself is PACKET_SIZE_BYTES
            operation: Determines the operation a Device wants to operate.
                Used to show what the Device wants to get or make completed.
            payload: Any information, corresponding to the Operation.
                Used to describe an exact thing a Device wants to achieve.
            delimiter: Used to determine the end of Packet and Payload section themselves.
        """

        self.operation = operation
        self.payload = payload
        self.delimiter = delimiter
        self.size = size

    def calculate_size(self) -> int:
        """Calculates the size of packet.

        Returns:
            Calculated size.
        """

        size = len(self.operation) + len(self.payload) + len(self.delimiter)
        return size