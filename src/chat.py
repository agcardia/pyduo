from dataclasses import dataclass

from openai import OpenAI, Stream
from src.config import Config

@dataclass
class Tutor:
    client: OpenAI
    config: Config
    model: str = "gpt-3.5-turbo"
    stream: bool = False

    def start_stream(self):
        assert self.model is not None
        self.config.generate_settings()
        stream = self.client.chat.completions.create(
            messages=[
                self.config.system_message,
                {"role": "user", "content": "Let us begin!"},
            ],
            model=self.model,
            stream=True,
        )
        self.read_stream(stream)
    
    def read_stream(self, stream: Stream) -> None:
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
    
    def read_answer(self, line: str):
        assert self.model is not None
        self.config.generate_settings()
        stream = self.client.chat.completions.create(
            messages=[
                self.config.system_message,
                {"role": "user", "content": line},
            ],
            model=self.model,
            stream=True,
        )
        self.read_stream(stream)
