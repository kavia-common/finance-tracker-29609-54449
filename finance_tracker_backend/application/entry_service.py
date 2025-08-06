"""
Application service orchestrating finance entry use cases.
"""

from typing import Optional, List
from ..domain.finance_entry.entities import FinanceEntry
from ..domain.finance_entry.repository import FinanceEntryRepository

# PUBLIC_INTERFACE
class FinanceEntryService:
    """
    Application-layer service for managing finance entries orchestrating domain, repo, and business rules.
    """

    def __init__(self, repo: FinanceEntryRepository):
        self.repo = repo

    # PUBLIC_INTERFACE
    def list(self) -> List[FinanceEntry]:
        return self.repo.list_entries()

    # PUBLIC_INTERFACE
    def get(self, entry_id: int) -> Optional[FinanceEntry]:
        return self.repo.get_by_id(entry_id)

    # PUBLIC_INTERFACE
    def create(self, description, amount, category, entry_date) -> FinanceEntry:
        entry = FinanceEntry(
            id=None,
            description=description,
            amount=float(amount),
            category=category,
            entry_date=entry_date
        )
        return self.repo.add(entry)

    # PUBLIC_INTERFACE
    def update(self, entry_id, **kwargs) -> FinanceEntry:
        entry = self.repo.get_by_id(entry_id)
        if not entry:
            raise ValueError("Not found")
        for field in ["description", "amount", "category", "date"]:
            if field in kwargs and kwargs[field] is not None:
                setattr(entry, field, kwargs[field])
        return self.repo.update(entry)

    # PUBLIC_INTERFACE
    def delete(self, entry_id) -> bool:
        return self.repo.delete(entry_id)
