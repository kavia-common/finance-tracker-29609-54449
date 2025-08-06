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

def create_app():
    """ PUBLIC_INTERFACE
    Factory function to create and configure the Flask app instance.
    """
    app = Flask(__name__)

    # Placeholder for future SQLite database initialization

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
