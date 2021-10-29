from ..header import ProtocolPacket
from ..header import PayloadSizeIsOutOfBounds, PacketEndDelimiterIsMissing, PacketSizeIsOutOfBounds
from ..header import PacketSizeDiffersFromGivenValue, UnknownOperation


class BaseProtocolPacket(ProtocolPacket):
    """Class implementing base structure and operations.

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
        b'SERVER_ACCEPT',
        b'SERVER_DENY'
    )
    """Protocol Allowed Operations."""

    def __init__(self, operation: bytes, payload: bytes = b'', delimiter: bytes = ProtocolPacket.HEADER_PACKET_END_DELIMITER, size: int = None) -> None:
        """TestHeader constructor.
        
        Args:
            size: Tells how much bytes to receive to get the Respond.
                The size of operation + payload + delimiter fields.
                Field size itself is 2 bytes
            operation: Determines the operation a Device wants to operate.
                Used to show what the Device wants to get or make completed.
            payload: Any information, corresponding to the Operation.
                Used to describe an exact thing a Device wants to achieve.
            delimiter: Used to determine the end of Packet and Payload section themselves.

        Raises:
            UnknownOperation: Used unknown operation in the operation field.
            PayloadSizeIsOutOfBounds: The size of the payload is greater than HEADER_PAYLOAD_MAX_SIZE
            PacketEndDelimiterIsMissing: There's no HEADER_PAYLOAD_END_DELIMITER
                determed in the end of payload field.
            PacketSizeIsOutOfBounds: Packet size is greater than PACKET_MAX_SIZE.
        """

        if operation not in self.ALLOWED_OPERATIONS:
            raise UnknownOperation('Unknown operation has been given!')

        if len(payload) > ProtocolPacket.HEADER_PAYLOAD_MAX_SIZE:
            raise PayloadSizeIsOutOfBounds('Payload size is out of bounds!')

        if delimiter != ProtocolPacket.HEADER_PACKET_END_DELIMITER:
            raise PacketEndDelimiterIsMissing('Packet end delimiter is missing!')

        self.operation = operation
        self.payload = payload
        self.delimiter = delimiter

        if size is None:
            self.size = self.calculate_size()
        else:
            if size > ProtocolPacket.PACKET_MAX_SIZE:
                raise PacketSizeIsOutOfBounds('Packet size is out of bounds!')

            elif size != self.calculate_size():
                raise PacketSizeDiffersFromGivenValue('Size argument value differs from the current packet size!')

            self.size = size

    def calculate_size(self) -> int:
        """Calculates the size of packet.

        Returns:
            Calculated size.

        Raises:
            PacketSizeIsOutOfBounds: New calculated size is bigger its maximum allowed value.
        """

        size = len(self.operation) + len(self.payload) + len(self.delimiter)
        if size > ProtocolPacket.PACKET_MAX_SIZE:
            raise PacketSizeIsOutOfBounds('New Packet size is out of bounds!')
        else:
            return size