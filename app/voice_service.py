import os
import openai
import pandas as pd
from google.cloud import speech
import sounddevice as sd
import wave
import threading
import queue
import time
from datetime import datetime
import logging
import numpy as np
import pyttsx3
from dotenv import load_dotenv

class VoiceChatBot:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        load_dotenv()
        
        # Initialize context_data
        self.context_data = self._load_excel_data()
        
        # Set up environment
        self.setup_environment()
        
        # Audio settings
        self.RATE = 16000
        self.CHANNELS = 1
        self.is_listening = False
        self.audio_queue = queue.Queue()

        # Initialize components
        self.speech_client = speech.SpeechClient()

    def _load_excel_data(self):
        try:
            excel_path = os.path.join(os.getcwd(), 'SCADA TestData.xlsx')
            if not os.path.exists(excel_path):
                self.logger.error(f"Excel file not found at: {excel_path}")
                return ""
                
            df = pd.read_excel(excel_path)
            for column in df.columns:
                if df[column].dtype in ['float64', 'int64']:
                    df[column] = df[column].fillna(0)
                else:
                    df[column] = df[column].fillna('')
            context = df.astype(str).to_string(index=False, header=True)
            self.logger.info("Excel data loaded successfully")
            return context
        except Exception as e:
            self.logger.error(f"Error loading Excel: {e}")
            return ""

    def setup_environment(self):
        """Set up environment variables and credentials"""
        try:
            openai.api_key = os.getenv('OPENAI_API_KEY')
            if os.getenv('GOOGLE_CREDENTIALS'):
                self.logger.info("Google credentials loaded successfully")
            else:
                self.logger.error("GOOGLE_CREDENTIALS environment variable not set")
        except Exception as e:
            self.logger.error(f"Error in setup_environment: {e}")

    def start_listening(self):
        self.is_listening = True

        def callback(indata, frames, time, status):
            if status:
                self.logger.warning(f"SoundDevice Status: {status}")
            if self.is_listening:
                self.audio_queue.put(indata.copy())

        self.stream = sd.InputStream(
            channels=self.CHANNELS,
            samplerate=self.RATE,
            callback=callback
        )
        self.stream.start()
        self.logger.info("Audio stream started.")

    def stop_listening(self):
        self.is_listening = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.logger.info("Audio stream stopped.")

    def process_audio_data(self, audio_data):
        if not audio_data:
            return None

        # Save audio to a temporary WAV file
        temp_filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        audio_data = np.concatenate(audio_data, axis=0)  # Combine queued data
        with wave.open(temp_filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(2)  # Assuming 16-bit audio
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data.tobytes())

        try:
            with open(temp_filename, 'rb') as f:
                content = f.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.RATE,
                language_code="en-US",
                enable_automatic_punctuation=True,
                use_enhanced=True
            )

            response = self.speech_client.recognize(config=config, audio=audio)
            for result in response.results:
                return result.alternatives[0].transcript
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        return None

    def process_continuous_audio(self):
        audio_data = []
        silence_threshold = 500  # Adjust based on your needs
        silence_frames = 0
        max_silence_frames = 20  # Adjust based on your needs

        while self.is_listening:
            try:
                if not self.audio_queue.empty():
                    data = self.audio_queue.get()
                    audio_data.append(data)
                    
                    audio_array = np.frombuffer(data, dtype=np.int16)
                    if np.abs(audio_array).mean() < silence_threshold:
                        silence_frames += 1
                    else:
                        silence_frames = 0

                    if silence_frames >= max_silence_frames and len(audio_data) > 0:
                        transcript = self.process_audio_data(audio_data)
                        if transcript:
                            response = self.get_gpt_response(transcript)
                            yield {"transcript": transcript, "response": response}
                            self.speak_response(response)
                        audio_data = []
                        silence_frames = 0
                else:
                    time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Error in continuous processing: {e}")
                yield {"error": str(e)}
