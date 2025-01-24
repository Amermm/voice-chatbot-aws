import os
from flask import Flask


def create_app():
    """Factory function to create and configure the Flask application"""
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
        raise RuntimeError("GOOGLE_CREDENTIALS environment variable is missing. Ensure it is set in your deployment configuration.")
    if not app.config['OPENAI_KEY']:
        raise RuntimeError("OPENAI_API_KEY environment variable is missing. Ensure it is set in your deployment configuration.")

    # Check if the database file exists
    database_path = app.config['DATABASE_PATH']
    if not os.path.exists(database_path):
        raise FileNotFoundError(f"Database file not found at: {database_path}. Ensure the file is in the deployment directory.")

    # Import and register routes after configuration is loaded
    from .routes import bp
    app.register_blueprint(bp)

    return app
