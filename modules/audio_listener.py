# audio_listener.py - module for beda assistant

import sounddevice as sd
import numpy as np
import webrtcvad
import queue
import threading

class AudioListener:
    def __init__(self, sample_rate=16000, frame_duration_ms=30, vad_mode=2):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.vad = webrtcvad.Vad(vad_mode)
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.q = queue.Queue()
        self.listening = False

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        self.q.put(bytes(indata))

    def start_listening(self):
        self.listening = True
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            callback=self._callback,
            blocksize=self.frame_size,
        )
        self.stream.start()
        print("AudioListener started.")

    def stop_listening(self):
        self.listening = False
        self.stream.stop()
        self.stream.close()
        print("AudioListener stopped.")

    def read_frames(self):
        while self.listening:
            frame = self.q.get()
            if self.vad.is_speech(frame, self.sample_rate):
                yield frame
