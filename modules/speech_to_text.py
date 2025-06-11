# speech_to_text.py - module for beda assistant

import whisper

class SpeechToText:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result["text"]
