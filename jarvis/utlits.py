
import os
import re 
import sys
import openai
import random
import datetime
import smtplib
import platform
import pyautogui
import pywhatkit
import subprocess
import webbrowser
from gtts import gTTS
import google.generativeai as genai
from email.message import EmailMessage


from jarvis.tts import TTSpy 
from jarvis.logger import logging 
from jarvis.exception import CustomException

from dotenv import load_dotenv

load_dotenv()

# Global TTS object
speak = TTSpy()


def translate_bangla_to_english(bangla_text: str) -> str:
    """
    Translate Bangla voice command to English equivalent.
    If no match found, returns original text.

    Args:
        bangla_text (str): Bangla text from speech recognition.

    Returns:
        str: Translated English command.
    """
    try:
        logging.info(f"Translating Bangla text: {bangla_text}")

        bangla_english_map = {
            # greetings
            'হ্যালো': 'hello', 'হাই': 'hi', 'কেমন আছ': 'how are you',
            'কেমন আছেন': 'how are you', 'ধন্যবাদ': 'thank you',
            'থ্যাঙ্কস': 'thanks',

            # Identity
            'তোমার নাম কি': 'what is your name',
            'তুমি কে': 'who are you',
            'কি তৈরি করেছ': 'who made you',
            'তোমার ক্রিয়েটর কে': 'who is your creator',

            # Time
            'সময় কি': 'what time is it',
            'কয়টা বাজে': 'what time is it',
            'টাইম বল': 'tell me time',
            'বর্তমান সময়': 'current time',

            # Music
            'গান বাজাও': 'play music',
            'সঙ্গীত চালাও': 'play music',
            'গান শুনি': 'play song',
            'মিউজিক চালু কর': 'play music',

            # Application opening
            'গুগল খোল': 'open google',
            'ইউটিউব খোল': 'open youtube',
            'ফেসবুক খোল': 'open facebook',
            'গিটহাব খোল': 'open github',
            'ক্যালকুলেটর খোল': 'open calculator',
            'নোটপ্যাড খোল': 'open notepad',
            'টার্মিনাল খোল': 'open terminal',

            # Info
            'আবহাওয়া কেমন': 'how is weather',
            'খবর বল': 'tell me news',
            'আজকের খবর': 'today news',
            'উইকিপিডিয়া': 'wikipedia',

            # Entertainment
            'কৌতুক বল': 'tell me joke',
            'জোকস বল': 'tell joke',
            'মজার কথা বল': 'say something funny',

            # System
            'বন্ধ কর': 'exit',
            'স্টপ': 'stop',
            'বিদায়': 'goodbye',
            'ঘুমাও': 'sleep'
        }

        text = bangla_text.lower()

        for bangla_phrase, english_phrase in bangla_english_map.items():
            if bangla_phrase in text:
                return english_phrase

        return text  

    except Exception as e:
        logging.error(f"Translation error: {e}")
        raise CustomException(e,sys)

def ai_voice():
    ai_sound = '/home/ahmed/project/JARVIS/music/ai_voice/start_sound.mp3'
    os.system(f"mpg123 -q '{ai_sound}'")

def click_type():
    ai_sound = '/home/ahmed/project/JARVIS/music/click_sound.mp3'
    os.system(f"mpg123 -q '{ai_sound}'")

def PlayYoutube(query):
    speak.speak(f"Playing {query} on YouTube")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

'''
def PlayYoutube(query,speak):
    """
    Plays a YouTube video based on user's query.

    Parameters:
    - query (str): The user's voice/text command
    - speak (object): Your TTSpy or TTS class instance
    """
    search_term = extract_yt_term(query)
    
    if search_term:
        speak.speak(f"Playing {search_term} on YouTube")
        pywhatkit.playonyt(search_term)
    else:
        speak.speak("Sorry, I couldn't find what to play on YouTube.")

def extract_yt_term(command):
    """
    Extracts the song/video name from a command string.
    Examples:
        "Play Despacito on YouTube" => "Despacito"
        "Can you play bad guy on YouTube?" => "bad guy"
    """
    # Flexible pattern: looks for "play ... on youtube"
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    
    if match:
        return match.group(1)
    
    # fallback: just look for "play ..." if "on YouTube" is missing
    fallback_pattern = r'play\s+(.*)'
    match = re.search(fallback_pattern, command, re.IGNORECASE)
    return match.group(1) if match else None
'''

def voice_getting():
    """
    Greets the user based on current time.
    """
    try:
        hour = datetime.datetime.now().hour
        logging.info(f"Greeting based on hour: {hour}")

        if 0 < hour <= 12:
            speak.speak("Good Morning sir! I am listening to your voice commands.")
        elif 12 <= hour < 18:
            speak.speak("Good Afternoon sir! I am listening to your voice commands.")
        else:
            speak.speak("Good Evening sir! I am here for your voice commands.")
        
        speak.speak("Hello Sir, how may I assist you today?")

    except Exception as e:
        logging.error(f"voice_getting() failed: {e}")
        raise CustomException(e,sys)

def open_app(path_or_command):
    """
    Opens a file, folder, or application in a cross-platform way.

    Args:
        path_or_command (str or list): Path to file/folder or list of command for app.
    """
    system = platform.system()
    try:
        if isinstance(path_or_command, str):
            # Open file/folder
            if system == "Windows":
                os.startfile(path_or_command)
            elif system == "Darwin":
                subprocess.Popen(["open", path_or_command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            else:  # Linux
                subprocess.Popen(["xdg-open", path_or_command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

        elif isinstance(path_or_command, list):
            # Open application by command
            subprocess.Popen(path_or_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

        else:
            print("Invalid path or command type.")

    except Exception as e:
        print(f"Failed to open {path_or_command}: {e}")

def voice_play_music():
    """
    Plays random music from the music directory.
    """
    try:
        music_dir = '/home/ahmed/project/JARVIS/music'
        logging.info(f"Looking for music in: {music_dir}")

        if os.path.exists(music_dir):
            songs = os.listdir(music_dir)
            if songs:
                random_song = random.choice(songs)
                song_path = os.path.join(music_dir, random_song)
                speak.speak(f"Playing a random song: {random_song}")
                os.system(f"mpg123 -q '{song_path}'")
                #subprocess.call(["xdg-open", music_dir])
            else:
                speak.speak("No songs found in the music folder.")
        else:
            speak.speak("Music directory not found.")

    except Exception as e:
        logging.error(f"Music play error: {e}")
        raise CustomException(e,sys)

def voice_study_routine():
    """
    Speaks out the user's daily study routine.
    Jarvis will read tasks in order, hour by hour.
    """
    try:
        speak.speak("Here is your study routine for today sir")

        study_plan = [
            "At 7 AM, you will start coding and practice your InceptionBD assignment.",
            "At 9 AM, you will attend daily work purpose.",
            "At 11 AM, you will continue learning LangGraph and ComputerVision.",
            "At 1 PM, take a lunch break and relax.",
            "At 2 PM, work on your Machine Learning project.",
            "At 4 PM, revise today's topics and notes.",
            "At 5 PM, take a short break and have some refreshment.",
            "At 7 PM, practice coding problems or exercises.",
            "At 9 PM, you will attend your live class InceptionBD.CTO, Boktiar Ahmed Bappy."
        ]

        for task in study_plan:
            speak.speak(task)

    except Exception as e:
        logging.error(f"Failed to read study routine: {e}")
        raise CustomException(e,sys)

def gemini_model_response(user_input: str) -> str:
    """
    Gets AI response from Gemini model based on user query.

    Args:
        user_input (str): User's text command.

    Returns:
        str: Model-generated response.
    """
    try:
        logging.info("Generating AI response from Gemini...")

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        gemini_model_name = os.getenv("GEMINI_MODEL_NAME")

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(gemini_model_name)

        prompt = f"""
        You are JARVIS from Iron Man. 
        The user gave this voice command: '{user_input}'.
        Respond in English only.
        Be concise, helpful, and conversational.
        Keep responses under 2 sentences.
        """

        response = model.generate_content(prompt)
        text = response.text.strip()

        logging.info("Gemini response generated successfully.")
        return text

    except Exception as e:
        logging.error(f"Gemini model error: {e}")
        raise CustomException(e,sys)

def handle_who_made_you():
    speak.speak("I was created by Tanvir Ahmed. Who is inspiring Boktiar Ahmed Bappy and the Inception BD team.")

def set_brightness(level):
    os.system(f"brightnessctl set {level}%")
    print(f"Brightness set to {level}%")

def set_volume(level):
    os.system(f"amixer sset 'Master' {level}%")
    print(f"Volume set to {level}%")

def volume_up():
    os.system("amixer sset 'Master' 10%+")
    print("Volume increased")

def volume_down():
    os.system("amixer sset 'Master' 10%-")
    print("Volume decreased")

def mute():
    os.system("amixer sset 'Master' mute")
    print("Muted")

def unmute():
    os.system("amixer sset 'Master' unmute")
    print("Unmuted")

def wifi_off():
    os.system("nmcli radio wifi off")
    print("Wi-Fi turned OFF")

def wifi_on():
    os.system("nmcli radio wifi on")
    print("Wi-Fi turned ON")

def open_app(app_name):
    os.system(f"{app_name} &")

def close_app(app_process):
    os.system(f"pkill {app_process}")
    
def send_whatsapp_message(phone: str, message: str):
    """
    Send WhatsApp message instantly.
    Requires WhatsApp Web to be logged in.
    """
    try:
        logging.info(f"Sending WhatsApp message to {phone} : {message}")
        print(f"JARVIS : Sending message to {phone}")

        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=2,  
            tab_close=True,
            close_time=3
        )
        # Press Enter to actually send
        pyautogui.press("enter")
        
        speak.speak("Message sent successfully!")

    except Exception as e:
        logging.error(f"WhatsApp message sending failed: {e}")
        print("JARVIS : Unable to send message. Please check connection/QR login.")

def open_terminal():
    os.system("gnome-terminal &")

def send_email(receiver, subject, body):
    sender = "tanvirahmed754575@gmail.com"
    
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)


# ================== GPT Code Generator ==================
def gpt_generate_code(instruction, code_context=""):
    prompt = f"Here is the existing Python code:\n{code_context}\nInstruction: {instruction}\nProvide full Python code only."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0
    )
    return response.choices[0].text.strip()

# ================== Run & Fix Errors ==================
def run_and_fix(file_path):
    result = subprocess.run(["python", file_path], capture_output=True, text=True)
    if result.stderr:
        print("Errors detected. Fixing...")
        with open(file_path, "r") as f:
            context = f.read()
        fixed_code = gpt_generate_code(f"Fix these errors:\n{result.stderr}", context)
        with open(file_path, "w") as f:
            f.write(fixed_code)
        pyautogui.write(fixed_code, interval=0.02)
        print("Errors fixed!")
    else:
        print(result.stdout)

# ================== Process Command ==================
def process_command(command, current_file):
    cmd = command.lower()
    
    if cmd.startswith("create file"):
        file_name = cmd.replace("create file", "").strip()
        if not file_name.endswith(".py"):
            file_name += ".py"
        open(file_name, "w").close()
        print(f"Created new file: {file_name}")
        return "", file_name

    if cmd == "run file":
        run_and_fix(current_file)
        return "", current_file

    if cmd in ["new line", "enter"]:
        pyautogui.press("enter")
        return "", current_file

    if cmd == "tab":
        pyautogui.press("tab")
        return "", current_file

    if cmd == "save file":
        pyautogui.hotkey("ctrl", "s")
        return "", current_file

    # Generate code
    with open(current_file, "r") as f:
        context = f.read()
    code_to_type = gpt_generate_code(command, context)
    return code_to_type, current_file


