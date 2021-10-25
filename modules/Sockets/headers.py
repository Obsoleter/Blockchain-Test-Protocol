import modules.Header.headers as TestHeaders
import socket


class TestHeaderNetworkManager:
    """Class used to handle network operations related with TestHeaders.
    
    Use this class to Receive and Send packets using TestHeaders.
    """

    def __init__(self, socket: socket.socket) -> None:
        """Network Manager initialization.
        
        Args:
            socket: Destination socket. Any device socket you send data to.
        """

        self.socket = socket

    def send(self, header: TestHeaders.TestMessageHeader) -> int:
        """Sends TestHeader to the network.

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
        return self.socket.send(data)

    def recv(self) -> TestHeaders.TestMessageHeader:
        """Receives TestHeader from the network.
        
        Returns:
            Test header received from the network

        Raises:
            PacketSizeIsOutOfBounds: When received invalid Packet size.
            UnknownOperation: When couldn't decode an operation.
        """

        # Get Packet Size
        size = self.socket.recv(TestHeaders.PACKET_SIZE_BYTES)
        size = int.from_bytes(size, 'little')

        if size > TestHeaders.PACKET_MAX_SIZE:
            raise TestHeaders.PacketSizeIsOutOfBounds('Received invalid Packet size!')

        # Get Packet
        data = self.socket.recv(size)

        # Decode operation
        operation = None
        for allowed_operation in TestHeaders.ALLOWED_OPERATIONS:
            header_operation = data[0:len(allowed_operation)]

            if header_operation == allowed_operation:
                operation = header_operation
                break

        if operation is None:
            raise TestHeaders.UnknownOperation('Couldn\'t decode Packet operation!')

        # Get Data
        payload = data[len(operation):-len(TestHeaders.HEADER_PACKET_END_DELIMITER)]
        delimiter = data[-len(TestHeaders.HEADER_PACKET_END_DELIMITER):]

        # Collect received data to the TestHeader
        header = TestHeaders.TestMessageHeader(size, operation, payload, delimiter)

        return header