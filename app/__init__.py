import os
from flask import Flask

def create_app():
    """Factory function with armored initialization"""
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config.update({
        'DATABASE_PATH': os.getenv('DATABASE_EXCEL_PATH', 'SCADA TestData.xlsx'),
        'GOOGLE_CREDS': os.getenv('GOOGLE_CREDENTIALS'),
        'OPENAI_KEY': os.getenv('OPENAI_API_KEY'),
        'ROBOT_NAME': os.getenv('ROBOTNAME', 'DefaultBot')
    })

    # Validate critical environment variables
    if not app.config['GOOGLE_CREDS']:
        raise RuntimeError("GOOGLE_CREDENTIALS environment variable is missing.")
    if not app.config['OPENAI_KEY']:
        raise RuntimeError("OPENAI_API_KEY environment variable is missing.")

    # Check if the database file exists
    if not os.path.exists(app.config['DATABASE_PATH']):
        raise FileNotFoundError(f"Database file not found at: {app.config['DATABASE_PATH']}")

    # Import and register routes after configuration is loaded
    from .routes import bp
    app.register_blueprint(bp)

    return app
