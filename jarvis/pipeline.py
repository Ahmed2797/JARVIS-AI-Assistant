from jarvis.command import Command
from jarvis.tts import TTSpy
from jarvis.utlits import *
from jarvis.logger import logging
from jarvis.exception import CustomException

import sys

class Main:
    """
    Main controller for Jarvis Voice Assistant.
    
    Handles:
    - Voice wakeup
    - Continuous command listening
    - Command execution
    - Proper exit handling
    """

    def __init__(self):
        self.command = Command()
        self.speak = TTSpy()

    def main_voice_loop(self):
        """
        Starts the main voice loop.
        Continuously listens for commands and executes them.
        """
        try:
            logging.info("Starting Jarvis voice loop...")
            ai_voice()
            voice_getting()

            while True:
                user_command = self.command.take_voice_command()
                logging.info(f"User said: {user_command}")

                if user_command and user_command != "none":
                    result = self.command.execute_all_command(user_command)

                    if result == "exit":
                        logging.info("Exit command received. Shutting down...")
                        break

                self.speak.speak("Anything else I can help you with sir?")

        except Exception as e:
            logging.error(f"Unexpected error in main_voice_loop: {e}")
            raise CustomException(e,sys)
        finally:
            self.speak.speak("Goodbye sir! Program terminated.")
            logging.info("Jarvis shut down successfully.")
