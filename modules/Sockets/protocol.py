from typing import Type
from modules.Protocol.header import ProtocolPacket
import modules.Protocol.header as protocol

import socket


class ProtocolNetworkManager:
    """Class used to handle network operations related with Protocol.
    
    Use this class to Receive and Send Protocol Packets.
    """

    def __init__(self, socket: socket.socket, PACKET: Type) -> None:
        """Network Manager initialization.
        
        Args:
            socket: Destination socket. Any device socket you send data to.
        """

        self.socket = socket
        self.PACKET = PACKET

    def send(self, header: ProtocolPacket) -> int:
        """Sends Protocol Packet to the network.

        Args:
            header: Packet to be sent.

        Returns:
            Returns whatever socket.send function returns.
        """

        data = b''
        data += header.operation
        data += header.payload
        data += header.delimiter

        # Send the Packet size
        size = int.to_bytes(header.size, self.PACKET.PACKET_SIZE_BYTES, 'little')
        self.socket.send(size)

        # Send the Packet itself
        return self.socket.send(data)

    def recv(self) -> ProtocolPacket:
        """Receives Protocol Packet from the network.
        
        Returns:
            Test header received from the network

        Raises:
            PacketSizeIsOutOfBounds: When received invalid Packet size.
            UnknownOperation: When couldn't decode an operation.
        """

        # Get Packet Size
        size = self.socket.recv(self.PACKET.PACKET_SIZE_BYTES)
        size = int.from_bytes(size, 'little')

        if size > self.PACKET.PACKET_MAX_SIZE:
            raise protocol.PacketSizeIsOutOfBounds('Packet size is too big!')

        # Get Packet
        data = self.socket.recv(size)

        if len(data) != size:
            raise protocol.PacketSizeDiffersFromGivenValue(f'Got {len(data)} bytes. Expected {size} bytes!')

        # Decode operation
        operation = None
        for allowed_operation in self.PACKET.ALLOWED_OPERATIONS:
            header_operation = data[0:len(allowed_operation)]

            if header_operation == allowed_operation:
                operation = header_operation
                break

        if operation is None:
            raise protocol.UnknownOperation('Couldn\'t decode Packet operation!')

        # Get Data
        payload = data[len(operation):-len(self.PACKET.HEADER_PACKET_END_DELIMITER)]
        delimiter = data[-len(self.PACKET.HEADER_PACKET_END_DELIMITER):]

        # Collect received data to the TestHeader
        header = self.PACKET(size=size, operation=operation, payload=payload, delimiter=delimiter)

        return header