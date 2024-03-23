from flask import Flask, render_template, request
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

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio_data' not in request.files:
        return 'No audio_data key in request.files', 400

    audio_file = request.files['audio_data']
    temp_webm_path = 'temp.webm'
    audio_file.save(temp_webm_path)
    temp_wav_path = "temp.wav"
    
    try:
        subprocess.run(['ffmpeg', '-i', temp_webm_path, temp_wav_path], check=True)

        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(text)

        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e), 500
    finally:
        os.remove(temp_webm_path)
        os.remove(temp_wav_path)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')

