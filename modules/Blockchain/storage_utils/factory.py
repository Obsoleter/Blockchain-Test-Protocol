from ..storage import StoredBlockchain, Blockchain
from .Drivers.file import BlockchainFileStorage
from ..utils.Drivers.hash import HashManagerDriver


class StoredBlockchainFactory:
    """Class that incapsulates BlockchainStorage creation logic.
    
    Gives all dependencies BlockchainStorage needs.
    """

    def __init__(self) -> None:
        """Factory constructor."""

    def create(self, path: str = 'blockchain') -> Blockchain:
        """Creates storage for Blockchain."""

        # Dependencies
        hash_manager = HashManagerDriver()

        return BlockchainFileStorage(hash_manager, path)