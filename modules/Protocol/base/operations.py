from .header import BaseProtocolPacket


# Basic operations
class ServerAccept(BaseProtocolPacket):
    """Server Accept operation.
    
    Used to show that operation was accepted.
    """

    def __init__(self) -> None:
        """Operation constructor."""

        super().__init__(b'SERVER_ACCEPT')


class ServerDeny(BaseProtocolPacket):
    """Server Deny operation.
    
    Shows that operation was denied.
    """

    def __init__(self, reason: bytes = b'') -> None:
        """Operation constructor."""

        super().__init__(b'SERVER_DENY', reason)