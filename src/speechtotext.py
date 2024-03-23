from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pydub import AudioSegment
import speech_recognition as sr
import io
from threading import Lock
import os

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
    global audio_buffer
    with buffer_lock:
        audio_buffer.seek(0)
        temp_file_path = "temp.wav"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(audio_buffer.getvalue())
        audio_buffer.seek(0)
        audio_buffer.truncate()

    try:
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 0.8
        print('hi')
        with sr.AudioFile(temp_file_path) as source:
            print('hello')
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print("Recognized text:", text)
            emit('recognized_text', text)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if os.path.exists(temp_file_path):  # Check if the temporary file exists
            os.remove(temp_file_path)  # Remove the temporary file

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
