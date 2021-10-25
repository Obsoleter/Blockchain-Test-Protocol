import modules.Header.headers as TestHeaders
import socket


class TestHeaderNetworkManager:
    """Class used to handle network operations related with TestHeaders.
    
    Use this class to Receive and Send packets using TestHeaders.

    Doesn't validate TestHeaders! It assumes you're already using valid TestHeaders!
    """

    def __init__(self, socket: socket.socket) -> None:
        """Network Manager initialization.
        
        Args:
            socket: Destination socket.
        """

        self.socket = socket

    def send(self, header: TestHeaders.TestMessageHeader) -> int:
        """Sends TestHeader to the network.
        
        Doesn't check a TestHeader to correspond the protocol!

        Args:
            header: TestHeader to be sent.

        Returns:
            Returns whatever socket.send function returns.
        """

        data = b''
        data += header.operation
        data += header.payload
        data += header.delimiter

        # Send the Packet size
        size = int.to_bytes(header.size, 2, 'little')
        self.socket.send(size)

        # Send the Packet itself
        self.socket.send(data)

    def recv(self) -> TestHeaders.TestMessageHeader:
        """Receives TestHeader from the network.
        
        Doesn't check a TestHeader to correspond the protocol!
        
        Returns:
            Test header received from the network
        """

        # Get Packet Size
        size = self.socket.recv(TestHeaders.PACKET_SIZE_BYTES)
        size = int.from_bytes(size, 'little')

        if size > TestHeaders.PACKET_MAX_SIZE:
            raise TestHeaders.TestMessageHeader.PacketSizeIsOutOfBounds('Received invalid Packet size!')

        # Get Packet
        data = self.socket.recv(size)

        # Find operation
        operation = None
        for allowed_operation in TestHeaders.TestMessageHeader.ALLOWED_OPERATIONS:
            header_operation = data[0:len(allowed_operation)]

            if header_operation == allowed_operation:
                operation = header_operation
                break

        if operation is None:
            raise TestHeaders.TestMessageHeader.UnknownOperation('Unknown client operation!')

        # Get Data
        payload = data[len(operation):-len(TestHeaders.HEADER_PACKET_END_DELIMITER)]
        delimiter = data[-len(TestHeaders.HEADER_PACKET_END_DELIMITER):]

        header = TestHeaders.TestMessageHeader(size, operation, payload, delimiter)

        return header