"""
Repository contract for FinanceEntry aggregate.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import FinanceEntry

# PUBLIC_INTERFACE
class FinanceEntryRepository(ABC):
    """Repository interface for FinanceEntry aggregates."""

    @abstractmethod
    def list_entries(self) -> list:
        """Return all finance entries."""
        pass

    @abstractmethod
    def get_by_id(self, entry_id: int) -> Optional[FinanceEntry]:
        """Find entry by ID."""
        pass

    @abstractmethod
    def add(self, entry: FinanceEntry) -> FinanceEntry:
        """Add a new FinanceEntry."""
        pass

    @abstractmethod
    def update(self, entry: FinanceEntry) -> FinanceEntry:
        """Update an existing FinanceEntry."""
        pass

    @abstractmethod
    def delete(self, entry_id: int) -> bool:
        """Delete an entry by ID."""
        pass
