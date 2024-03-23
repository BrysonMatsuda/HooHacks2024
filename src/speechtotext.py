from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import io
from threading import Lock
import os
import subprocess
import wave
import time

app = Flask(__name__, template_folder='../public', static_folder='../static')
socketio = SocketIO(app)
audio_buffer = io.BytesIO()
buffer_lock = Lock()

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    global audio_buffer
    with buffer_lock:
        audio_buffer.write(chunk)

@socketio.on('recording_stopped')
def speech_to_text():
    temp_webm_path = "temp.webm"
    temp_wav_path = "temp.wav"
    try:
        # Save the audio buffer to a temporary WebM file
        with wave.open(temp_webm_path, "wb") as webm_file:
            webm_file.setnchannels(2)
            webm_file.setsampwidth(2)
            webm_file.setframerate(44100)
            webm_file.writeframes(audio_buffer.getvalue())
        
        time.sleep(0.5)

        # Convert WebM to WAV using ffmpeg
        subprocess.run(['ffmpeg', '-i', temp_webm_path, temp_wav_path])

        # Load the WAV file and perform speech-to-text processing
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Emit the recognized text to the client
        socketio.emit('recognized_text', text)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(temp_webm_path):
                os.remove(temp_webm_path)
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
        except Exception as e:
            print(f"An error occurred while deleting temporary files: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
