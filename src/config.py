from dataclasses import dataclass

from src.types import Focus, Difficulty


@dataclass(repr=True, kw_only=True)
class Config:
    """
    Defines a config environment for the system of a Tutor instance

    Args:
        language (str): Current language
        focus (Focus): Current focus, enum type with options `[Grammar, Verbs, Noun, Conversation]`
        difficulty (Difficuly): Current difficulty level, enum type with options `[Easy, Medium, Hard]`
        num_exercises (int): Number of excercises to return with each response (default 10)

    """

    language: str = "ENG"
    focus: Focus = "GRAMMAR"
    difficulty: Difficulty = "EASY"
    num_exercises: int = 10

    def generate_settings(self):

        system_message = f"""you are a tutor advising a student in the {self.language} language. 
                                they would like to focus on {self.focus} with a difficulty level of {self.difficulty}
                                you will begin by giving them a list of {self.num_exercises} to complete in the {self.language} language.
                                upon recieving a response, you will critique their answers and give them another list of {self.num_exercises} exercises
                            """

        if self.focus == "CONVERSATION":
            system_message = f"""you are a tutor advising a student in the {self.language} language. with a difficulty level of {self.difficulty}
                                you will be simulating a real life conversation with the user take in each response and respond as you would
                                if you were talking to a real person in front of you
                             """
        self.system_message = {"role": "system", "content": system_message}

    def generate_audio_response_settings(self, answer_key: str):
        system_message = f"""You are a tutor advising a student in the {self.language} language. 
                                They were given an mp3 file of sentences to translate from {self.language} into English.
                                Upon recieving their response, you will critique their answers based on the given answer key {answer_key}
                            """
        self.system_message = {"role": "system", "content": system_message}
    
    def generate_conversation_settings(self):
        system_message = f"""You are a tutor advising a student in the {self.language} language. 
                               You are simulating a real life conversation with a student in {self.language}. You will respond as if you 
                               are having a real conversation.
                            """
        self.system_message = {"role": "system", "content": system_message}
