import socket
import threading
import concurrent.futures


HEADER_OPERATION_MAX_SIZE = 32
"""Maximum TestHeader Operation field size"""

HEADER_PAYLOAD_MAX_SIZE = 1024
"""Maximum Payload size.

Excludes Header size and End of packet.
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
"""Determines the Maximum size of Packet
"""

PACKET_SIZE_BYTES = 2
"""The Size of Size Field itself.

This constant is used for Packet transfer
"""

HEADER_DATA_CODING = 'utf-8'
"""Determines used Coding for a packet transfer.
"""

class TestMessageHeader:
    """Abstract Class determining the structure of a message sent among the Test network.

    Use Concrete Classes determining the exact operations.

    Structure:
        size: Tells how much bytes to receive to get the Respond.
            The size of operation + payload + delimiter fields.
            Field size itself is 2 bytes
        operation: Determines the operation a Device wants to operate.
            Used to show what the Device wants to get or make completed.
        payload: Any information, corresponding to the Operation.
            Used to describe an exact thing a Device wants to achieve.
        delimiter: Used to mark the end of Packet.
    """

    ALLOWED_OPERATIONS = (
        b'CLIENT_CONNECT',
        b'CLIENT_GET',
        b'CLIENT_OK',

        b'SERVER_CONNECTED',
        b'SERVER_SENT',
        b'SERVER_DISCONNECTED'
    )

    class UnknownOperation(Exception):
        """Used unknown operation in the operation field."""

    class PayloadSizeIsOutOfBounds(Exception):
        """The size of the payload is greater than HEADER_PAYLOAD_MAX_SIZE."""

    class PacketEndDelimiterIsMissing(Exception):
        """There's no HEADER_PACKET_END_DELIMITER determed.
        This probably tells that packet was corrupted.
        """

    class PacketSizeIsOutOfBounds(Exception):
        """The size of a Packet is greater than PACKET_MAX_SIZE"""

    def __init__(self, size: int, operation: bytes, payload: bytes = b'', delimiter: bytes = HEADER_PACKET_END_DELIMITER) -> None:
        """Message constructor.
        
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
        """

        if size > PACKET_MAX_SIZE:
            raise TestMessageHeader.PacketSizeIsOutOfBounds('Packet size is out of bounds!')

        if operation not in TestMessageHeader.ALLOWED_OPERATIONS:
            raise TestMessageHeader.UnknownOperation('Unknown operation has been given!')

        if len(payload) > HEADER_PAYLOAD_MAX_SIZE:
            raise TestMessageHeader.PayloadSizeIsOutOfBounds('Payload size is out of bounds!')

        if delimiter != HEADER_PACKET_END_DELIMITER:
            raise TestMessageHeader.PacketEndDelimiterIsMissing('Packet end delimiter is missing!')

        self.size = size
        self.operation = operation
        self.payload = payload
        self.delimiter = delimiter

    def calculate_size(self):
        """Calculates the size of packet.
        
        Use if you create TestHeader to send.

        Affects self.size

        Raises:
            PacketSizeIsOutOfBounds: New calculated size is bigger its maximum allowed value.
        """

        size = len(self.operation) + len(self.payload) + len(self.delimiter)
        if size > PACKET_MAX_SIZE:
            raise TestMessageHeader.PacketSizeIsOutOfBounds('New Packet size is out of bounds!')
        else:
            self.size = size


# Client Operations
class TestOperationClientConnect(TestMessageHeader):
    """Class describing the operation CLIENT_CONNECT.
    
    Used by client to send after a successful TCP connection with server.

    Shows that client is alive and understands the Protocol.
    If is not sent, connection would be closed.
    """

    def __init__(self) -> None:
        """Instantiates CLIENT_CONNECT kind of Message"""

        TestMessageHeader.__init__(self, 0, b'CLIENT_CONNECT')
        self.calculate_size()


class TestOperationClientGet(TestMessageHeader):
    """Class describing the operation CLIENT_GET.
    
    Used by client to Get a respond from the server
    """

    def __init__(self) -> None:
        """Instantiates CLIENT_GET kind of Message"""

        TestMessageHeader.__init__(self, 0, b'CLIENT_GET')
        self.calculate_size()


class TestOperationClientOk(TestMessageHeader):
    """Class describing the operation CLIENT_OK.
    
    Used by client to confirm Server Action
    """

    def __init__(self) -> None:
        """Instantiates CLIENT_OK kind of Message"""

        TestMessageHeader.__init__(self, 0, b'CLIENT_OK')
        self.calculate_size()


# Server Operations
class TestOperationServerConnected(TestMessageHeader):
    """Class describing the operation SERVER_CONNECTED.
    
    Used by server to tell a client that connection is established
    """

    def __init__(self) -> None:
        """Instantiates SERVER_CONNECTED kind of Message"""

        TestMessageHeader.__init__(self, 0, b'SERVER_CONNECTED')
        self.calculate_size()


class TestOperationServerSent(TestMessageHeader):
    """Class describing the operation SERVER_SENT.
    
    Used by server to send a data to client
    """

    def __init__(self, payload: bytes) -> None:
        """Instantiates SERVER_SENT kind of Message
        
        Args:
            payload: Payload to be sent.
        """

        TestMessageHeader.__init__(self, 0, b'SERVER_SENT', payload)
        self.calculate_size()


class TestOperationServerDisconnected(TestMessageHeader):
    """Class describing the operation SERVER_DISCONNECTED.
    
    Used by server to tell a client that connection is dropped
    """

    def __init__(self) -> None:
        """Instantiates SERVER_DISCONNECTED kind of Message"""

        TestMessageHeader.__init__(self, 0, b'SERVER_DISCONNECTED')
        self.calculate_size()