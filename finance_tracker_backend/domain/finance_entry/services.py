"""
Domain-layer business logic (domain services) for FinanceEntry.
"""

from .entities import FinanceEntry
from .value_objects import Description, Amount, Category, EntryDate

# PUBLIC_INTERFACE
def validate_entry_data(data, for_update=False):
    """
    Validate data for finance entry using value objects logic.
    Throws ValueError for invalid data.
    """
    required = ["description", "amount", "category", "date"]
    if for_update:
        if not any(f in data for f in required):
            raise ValueError("At least one field (description, amount, category, date) required for update")
    else:
        missing = [f for f in required if f not in data]
        if missing:
            raise ValueError(f"Missing fields: {', '.join(missing)}")
    if "description" in data:
        Description(data["description"])
    if "amount" in data:
        Amount(data["amount"])
    if "category" in data:
        Category(data["category"])
    if "date" in data:
        EntryDate(data["date"])
    # All validations passed if no exception thrown
    return True
