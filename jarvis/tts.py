from jarvis.logger import logging
from jarvis.exception import CustomException

from gtts import gTTS
import sys
import os 
import platform
import pyttsx3


class TTSpy:
    """
    TTSpy: High-quality Text-To-Speech (TTS) engine using Google gTTS.

    Features:
    - Converts text into natural-sounding speech using Google's TTS.
    - Saves the spoken audio as an MP3 file.
    - Plays the audio using mpg123 (Linux command-line MP3 player).
    - Logs all TTS activities for debugging and monitoring.

    Requirements:
    - Internet connection (gTTS is online)
    - mpg123 installed on Linux:
        sudo apt install mpg123

    Usage:
        tts = TTSpy()
        tts.speak("Hello sir, how are you?")
    """

    def __init__(self):
        pass

    def speak(self, text: str):
        """
        Convert text to speech using gTTS and play the output MP3.

        Args:
            text (str): The message Jarvis will speak aloud.
        """
        try:
            logging.info(f"TTS speaking: {text}")
            print(f"JARVIS : {text}")

            # Generate speech
            tts = gTTS(text, lang='en')
            tts.save("output.mp3")

            # Play MP3
            os.system("mpg123 output.mp3")

        except Exception as e:
            logging.error(f"TTS failed while speaking: {e}")
            raise CustomException(e, sys)




'''
class TTSpy:
    """
    Text-To-Speech (TTS) engine wrapper for Jarvis using pyttsx3.
    
    Features:
    - Automatically selects voice engine based on OS
    - Speak text aloud
    - Logs TTS activity
    - Handles exceptions gracefully
    """

    def __init__(self):
        try:
            logging.info("Initializing TTS engine (pyttsx3)...")
            system = platform.system()
            if system == "Windows":
                self.engine = pyttsx3.init('sapi5')
            elif system == "Darwin":
                self.engine = pyttsx3.init('nsss')
            else:
                self.engine = pyttsx3.init('espeak')

            self.engine.setProperty('rate', 150)
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)
            logging.info(f"TTS engine initialized successfully on {system}")

        except Exception as e:
            logging.error(f"Failed to initialize TTS engine: {e}")
            raise CustomException(e, sys)

    def pyspeak(self, text: str):
        try:
            logging.info(f"TTS speaking: {text}")
            print(f"JARVIS : {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS failed while speaking: {e}")
            raise CustomException(e, sys)
        
    # FIXED: Added 'self' as first argument
    def speak(self, text: str):
        try:
            logging.info(f"TTS speaking: {text}")
            print(f"JARVIS : {text}")
            tts = gTTS(text, lang='en')
            tts.save("output.mp3")
            os.system("mpg123 output.mp3")
        except Exception as e:
            logging.error(f"TTS failed while speaking: {e}")
            raise CustomException(e, sys)

'''