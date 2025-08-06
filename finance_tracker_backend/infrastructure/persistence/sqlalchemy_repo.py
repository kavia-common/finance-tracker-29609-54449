"""
SQLAlchemy-backed implementation of FinanceEntryRepository.
"""

from datetime import date
from typing import Optional, List

from .db_models import db, FinanceEntryORM
from ...domain.finance_entry.repository import FinanceEntryRepository
from ...domain.finance_entry.entities import FinanceEntry

# PUBLIC_INTERFACE
class SQLAlchemyFinanceEntryRepository(FinanceEntryRepository):
    """SQLAlchemy implementation of FinanceEntryRepository."""

    def list_entries(self) -> List[FinanceEntry]:
        entries = FinanceEntryORM.query.order_by(FinanceEntryORM.date.desc(), FinanceEntryORM.id.desc()).all()
        return [FinanceEntry(e.id, e.description, e.amount, e.category, e.date) for e in entries]

    def get_by_id(self, entry_id: int) -> Optional[FinanceEntry]:
        obj = FinanceEntryORM.query.get(entry_id)
        if not obj:
            return None
        return FinanceEntry(obj.id, obj.description, obj.amount, obj.category, obj.date)

    def add(self, entry: FinanceEntry) -> FinanceEntry:
        new_obj = FinanceEntryORM(
            description=entry.description,
            amount=entry.amount,
            category=entry.category,
            date=entry.date
        )
        db.session.add(new_obj)
        db.session.commit()
        entry.id = new_obj.id
        return entry

    def update(self, entry: FinanceEntry) -> FinanceEntry:
        obj = FinanceEntryORM.query.get(entry.id)
        if not obj:
            raise ValueError("Entry not found")
        obj.description = entry.description
        obj.amount = entry.amount
        obj.category = entry.category
        obj.date = entry.date
        db.session.commit()
        return entry

    def delete(self, entry_id: int) -> bool:
        obj = FinanceEntryORM.query.get(entry_id)
        if not obj:
            return False
        db.session.delete(obj)
        db.session.commit()
        return True
