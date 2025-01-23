import boto3
import os
from flask import Flask

def get_parameter(name):
    """Fetch a parameter from AWS Systems Manager Parameter Store."""
    ssm = boto3.client('ssm', region_name='us-east-1')  # Replace with your AWS region
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response['Parameter']['Value']

# Fetch secrets and set them as environment variables
os.environ['DATABASE_EXCEL_PATH'] = get_parameter('/voice-chatbot/DATABASE_EXCEL_PATH')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = get_parameter('/voice-chatbot/GOOGLE_APPLICATION_CREDENTIALS')
os.environ['OPENAI_API_KEY'] = get_parameter('/voice-chatbot/OPENAI_API_KEY')
os.environ['ROBOTNAME'] = get_parameter('/voice-chatbot/ROBOTNAME')

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    return app
print("Testing AWS Parameter Store:")
print("DATABASE_EXCEL_PATH:", get_parameter('/voice-chatbot/DATABASE_EXCEL_PATH'))
print("GOOGLE_APPLICATION_CREDENTIALS:", get_parameter('/voice-chatbot/GOOGLE_APPLICATION_CREDENTIALS'))
print("OPENAI_API_KEY:", get_parameter('/voice-chatbot/OPENAI_API_KEY'))
print("ROBOTNAME:", get_parameter('/voice-chatbot/ROBOTNAME'))