from flask import Blueprint, render_template, current_app

# Create a Flask Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    """Render the home page with robot name."""
    print("DEBUG: Entered the '/' route in routes.py")
    robot_name = current_app.config.get('ROBOT_NAME', 'Unknown')
    print(f"DEBUG: Robot name in '/' route is {robot_name}")
    return render_template('index.html', robot_name=robot_name)

@bp.route('/status')
def status():
    """Status route to check app health."""
    return {"status": "App is running", "version": "1.0"}

@bp.route('/config')
def config():
    """Route to display app configuration (for debugging)."""
    config = {
        'DATABASE_PATH': current_app.config.get('DATABASE_PATH'),
        'GOOGLE_CREDS': current_app.config.get('GOOGLE_CREDS'),
        'OPENAI_KEY': current_app.config.get('OPENAI_API_KEY'),
        'ROBOT_NAME': current_app.config.get('ROBOT_NAME'),
    }
    return config
