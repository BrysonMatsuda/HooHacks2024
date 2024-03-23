from translate import Translator

def translate_text(text, target_language):
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text

input_text = "Hi, I am Bryson"
target_language = "ja"  # Japanese
translated_text = translate_text(input_text, target_language)
print("Translated text:", translated_text)
