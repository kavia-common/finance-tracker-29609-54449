"""
Application configuration for Flask and SQLAlchemy.
"""

import os

# PUBLIC_INTERFACE
class Config:
    """Base configuration object for Flask app."""
    SQLALCHEMY_DATABASE_URI = os.getenv("FINANCE_DB_URI", "sqlite:///finance_db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
