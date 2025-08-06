"""
Domain value objects for finance entry attributes.
"""

from datetime import date

# PUBLIC_INTERFACE
class Description:
    """Description value object."""
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Description cannot be empty")
        self.value = value.strip()

    def __str__(self):
        return self.value

# PUBLIC_INTERFACE
class Amount:
    """Amount value object."""
    def __init__(self, value):
        try:
            self.value = float(value)
        except Exception:
            raise ValueError("Amount must be a valid number")
        # Add possible domain rules here (e.g., no negative if required)

    def __float__(self):
        return self.value

# PUBLIC_INTERFACE
class Category:
    """Category value object."""
    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Category cannot be empty")
        self.value = value.strip()

    def __str__(self):
        return self.value

# PUBLIC_INTERFACE
class EntryDate:
    """EntryDate value object."""
    def __init__(self, value):
        if isinstance(value, str):
            try:
                self.value = date.fromisoformat(value)
            except Exception:
                raise ValueError("Invalid date format (use YYYY-MM-DD)")
        elif isinstance(value, date):
            self.value = value
        else:
            raise ValueError("Date must be a string or a datetime.date instance")

    def __str__(self):
        return self.value.isoformat()
