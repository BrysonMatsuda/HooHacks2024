from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import io
from threading import Lock
from pydub import AudioSegment

app = Flask(__name__, template_folder='../public', static_folder='../static')
socketio = SocketIO(app)
audio_buffer = io.BytesIO()
buffer_lock = Lock()

@socketio.on('audio_chunk')
def handle_audio_chunk(chunk):
    global audio_buffer
    audio_buffer.write(chunk)

@socketio.on('recording_stopped')
def speech_to_text():
    global audio_buffer
    combined = b"".join(audio_buffer)
    audio_buffer = []
    
    audio_stream = io.BytesIO(combined)
    audio_segment = AudioSegment.from_file(audio_stream, format="wav")
    
    audio_segment.export("output.wav", format="wav")
    
    try:
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 0.8
        with sr.AudioFile("output.wav") as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print("Recognized text:", text)
            emit('recognized_text', text)
    except Exception as e:
        print(f"An error occurred: {e}")


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
