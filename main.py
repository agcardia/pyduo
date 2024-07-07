import cmd

from openai import OpenAI
from src.variables import API_KEY, PROJECT_ID
from src.config import Config
from src.types import Difficulty, Focus
from src.chat import Tutor

client = OpenAI(api_key=API_KEY, project=PROJECT_ID)
tutor = Tutor(client, Config(language='Italian'))

def test(line: str):
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": line}], model="gpt-3.5-turbo", stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    print("\n")

class PyDuoCLI(cmd.Cmd):
    intro = r"""
                         
              __________-------____                 ____-------__________
          \------____-------___--__---------__--___-------____------/
           \//////// / / / / / \   _-------_   / \ \ \ \ \ \\\\\\\\/
             \////-/-/------/_/_| /___   ___\ |_\_\------\-\-\\\\/
               --//// / /  /  //|| (O)\ /(O) ||\\  \  \ \ \\\\--
                    ---__/  // /| \_  /V\  _/ |\ \\  \__---
                         -//  / /\_ ------- _/\ \  \\-
                           \_/_/ /\---------/\ \_\_/
                               ----\   |   /----
                                    | -|- |
                                   /   |   \
                                   ---- \___|


                                Welcome to pyDuo! type help or ? to list commands.         
    """
    prompt = "(pyDuo) "

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.tutor = Tutor(client, self.config)
    
    def do_config(self, line: str) -> None:
        """View the config for the current session"""
        print(self.config)

    def do_lang(self, line: str) -> None:
        """Sets the current language for the active session"""
        self.config.language = line
        print(f"...resetting wth new language of {line}...")
        self.tutor.start_stream()

    def do_level(self, line: str) -> None:
        """Sets the current difficulty for the active session (EASY,MEDIUM,HARD)"""
        if line in Difficulty.__members__:
            self.config.difficulty = line
            print(f"...resetting wth new difficulty of {line}...")
            self.tutor.start_stream()
        else:
            print(f"Invalid Option: Choices are {Difficulty.__members__}")

    def do_focus(self, line: str) -> None:
        if line in Focus.__members__:
            self.config.focus = line
            print(f"...resetting wth new focus of {line}...")
            self.tutor.start_stream()
        else:
            print(f"Invalid Option: Choices are {Focus.__members__}")
    
    def do_exit(self, line: str) -> bool:
        """Exits shell environment"""
        print("goodbye!")
        return True
    
    def do_begin(self, line:str) -> None:
        print(f'{self.tutor.config.language}')
        self.tutor.start_stream()

    def default(self, line: str) -> None:
        """Default behavior, spins up a chatGPT response to input line of text"""
        self.tutor.read_answer(line)

    def precmd(self, line: str) -> str:
        split_line = line.split()
        if len(split_line) > 1:
            line = " ".join(
                [split_line[0]] + [l.upper() for i, l in enumerate(split_line) if i > 0]
            )
        return line
    
def shell():
    PyDuoCLI(config=Config(language='Italian')).cmdloop()

if __name__ == "__main__":
    shell()
