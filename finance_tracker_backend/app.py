"""
App factory/bootstrap. Wires Flask, DB, API, CORS, and DDD layers.
"""

from flask import Flask
from flask_cors import CORS
from .config.settings import Config
from .infrastructure.persistence.db_models import db
from .api.routes import api_bp

# PUBLIC_INTERFACE
def create_app():
    """
    Factory function to create and configure the Flask app instance.
    Sets up Flask, SQLAlchemy, and initializes the database.
    Wires API, DB, CORS, etc.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        # Import blueprints here so they're registered AFTER app/db config.
        app.register_blueprint(api_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
