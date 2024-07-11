import cmd

from enum import Enum

from openai import OpenAI
from src.variables import API_KEY, PROJECT_ID
from src.config import Config
from src.types import Difficulty, Focus
from src.chat import Tutor


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

                                Quickstart

                Use the command begin to activate the agent

                lang [language] changes the language of the current session 
                focus [focus] changes the focus 
                level [level] alters the difficulty level of the questions        
    """
    prompt = "(pyDuo) "

    def __init__(self, config: Config, client: OpenAI):
        super().__init__()
        self.config = config
        self.tutor = Tutor(client, self.config)
    
    def config_change(self, *, setting_enum: Enum | None, setting_attr: str, line: str) -> None:
        """Abstract function for implementing config changes in our CLI"""

        if isinstance(setting_enum, Enum) and line not in setting_enum.__members__:
            print(f"Invalid Option: Choices are {setting_enum.__members__}")
            return 

        setattr(self.config, setting_attr, line)
        print(f"...resetting wth new {setting_attr} of {line}...")
        self.tutor.config.generate_settings()

    def do_config(self, line: str) -> None:
        """View the config for the current session"""
        print(self.config)

    def do_lang(self, line: str) -> None:
        """Sets the current language for the active session"""
        self.config_change(setting_enum=None, setting_attr='language', line=line)

    def do_level(self, line: str) -> None:
        """Sets the current difficulty for the active session (EASY,MEDIUM,HARD)"""
        self.config_change(setting_enum=Difficulty, setting_attr='difficulty', line=line)

    def do_focus(self, line: str) -> None:
        self.config_change(setting_enum=Focus, setting_attr='focus', line=line)

    def do_audio(self, line: str) -> None:
        self.tutor.generate_audio()
    
    def do_restart(self, line:str) -> None:
        self.tutor.start_stream()

    def do_exit(self, line: str) -> bool:
        """Exits shell environment"""
        print("goodbye!")
        return True

    def do_begin(self, line: str) -> None:
        print(f"{self.tutor.config.language}")
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
    client = OpenAI(api_key=API_KEY, project=PROJECT_ID)
    PyDuoCLI(config=Config(language="Italian"), client=client).cmdloop()


if __name__ == "__main__":
    shell()
