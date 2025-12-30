import openai
import speech_recognition as sr
import pyautogui
import subprocess
import time
import os
from config import OPENAI_API_KEY, DEFAULT_FILE, LISTEN_PHRASE_TIME

# ================== Setup ==================
openai.api_key = OPENAI_API_KEY
recognizer = sr.Recognizer()
mic = sr.Microphone()
current_file = DEFAULT_FILE

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

# ================== Main Loop ==================
print("Jarvis v5 ready. Say 'exit' to stop.")

while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=LISTEN_PHRASE_TIME)
        
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")

        if "exit" in speech_text.lower():
            print("Jarvis stopped.")
            break

        code_to_type, current_file = process_command(speech_text, current_file)
        if code_to_type:
            pyautogui.write(code_to_type, interval=0.02)
            pyautogui.press("enter")
            pyautogui.press("enter")
    
    except sr.UnknownValueError:
        pass  # ignore unrecognized speech
    except Exception as e:
        print("Error:", e)
