"""
FinanceEntry entity for Domain Layer.
Domain entity is decoupled from persistence/ORM specifics.
"""

from datetime import date

# PUBLIC_INTERFACE
class FinanceEntry:
    """Domain entity for finance entry (Aggregate Root)."""
    def __init__(self, id: int, description: str, amount: float, category: str, entry_date: date):
        self.id = id
        self.description = description
        self.amount = amount
        self.category = category
        self.date = entry_date

    # PUBLIC_INTERFACE
    def as_dict(self):
        """Return dictionary representation for serialization."""
        return dict(
            id=self.id,
            description=self.description,
            amount=self.amount,
            category=self.category,
            date=self.date.isoformat()
        )
