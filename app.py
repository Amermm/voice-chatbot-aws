from app import create_app 
import logging
logging.basicConfig(level=logging.DEBUG)

app = create_app()

if __name__ == '__main__':
    # Use port 8000 instead of the default 5000
    app.run(host='0.0.0.0', port=8000, debug=True)