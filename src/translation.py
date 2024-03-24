from speechtotext import app
from translate import Translator
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='../public', static_folder='../static')
socketio = SocketIO(app)

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    print(data)
    data = request.get_json()
    text = data['text']
    target_language = data['languageName']
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return jsonify(translated_text=translated_text)

if __name__ == '__main__':
    socketio.run(app, debug=True)