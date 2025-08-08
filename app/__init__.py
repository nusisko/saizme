from flask import Flask
from app.config import Config

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Import and register the API blueprint from the api module
    from .api.routes import api_bp
    app.register_blueprint(api_bp)

    @app.route("/health")
    def health_check():
        return "healthy as a horse"

    return app