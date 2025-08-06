"""
Flask routes for API layer. Thin controllers delegate to Application layer.
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

from ..infrastructure.persistence.db_models import db
from ..infrastructure.persistence.sqlalchemy_repo import SQLAlchemyFinanceEntryRepository
from ..application.entry_service import FinanceEntryService
from ..domain.finance_entry.services import validate_entry_data

api_bp = Blueprint("api", __name__)

def get_service():
    # Singleton per app
    if not hasattr(current_app, "_finance_entry_service"):
        repo = SQLAlchemyFinanceEntryRepository()
        current_app._finance_entry_service = FinanceEntryService(repo)
    return current_app._finance_entry_service

@api_bp.route("/entries", methods=["GET"])
# PUBLIC_INTERFACE
def get_entries():
    """
    Get all finance entries.
    Returns: {"entries": [...], "running_total": float}
    """
    service = get_service()
    entries = service.list()
    data = [e.as_dict() for e in entries]
    running_total = sum(e.amount for e in entries)
    return jsonify({"entries": data, "running_total": running_total}), 200

@api_bp.route("/entries", methods=["POST"])
# PUBLIC_INTERFACE
def add_entry():
    """
    Add a new finance entry.
    Request JSON: description, amount, category, date
    Returns: 201 with created object, or 400 if invalid.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        validate_entry_data(data)
        service = get_service()
        entry = service.create(
            description=data["description"],
            amount=data["amount"],
            category=data["category"],
            entry_date=datetime.strptime(data["date"], "%Y-%m-%d").date()
        )
        return jsonify(entry.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@api_bp.route("/entries/<int:entry_id>", methods=["PUT"])
# PUBLIC_INTERFACE
def update_entry(entry_id):
    """
    Edit a finance entry.
    Request JSON: Any of [description, amount, category, date]
    Returns: updated entry, 404 if not found, 400 on error
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        validate_entry_data(data, for_update=True)
        service = get_service()
        # Only pass present fields, not all of them
        update_fields = {}
        for field in ["description", "amount", "category", "date"]:
            if field in data:
                update_fields[field] = data[field]
        entry = service.update(entry_id, **update_fields)
        return jsonify(entry.as_dict()), 200
    except Exception as e:
        db.session.rollback()
        if "Not found" in str(e):
            return jsonify({"error": "Entry not found"}), 404
        return jsonify({"error": str(e)}), 400

@api_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
# PUBLIC_INTERFACE
def delete_entry(entry_id):
    """
    Delete a finance entry.
    Returns: 200 on success, 404 if not found
    """
    service = get_service()
    ok = service.delete(entry_id)
    if ok:
        return jsonify({"message": f"Entry {entry_id} deleted"}), 200
    return jsonify({"error": "Entry not found"}), 404

@api_bp.route("/health", methods=["GET"])
# PUBLIC_INTERFACE
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200
