from flask import Blueprint, current_app

bp = Blueprint('main', __name__)

@bp.route('/')
def health_check():
    return f"Config loaded successfully: {current_app.config['ROBOT_NAME']}"