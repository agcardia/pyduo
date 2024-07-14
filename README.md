# Overview

pyduo is a CLI application that uses the OpenAI API to allow users to create their own interactive language tutor. The program can generate grammar excercises through the terminal as well as simulate a real conversation, allowing the user to record their response to an audio generated AI agent.

# Getting Started

 Create a virtual environment to hold the project with `python -m venv .venv` and activate it with `source .venv/bin/activate`. You will need to download the `ffpmeg` library to use the conversation simulator.
 
 Install the project with `pip install .`

Now run `pyduo start` to activate the tutor

# Commands

  *  `lang`: Changes the current language for the active session
  *  `focus`: Changes the active focus of the tutor object
  *  `level`: changes the difficulty level
  *  `config`: View the current configuration for the tutor
  * `simulate` Starts the live conversation simulator



