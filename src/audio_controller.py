from io import BytesIO
from dataclasses import dataclass
import wave

from openai import OpenAI

from src.variables import (
    CHUNK,
    CHANNELS,
    FORMAT,
    RATE,
)
from src.types import NamedBytesIO

import keyboard
import pyaudio


@dataclass
class AudioController:

    client: OpenAI
    is_recording: bool = True

    def __post_init__(self):
        keyboard.add_hotkey("space", lambda: setattr(self, "is_recording", False))

    def record_audio(self) -> BytesIO:
        buffer = BytesIO()
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        print("Recording... press the spacebar when you are done")
        while True and self.is_recording:
            buffer.write(stream.read(CHUNK))
        stream.close()
        p.terminate()
        setattr(self, "is_recording",True)
        return buffer

    def create_wav_buffer(self, audio_buffer: BytesIO):
        wav_buffer = BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            audio_buffer.seek(0)
            wf.writeframes(audio_buffer.read())
        return wav_buffer

    def transcribe_audio(self, audio_buffer: BytesIO, name: str = "audio.wav") -> str:
        wav_buffer = self.create_wav_buffer(audio_buffer)
        wav_buffer.seek(0)

        named_buffer = NamedBytesIO(wav_buffer, name)

        transcription = self.client.audio.transcriptions.create(
            model="whisper-1", file=named_buffer
        )
        return transcription.text
