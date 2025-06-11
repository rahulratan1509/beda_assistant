# text_to_speech.py - module for beda assistant

from TTS.api import TTS

class TextToSpeech:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        self.tts = TTS(model_name)

    def speak(self, text):
        self.tts.tts_to_file(text=text, file_path="output.wav")
        # You can add playback code here
