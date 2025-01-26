import os
from flask import Flask

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, template_folder='templates')

    # Load configuration from environment variables
    app.config.update({
        'DATABASE_PATH': os.getenv('DATABASE_EXCEL_PATH', 'SCADA TestData.xlsx'),
        'GOOGLE_CREDS': os.getenv('GOOGLE_CREDENTIALS'),
        'OPENAI_KEY': os.getenv('OPENAI_API_KEY'),
        'ROBOT_NAME': os.getenv('ROBOTNAME', 'DefaultBot'),
        'EXPLAIN_TEMPLATE_LOADING': True  # Debug template loading
    })

    # Debugging: Log the configuration
    print("DEBUG: Flask app created and configuration loaded.")
    print(f"DEBUG: DATABASE_PATH={app.config.get('DATABASE_PATH')}")
    print(f"DEBUG: GOOGLE_CREDS={app.config.get('GOOGLE_CREDS')}")
    print(f"DEBUG: OPENAI_KEY={app.config.get('OPENAI_KEY')}")
    print(f"DEBUG: ROBOT_NAME={app.config.get('ROBOT_NAME')}")
    print(f"DEBUG: Template search paths are {app.jinja_loader.searchpath}")

    # Import and register routes
    from .routes import bp
    app.register_blueprint(bp)

    # Debugging: Confirm blueprint registration
    print("DEBUG: Blueprint 'main' registered.")

    return app
