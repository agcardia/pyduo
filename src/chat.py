from dataclasses import dataclass, field
import os

from pydub import AudioSegment
from pydub.playback import play
from openai import OpenAI, Stream
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from src.config import Config


@dataclass(repr=True)
class Tutor:
    client: OpenAI
    config: Config 
    model: str = "gpt-3.5-turbo"
    stream: bool = False
    audio_path: str = os.path.join(os.getcwd(),'audio')

    def __post_init__(self):
        if not os.path.exists(self.audio_path):
            os.mkdir(self.audio_path)

    def start_stream(self):
        assert self.model is not None
        self.config.generate_settings()
        stream: Stream[ChatCompletionChunk] = self.client.chat.completions.create(
            messages=[
                self.config.system_message,
                {"role": "user", "content": "Let us begin!"},
            ],
            model=self.model,
            stream=True,
        )
        self.read_stream(stream)


    def read_stream(self, stream: Stream[ChatCompletionChunk]) -> None:
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
        print("\n")

    def read_answer(self, line: str) -> None:
        assert self.model is not None
        if hasattr(self, "audio_answer"):
            self.read_audio_answer(line, self.audio_answer)
            delattr(self, "audio_answer")
            return

        self.config.generate_settings()
        stream: Stream[ChatCompletionChunk] = self.client.chat.completions.create(
            messages=[
                self.config.system_message,
                {"role": "user", "content": line},
            ],
            model=self.model,
            stream=True,
        )
        self.read_stream(stream)
    
    def read_audio_answer(self, line: str, answer_key: str):
        self.config.generate_audio_response_settings(answer_key)
        stream: Stream[ChatCompletionChunk] = self.client.chat.completions.create(
            messages=[
                self.config.system_message,
                {"role": "user", "content": line},
            ],
            model=self.model,
            stream=True,
        )
        self.read_stream(stream)


    def generate_audio(self):
        assert self.model is not None
        self.config.generate_settings()
        completion: ChatCompletion = self.client.chat.completions.create(
            messages=[
                self.config.system_message,
                {
                    "role": "user",
                    "content": f"Generate 5 written examples in {self.config.language} with a focus on {self.config.focus} at a difficulty of {self.config.difficulty}. Return your response as a single string without numbers.",
                },
            ],
            model=self.model,
            temperature=0.3,
            stream=False,
        )
        response = completion.choices[0].message.content
        formatted_response = " ".join(
            [example + "[pause]" for example in response.split("\n")]
        )
        self.make_mp3(formatted_response)
        self.audio_answer = response

    def make_mp3(self, line: str):
        speech_file_path = os.path.join(self.audio_path,"speech.mp3")
        with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="onyx",
            input=line,
        ) as response:
            response.stream_to_file(speech_file_path)

        sound = AudioSegment.from_mp3(speech_file_path)
        play(sound)
