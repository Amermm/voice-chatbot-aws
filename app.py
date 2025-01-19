from flask import Flask
from app.routes import bp
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__, 
                template_folder='templates',  # Add this
                static_folder='static')       # Add this
    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Enable debug mode