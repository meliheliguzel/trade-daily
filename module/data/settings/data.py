from abc import ABC, abstractmethod
from collections.abc import Callable


class IDataEntity(ABC):
    ...

class IDataManager(ABC):

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def add(self, item: IDataEntity | dict) -> bool:
        """Add a new item."""
        ...

    @abstractmethod
    def remove(self, identifier: str) -> bool:
        """Remove an item by identifier."""
        ...

    @abstractmethod
    def update(self, identifier: str, **kwargs) -> bool:
        """Update an item by identifier."""
        ...

    @abstractmethod
    def find(self, identifier: str) -> IDataEntity | None:
        """Find an item by identifier."""
        ...

    @abstractmethod
    def list_all(self) -> list[IDataEntity]:
        """List all items."""
        ...

    @abstractmethod
    def sort_by(self, attribute: str, reverse: bool = False) -> list[IDataEntity]:
        """Sort items by a specified attribute."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Return the total count of items."""
        ...

    @abstractmethod
    def filter(self, criteria: Callable[[IDataEntity], bool]) -> list[IDataEntity]:
        """Filter items based on criteria."""
        ...

    @abstractmethod
    def exists(self, identifier: str) -> bool:
        """Check if an item exists by identifier."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all items."""
        ...

    @abstractmethod
    def save(self, filepath: str) -> None:
        """Save items to a file."""
        ...

    @abstractmethod
    def load(self, filepath: str) -> bool:
        """Load items from a file."""
        ...
