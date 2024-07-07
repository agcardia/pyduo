from dataclasses import dataclass

from src.types import Focus, Difficulty


@dataclass(repr=True, kw_only=True)
class Config:
    """
    Defines a config environment for the system of a Tutor instance

    Args:
        language (str): #TODO
        focus (Focus): #TODO
        difficulty (Difficuly): #TODO
        num_exercises (int): #TODO

    """

    language: str = "ENG"
    focus: Focus = "GRAMMAR"
    difficulty: Difficulty = "EASY"
    num_exercises: int = 10

    def generate_settings(self):

        system_message = f"""You are a tutor advising a student in the {self.language} language. 
                                They would like to focus on {self.focus} with a difficulty level of {self.difficulty}
                                You will begin by giving them a list of {self.num_exercises} to complete in the {self.language} language.
                                Upon recieving a response, you will critique their answers and give them another list of {self.num_exercises} exercises
                            """
        self.system_message = {"role": "system", "content": system_message}
