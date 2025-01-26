from app import create_app
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Starting Flask application...")

# Create the Flask app
app = create_app()

if __name__ == '__main__':
    print("Running app.py from:", __file__)  # Print before starting the ap
    app.run(host='0.0.0.0', port=8080, debug=True)