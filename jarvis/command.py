from jarvis.logger import logging
from jarvis.exception import CustomException
from jarvis.utlits import *
from jarvis.tts import TTSpy

import speech_recognition as sr
import wikipedia 
import webbrowser 
import random 
import subprocess  
import sys
import datetime 
import os



class Command:
    """
    Command class handles voice interaction, speech recognition,
    command execution, and tool automation for JARVIS voice assistant.
    """

    def __init__(self):
        try:
            self.speak = TTSpy()
            logging.info("TTS Engine (TTSpy) initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize TTS engine.")
            raise CustomException(e, sys)


    def take_voice_command(self):
        r = sr.Recognizer()

        while True:
            try:
                with sr.Microphone() as source:
                    logging.info("Listening...")
                    print('Microphone Started...')
                    self.speak.speak('I am listening, sir.')

                    r.adjust_for_ambient_noise(source)
                    r.pause_threshold = 1
                    audio = r.listen(source)

                # Try Bangla first
                try:
                    english_query = r.recognize_google(audio, language='en-IN')
                    logging.info(f"English speech detected: {english_query}")
                    print("English query:", english_query)
                    return english_query.lower()

                # except Exception as e:
                #     logging.warning("English STT failed, trying Bangla...")
                #     try:
                #         bangla_query = r.recognize_google(audio, language='bn-BD')
                #         logging.info(f"Bangla speech detected: {bangla_query}")
                #         print("Bangla query:", bangla_query)

                #         english_query = translate_bangla_to_english(bangla_query)
                #         print("Translated to English:", english_query)
                #         return english_query.lower()
                        
                except Exception as e:
                    logging.warning("Speech not recognized, retrying...")
                    print("Speech not recognized, please try again.")
                    continue

            except Exception as e:
                logging.error("Microphone/STT error")
                raise CustomException(e, sys)


    def execute_all_command(self, query):
        logging.info(f"Executing command: {query}")
        print("Executing command:", query)

        try:
            # NAME & ABOUT
            if "name" in query and "your" in query:
                self.speak.speak("My name is Jarvis")

            elif "who made you" in query or "who created you" in query or "who built you" in query:
                handle_who_made_you()
                return

            # TIME
            elif "time" in query or "clock" in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                self.speak.speak(f"The time is {current_time}, sir")

            # MUSIC
            elif "music" in query or "song" in query:
                voice_play_music()

            # CALCULATOR (Linux)
            elif "calculator" in query:
                self.speak.speak("Opening calculator, sir")
                subprocess.Popen(["gnome-calculator"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
                # subprocess.Popen(["gnome-calculator"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                # open_app(["gnome-calculator"])

            elif "vs code" in query or "vscode" in query:
                self.speak.speak("Opening VS Code, sir")
                subprocess.Popen(
                    ["code"], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL, 
                    start_new_session=True
                )
                # Optional: generate or type code after opening VS Code
                code_to_type, current_file = process_command(query, current_file)
                if code_to_type:
                    pyautogui.write(code_to_type, interval=0.02)
                    pyautogui.press("enter")
                    pyautogui.press("enter")

            # TERMINAL (Linux)
            elif "terminal" in query or "console" in query:
                self.speak.speak("Opening terminal, sir")
                open_terminal()
                #subprocess.Popen(["gnome-terminal"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

            elif "whats-up" in query or "open whatsapp" in query:
                # Ask Jarvis user for number
                self.speak.speak("Whom should I send the message to? Please provide the phone number with country code.")
                number = input('Enter number:'+'+88')
                if not number.startswith("+"):
                    number = "+88" + number

                #number = self.take_voice_command()  # Your existing STT function

                # Ask Jarvis user for the message
                self.speak.speak("What should I say?")
                msg = input("Enter msg:")
                #msg = self.take_voice_command()

                # Send WhatsApp message
                send_whatsapp_message(number, msg)

            elif "send email" in query or "open email" in query:
                self.speak.speak("Sir, whom should I send the email to?")
                receiver = input("Enter email: ")
                #receiver = self.takeCommand() + "@gmail.com"

                self.speak.speak("What should be the subject?")
                subject = input("Subject: ")
                #subject = self.takeCommand()

                self.speak.speak("What is the message?")
                body = input("Message: ")
                #body = self.takeCommand()

                send_email(receiver, subject, body)
                self.speak.speak("Email has been sent successfully.")





            # # SOCIAL MEDIA / WEB
            # elif "facebook" in query:
            #     self.speak.speak("Opening Facebook, sir")
            #     webbrowser.open("https://facebook.com")

            # elif "linkedin" in query:
            #     self.speak.speak("Opening LinkedIn, sir")
            #     webbrowser.open("https://linkedin.com")

            # elif "google" in query:
            #     self.speak.speak("Opening Google, sir")
            #     webbrowser.open("https://google.com")

            elif "youtube" in query:
                self.speak.speak("Opening YouTube, sir")
                self.speak.speak(f'{query} here')
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                #PlayYoutube(query=query,speak=self.speak)
                
            # SOCIAL MEDIA / WEB
            elif "open" in query:
                site = query.replace("open", "").strip()
                self.speak.speak(f"Opening {site}, sir")
                webbrowser.open(f"https://{site}.com")

            # WIKIPEDIA
            elif "wikipedia" in query:
                search = query.replace("wikipedia", "").strip()
                if search:
                    try:
                        results = wikipedia.summary(search, sentences=2)
                        self.speak.speak("According to Wikipedia")
                        self.speak.speak(results)
                    except Exception:
                        self.speak.speak("Sorry sir, I could not find that.")

            # JOKES
            elif "joke" in query or "funny" in query:
                jokes = [
                    "Why did the computer get cold? Because it forgot to close Windows!",
                    "Why do programmers prefer dark mode? Because light attracts bugs!",
                    "Why was the JavaScript developer sad? He didn't Node how to Express himself!"
                ]
                joke = random.choice(jokes)
                self.speak.speak(joke)

            # STUDY ROUTINE
            elif "study routine" in query or "study plan" in query:
                self.speak.speak("Here is your study routine, sir")
                voice_study_routine()

            # SYSTEM CONTROL
            elif "brightness" in query:
                if "up" in query or "increase" in query:
                    set_brightness(80)
                elif "down" in query or "decrease" in query:
                    set_brightness(40)

            elif "volume" in query:
                if "up" in query or "increase" in query:
                    volume_up()
                elif "down" in query or "decrease" in query:
                    volume_down()
            elif "mute" in query:
                mute()

            elif "wifi on" in query:
                wifi_on()

            # EXIT
            elif "exit" in query or "stop" in query or "bye" in query:
                self.speak.speak("Goodbye, sir!")
                return "exit"

            # FALLBACK AI
            else:
                try:
                    response = gemini_model_response(query)
                    self.speak.speak(response)
                except Exception as e:
                    logging.error(f"AI response failed: {e}")
                    self.speak.speak("Sorry sir, I cannot answer that right now.")

        except Exception as e:
            logging.error("Error executing command")
            raise CustomException(e, sys)
