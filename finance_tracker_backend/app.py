"""
Main entry point for finance_tracker_backend.

This lightweight Flask API provides endpoints for managing financial entries, including:
- Viewing all entries (GET /entries)
- Creating a new entry (POST /entries)
- Editing an entry (PUT /entries/<id>)
- Deleting an entry (DELETE /entries/<id>)

Uses SQLite as the backend database (will be configured in future steps).
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

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

def create_app():
    """ PUBLIC_INTERFACE
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
        """Get all finance entries (stub implementation)."""
        return jsonify([]), 200

    @app.route('/entries', methods=['POST'])
    # PUBLIC_INTERFACE
    def add_entry():
        """Add a new finance entry (stub implementation)."""
        return jsonify({'message': 'Entry added (placeholder)'}), 201

    @app.route('/entries/<int:entry_id>', methods=['PUT'])
    # PUBLIC_INTERFACE
    def update_entry(entry_id):
        """Edit a finance entry (stub implementation)."""
        return jsonify({'message': f'Entry {entry_id} updated (placeholder)'}), 200

    @app.route('/entries/<int:entry_id>', methods=['DELETE'])
    # PUBLIC_INTERFACE
    def delete_entry(entry_id):
        """Delete a finance entry (stub implementation)."""
        return jsonify({'message': f'Entry {entry_id} deleted (placeholder)'}), 200

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
