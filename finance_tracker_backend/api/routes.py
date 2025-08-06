"""
Flask routes for API layer. Thin controllers delegate to Application layer.
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

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
        # Validation is done via value objects logic in the domain service.
        validate_entry_data(data)
        service = get_service()
        # Construct date argument robustly: accept ISO string or date object
        entry_date = data.get("date")
        if isinstance(entry_date, str):
            try:
                entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()
            except Exception:
                # Delegate parsing error to EntryDate value object
                pass
        entry = service.create(
            description=data["description"],
            amount=data["amount"],
            category=data["category"],
            entry_date=entry_date
        )
        return jsonify(entry.as_dict()), 201
    except Exception as e:
        # All exceptions should be handled by the application/domain/service; rollback infra if required.
        # The repository itself should also handle its own transactions.
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
        update_fields = {}
        for field in ["description", "amount", "category", "date"]:
            if field in data:
                # If "date" is provided as string, convert to date
                if field == "date" and isinstance(data[field], str):
                    try:
                        update_fields[field] = datetime.strptime(data[field], "%Y-%m-%d").date()
                    except Exception:
                        update_fields[field] = data[field]  # let domain/value object throw
                else:
                    update_fields[field] = data[field]
        entry = service.update(entry_id, **update_fields)
        return jsonify(entry.as_dict()), 200
    except Exception as e:
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
