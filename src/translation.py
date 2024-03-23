from speechtotext import app
from translate import Translator
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('translate')
def translate_text(text, target_language):
    target_language = 'es'
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    print(translated_text)
    emit('translated_text', translated_text)
