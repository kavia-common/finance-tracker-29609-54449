"""
Main entry point for finance_tracker_backend.

Implements REST API endpoints for managing financial entries:
- GET /entries: List all entries and running total.
- POST /entries: Add new entry.
- PUT /entries/<id>: Edit entry.
- DELETE /entries/<id>: Remove entry.

Uses SQLAlchemy (FinanceEntry) model and Flask request/response utilities.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# PUBLIC_INTERFACE
class FinanceEntry(db.Model):
    """
    Model representing a finance entry.
    Fields:
        id: Integer, primary key, auto-increment
        description: String, textual description of the entry
        amount: Float, value for the entry
        category: String, category for the entry
        date: Date, date of the entry
    """
    __tablename__ = 'finance_entries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # PUBLIC_INTERFACE
    def as_dict(self):
        """Converts model to dict for JSON serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date.isoformat()
        }

# PUBLIC_INTERFACE
def validate_entry_json(data, for_update=False):
    """Validate incoming JSON data for entry creation/update."""
    required = ["description", "amount", "category", "date"]
    if for_update:
        # Allow partial update; but at least one field must be present
        if not any(f in data for f in required):
            return False, "At least one field (description, amount, category, date) required for update"
    else:
        missing = [f for f in required if f not in data]
        if missing:
            return False, f"Missing fields: {', '.join(missing)}"
    try:
        if "amount" in data:
            float(data["amount"])
        if "date" in data:
            # Accepts 'YYYY-MM-DD'
            datetime.strptime(data["date"], "%Y-%m-%d")
    except Exception as e:
        return False, f"Invalid data format: {str(e)}"
    return True, None

# PUBLIC_INTERFACE
def create_app():
    """
    Factory function to create and configure the Flask app instance.
    Sets up Flask, SQLAlchemy, and initializes the SQLite database.
    """
    app = Flask(__name__)
    # SQLite configuration; uses local file 'finance_db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Create tables if db does not exist
    with app.app_context():
        db.create_all()

    @app.route('/entries', methods=['GET'])
    # PUBLIC_INTERFACE
    def get_entries():
        """
        Get all finance entries.

        Returns:
            JSON: {
                "entries": [ {entry}, ... ],
                "running_total": float
            }
        """
        entries = FinanceEntry.query.order_by(FinanceEntry.date.desc(), FinanceEntry.id.desc()).all()
        data = [e.as_dict() for e in entries]
        running_total = sum(e.amount for e in entries)
        return jsonify({"entries": data, "running_total": running_total}), 200

    @app.route('/entries', methods=['POST'])
    # PUBLIC_INTERFACE
    def add_entry():
        """
        Add a new finance entry.

        Request JSON:
            {
                "description": string,
                "amount": float,
                "category": string,
                "date": "YYYY-MM-DD"
            }

        Returns:
            201 with created object, or 400 if invalid.
        """
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        valid, msg = validate_entry_json(data)
        if not valid:
            return jsonify({"error": msg}), 400
        try:
            entry = FinanceEntry(
                description=data["description"],
                amount=float(data["amount"]),
                category=data["category"],
                date=datetime.strptime(data["date"], "%Y-%m-%d").date()
            )
            db.session.add(entry)
            db.session.commit()
            return jsonify(entry.as_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Unable to create entry: {str(e)}"}), 500

    @app.route('/entries/<int:entry_id>', methods=['PUT'])
    # PUBLIC_INTERFACE
    def update_entry(entry_id):
        """
        Edit a finance entry.

        Request JSON: Any of ["description", "amount", "category", "date"]
        Returns: updated entry, 404 if not found, 400 on error
        """
        entry = FinanceEntry.query.get(entry_id)
        if not entry:
            return jsonify({"error": "Entry not found"}), 404
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        valid, msg = validate_entry_json(data, for_update=True)
        if not valid:
            return jsonify({"error": msg}), 400

        try:
            if "description" in data:
                entry.description = data["description"]
            if "amount" in data:
                entry.amount = float(data["amount"])
            if "category" in data:
                entry.category = data["category"]
            if "date" in data:
                entry.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            db.session.commit()
            return jsonify(entry.as_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Unable to update entry: {str(e)}"}), 500

    @app.route('/entries/<int:entry_id>', methods=['DELETE'])
    # PUBLIC_INTERFACE
    def delete_entry(entry_id):
        """
        Delete a finance entry.

        Returns: 200 on success, 404 if not found
        """
        entry = FinanceEntry.query.get(entry_id)
        if not entry:
            return jsonify({"error": "Entry not found"}), 404
        try:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({"message": f"Entry {entry_id} deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Unable to delete entry: {str(e)}"}), 500

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    # PUBLIC_INTERFACE
    def health_check():
        """Health check endpoint."""
        return jsonify({'status': 'ok'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
