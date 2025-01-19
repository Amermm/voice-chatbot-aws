from flask import Blueprint, render_template, jsonify, Response, current_app
from .voice_service import VoiceChatBot
import json
import os

# Create Blueprint
bp = Blueprint('main', __name__, 
               template_folder='templates',
               static_folder='static',
               static_url_path='/static')

# Initialize chatbot
try:
    chatbot = VoiceChatBot()
except Exception as e:
    print(f"Error initializing chatbot: {e}")
    chatbot = None

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/start_listening', methods=['POST'])
def start_listening():
    if chatbot:
        try:
            chatbot.start_listening()
            return jsonify({"status": "started"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Chatbot not initialized"}), 500

@bp.route('/stop_listening', methods=['POST'])
def stop_listening():
    if chatbot:
        try:
            chatbot.stop_listening()
            return jsonify({"status": "stopped"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Chatbot not initialized"}), 500

@bp.route('/stream')
def stream():
    if not chatbot:
        return Response(json.dumps({"error": "Chatbot not initialized"}),
                       mimetype='application/json')
    
    def generate():
        try:
            for result in chatbot.process_continuous_audio():
                if isinstance(result, dict):
                    yield f"data: {json.dumps(result)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

# Error handlers
@bp.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404