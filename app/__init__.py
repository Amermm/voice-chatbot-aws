import os
from flask import Flask

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config.update({
        'DATABASE_PATH': os.getenv('DATABASE_EXCEL_PATH', 'SCADA TestData.xlsx'),
        'GOOGLE_CREDS': os.getenv('GOOGLE_CREDENTIALS'),
        'OPENAI_KEY': os.getenv('OPENAI_API_KEY'),
        'ROBOT_NAME': os.getenv('ROBOTNAME', 'DefaultBot')
    })

    # Debug log to confirm app creation
    print("DEBUG: Flask app created and configuration loaded.")

    # Import and register routes
    from .routes import bp
    app.register_blueprint(bp)

    # Debug log to confirm blueprint registration
    print("DEBUG: Blueprint 'main' registered.")

    return app
