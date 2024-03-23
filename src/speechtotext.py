from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import speech_recognition as sr

app = Flask(__name__, template_folder='../public', static_folder='../static')
socketio = SocketIO(app)

@socketio.on('speech_request')
def speech_to_text():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    
    with sr.Microphone() as mic:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(mic)
        
        try:
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
