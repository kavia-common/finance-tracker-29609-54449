"""
SQLAlchemy ORM model mapping (Infrastructure layer).
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# PUBLIC_INTERFACE
class FinanceEntryORM(db.Model):
    """SQLAlchemy model for finance entries."""
    __tablename__ = "finance_entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    date = db.Column(db.Date, nullable=False)
