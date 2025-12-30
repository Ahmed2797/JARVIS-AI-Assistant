# jarvis_langchain.py

import os
import random
import datetime
import wikipedia
import webbrowser
import subprocess
import speech_recognition as sr
from gtts import gTTS
import playsound
from langchain import OpenAI
from langchain.agents import initialize_agent, Tool

# --------------------------
# 1️⃣ Text-to-Speech (TTS)
# --------------------------
def speak(text: str):
    """Convert text to speech using gTTS"""
    print(f"JARVIS: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# --------------------------
# 2️⃣ Speech-to-Text (STT)
# --------------------------
def take_voice_command():
    """Listen to microphone and convert speech to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("Sorry sir, I did not catch that.")
        return ""
    except Exception as e:
        speak("Error with voice recognition.")
        print(e)
        return ""

# --------------------------
# 3️⃣ Simple tools for commands
# --------------------------
def open_google(_):
    webbrowser.open("https://google.com")
    return "Opening Google sir"

def open_youtube(_):
    webbrowser.open("https://youtube.com")
    return "Opening YouTube sir"

def open_calculator(_):
    subprocess.Popen("calc.exe")
    return "Opening Calculator sir"

def open_notepad(_):
    subprocess.Popen("notepad.exe")
    return "Opening Notepad sir"

def wikipedia_search(query: str):
    try:
        search_query = query.replace('wikipedia', '').strip()
        results = wikipedia.summary(search_query, sentences=2)
        return results
    except:
        return "Sorry sir, I couldn't find information on that topic."

def tell_joke(_):
    jokes = [
        "Why don't scientists trust atoms? They make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!"
    ]
    return random.choice(jokes)

def play_music(_):
    music_dir = "D:\\music"  # Change to your music path
    if os.path.exists(music_dir):
        songs = [s for s in os.listdir(music_dir) if s.endswith(('.mp3', '.wav'))]
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            return f"Playing song: {song}"
        else:
            return "No songs found sir"
    return "Music directory not found"

# --------------------------
# 4️⃣ Configure LangChain Agent
# --------------------------
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.5, openai_api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    Tool(name="Google", func=open_google, description="Open Google website"),
    Tool(name="YouTube", func=open_youtube, description="Open YouTube website"),
    Tool(name="Calculator", func=open_calculator, description="Open Windows calculator"),
    Tool(name="Notepad", func=open_notepad, description="Open Windows Notepad"),
    Tool(name="Wikipedia", func=wikipedia_search, description="Search Wikipedia articles"),
    Tool(name="Joke", func=tell_joke, description="Tell a joke"),
    Tool(name="Music", func=play_music, description="Play music from folder")
]

agent = initialize_agent(tools, llm, agent_type="conversational-react-description")

# --------------------------
# 5️⃣ Main Voice Loop
# --------------------------
def main_voice_loop():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning sir! I am ready.")
    elif 12 <= hour < 18:
        speak("Good Afternoon sir! Listening to your commands.")
    else:
        speak("Good Evening sir! I am here for you.")

    while True:
        query = take_voice_command()
        if not query:
            continue

        if any(word in query for word in ["exit", "stop", "bye", "goodbye", "sleep"]):
            speak("Goodbye sir! Call me anytime.")
            break

        # Let LangChain agent decide the action
        response = agent.run(query)
        speak(response)

# --------------------------
# 6️⃣ Run Jarvis
# --------------------------
if __name__ == "__main__":
    speak("Starting Jarvis Voice Assistant...")
    main_voice_loop()




'''----------------------------------------------------------------------'''

from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langgraph.graph import Graph, END
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import requests
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class STTNode:
    """Speech-to-Text Node for microphone input"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def __call__(self, state: dict) -> dict:
        try:
            logger.info("Listening for speech input...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=10)
            
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized text: {text}")
            return {"user_input": text, "transcribed_text": text}
            
        except sr.WaitTimeoutError:
            return {"error": "No speech detected", "user_input": ""}
        except sr.UnknownValueError:
            return {"error": "Could not understand speech", "user_input": ""}
        except Exception as e:
            return {"error": f"STT error: {str(e)}", "user_input": ""}


'''
class TTSNode:
    """Text-to-Speech Node for output"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        # Configure voice properties
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)

    
    def __call__(self, state: dict) -> dict:
        action_result = state.get("action_result", "")
        user_input = state.get("user_input", "")
        
        if not action_result and user_input:
            # If no specific action result, respond to general input
            response_llm = ChatOpenAI(temperature=0.7)
            response = response_llm.invoke([HumanMessage(content=f"Respond to this user input: {user_input}")])
            action_result = response.content
        
        if action_result:
            try:
                self.engine.say(action_result)
                self.engine.runAndWait()
                return {"tts_output": action_result, "final_response": action_result}
            except Exception as e:
                logger.error(f"TTS error: {e}")
                return {"tts_output": "", "final_response": action_result}
        
        return {"tts_output": "", "final_response": "No response generated"}

'''





class TransistorNode:
    """Bangla to English Translation Node"""
    
    def __init__(self):
        # You can use any translation service or model
        self.llm = ChatOpenAI(temperature=0)  # or use a translation-specific model
        
    def __call__(self, state: dict) -> dict:
        user_input = state.get("user_input", "")
        
        # Simple detection for Bangla (you might want more sophisticated detection)
        if self._contains_bangla(user_input):
            try:
                # For production, use a proper translation service
                # This is a simplified version
                translation_prompt = f"""
                Translate the following Bangla text to English. If it's already in English, return it as is.
                
                Text: {user_input}
                
                Translation: """
                
                response = self.llm.invoke([HumanMessage(content=translation_prompt)])
                translated_text = response.content.strip()
                
                return {"translated_text": translated_text, "original_language": "bangla"}
                
            except Exception as e:
                logger.error(f"Translation error: {e}")
                return {"translated_text": user_input, "original_language": "unknown"}
        
        return {"translated_text": user_input, "original_language": "english"}

    def _contains_bangla(self, text: str) -> bool:
        """Simple check for Bangla characters"""
        bangla_range = range(0x0980, 0x09FF)
        return any(ord(char) in bangla_range for char in text)




class LLMIntentNode:
    """LLM-based Intent Parser Node"""
    
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.1, model="gpt-4")
        # Alternative: use Gemini
        # from langchain_google_genai import ChatGoogleGenerativeAI
        # self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        
    def __call__(self, state: dict) -> dict:
        user_input = state.get("translated_text", state.get("user_input", ""))
        
        intent_prompt = f"""
        Analyze the user's input and determine the intent. Choose from the following intents:
        - google_search: User wants to search something on Google
        - youtube_search: User wants to search or open YouTube
        - calculator: User wants to perform calculations
        - wikipedia: User wants Wikipedia information
        - music: User wants to play music
        - news: User wants news or jokes
        - weather: User wants weather information
        - study_planner: User wants study planning help
        - general: General conversation or unknown intent
        
        User Input: {user_input}
        
        Respond with ONLY a JSON object in this format:
        {{
            "intent": "detected_intent",
            "query": "extracted_search_query_or_main_content",
            "confidence": 0.95
        }}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=intent_prompt)])
            intent_data = json.loads(response.content.strip())
            
            logger.info(f"Detected intent: {intent_data}")
            return {"intent": intent_data}
            
        except Exception as e:
            logger.error(f"Intent parsing error: {e}")
            return {"intent": {"intent": "general", "query": user_input, "confidence": 0.0}}




class GoogleNode:
    """Google Search Node"""
    
    def __call__(self, state: dict) -> dict:
        intent_data = state.get("intent", {})
        query = intent_data.get("query", "")
        
        if query:
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
            return {"action_result": f"Opened Google search for: {query}", "action": "google_search"}
        
        webbrowser.open("https://www.google.com")
        return {"action_result": "Opened Google homepage", "action": "google_search"}




class YouTubeNode:
    """YouTube Search Node"""
    
    def __call__(self, state: dict) -> dict:
        intent_data = state.get("intent", {})
        query = intent_data.get("query", "")
        
        if query:
            search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(search_url)
            return {"action_result": f"Opened YouTube search for: {query}", "action": "youtube_search"}
        
        webbrowser.open("https://www.youtube.com")
        return {"action_result": "Opened YouTube homepage", "action": "youtube_search"}




class CalculatorNode:
    """Calculator Node (opens Notepad as per your diagram)"""
    
    def __call__(self, state: dict) -> dict:
        try:
            # Open notepad (Windows)
            os.system("notepad.exe")
            return {"action_result": "Opened Notepad for calculations", "action": "calculator"}
        except:
            return {"action_result": "Could not open Notepad", "action": "calculator"}




class WikipediaNode:
    """Wikipedia Node (opens Mullvad as per your diagram)"""
    
    def __call__(self, state: dict) -> dict:
        intent_data = state.get("intent", {})
        query = intent_data.get("query", "")
        
        if query:
            search_url = f"https://en.wikipedia.org/wiki/Special:Search?search={query}"
            webbrowser.open(search_url)
            return {"action_result": f"Opened Wikipedia search for: {query}", "action": "wikipedia"}
        
        webbrowser.open("https://www.wikipedia.org")
        return {"action_result": "Opened Wikipedia homepage", "action": "wikipedia"}




class MusicNode:
    """Music Player Node"""
    
    def __call__(self, state: dict) -> dict:
        intent_data = state.get("intent", {})
        query = intent_data.get("query", "")
        
        # For a real implementation, you might integrate with Spotify, YouTube Music, etc.
        if query:
            search_url = f"https://www.youtube.com/results?search_query={query}+music"
            webbrowser.open(search_url)
            return {"action_result": f"Searching music for: {query}", "action": "music"}
        
        webbrowser.open("https://www.youtube.com/")
        return {"action_result": "Opened music platform", "action": "music"}




class NewsNode:
    """News Node (tells jokes as per your diagram)"""
    
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
        ]
    
    def __call__(self, state: dict) -> dict:
        import random
        joke = random.choice(self.jokes)
        return {"action_result": joke, "action": "news"}




class WeatherNode:
    """Weather Node (study planner as per your diagram)"""
    
    def __call__(self, state: dict) -> dict:
        # Simple study planner implementation
        study_plan = self._generate_study_plan()
        return {"action_result": study_plan, "action": "weather_study_planner"}
    
    def _generate_study_plan(self) -> str:
        return f"""
        Study Plan for {datetime.now().strftime('%Y-%m-%d')}:
        
        Morning (8:00-11:00): Focus on difficult subjects
        Afternoon (14:00-16:00): Review and practice
        Evening (19:00-21:00): Light reading and preparation
        
        Remember to take breaks every 45 minutes!
        """




class TTSNode:
    """Text-to-Speech Node for output"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        # Configure voice properties
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)
    
    def __call__(self, state: dict) -> dict:
        action_result = state.get("action_result", "")
        user_input = state.get("user_input", "")
        
        if not action_result and user_input:
            # If no specific action result, respond to general input
            response_llm = ChatOpenAI(temperature=0.7)
            response = response_llm.invoke([HumanMessage(content=f"Respond to this user input: {user_input}")])
            action_result = response.content
        
        if action_result:
            try:
                self.engine.say(action_result)
                self.engine.runAndWait()
                return {"tts_output": action_result, "final_response": action_result}
            except Exception as e:
                logger.error(f"TTS error: {e}")
                return {"tts_output": "", "final_response": action_result}
        
        return {"tts_output": "", "final_response": "No response generated"}




class VoiceAssistantGraph:
    """Main Voice Assistant Graph"""
    
    def __init__(self):
        self.graph = Graph()
        self._build_graph()
        self.compiled_graph = None
        
    def _build_graph(self):
        # Define nodes
        self.graph.add_node("stt", STTNode())
        self.graph.add_node("transistor", TransistorNode())
        self.graph.add_node("llm_intent", LLMIntentNode())
        self.graph.add_node("google", GoogleNode())
        self.graph.add_node("youtube", YouTubeNode())
        self.graph.add_node("calculator", CalculatorNode())
        self.graph.add_node("wikipedia", WikipediaNode())
        self.graph.add_node("music", MusicNode())
        self.graph.add_node("news", NewsNode())
        self.graph.add_node("weather", WeatherNode())
        self.graph.add_node("tts", TTSNode())
        
        # Define edges and conditional routing
        self.graph.set_entry_point("stt")
        
        self.graph.add_edge("stt", "transistor")
        self.graph.add_edge("transistor", "llm_intent")
        
        # Conditional routing based on intent
        self.graph.add_conditional_edges(
            "llm_intent",
            self._route_by_intent,
            {
                "google": "google",
                "youtube": "youtube", 
                "calculator": "calculator",
                "wikipedia": "wikipedia",
                "music": "music",
                "news": "news",
                "weather": "weather",
                "general": "tts"
            }
        )
        
        # All action nodes lead to TTS for output
        self.graph.add_edge("google", "tts")
        self.graph.add_edge("youtube", "tts")
        self.graph.add_edge("calculator", "tts")
        self.graph.add_edge("wikipedia", "tts")
        self.graph.add_edge("music", "tts")
        self.graph.add_edge("news", "tts")
        self.graph.add_edge("weather", "tts")
        
        self.graph.add_edge("tts", END)
        
    def _route_by_intent(self, state: dict) -> str:
        intent_data = state.get("intent", {})
        intent = intent_data.get("intent", "general")
        return intent
    
    def compile(self):
        self.compiled_graph = self.graph.compile()
        return self.compiled_graph
    
    def run(self, input_data: dict = None):
        if self.compiled_graph is None:
            self.compile()
        
        initial_state = input_data or {"user_input": ""}
        return self.compiled_graph.invoke(initial_state)

# Usage example
def main():
    assistant = VoiceAssistantGraph()
    assistant.compile()
    
    print("Voice Assistant Started!")
    print("Speak into your microphone...")
    
    while True:
        try:
            # Run the graph
            result = assistant.run()
            
            print(f"\nFinal Result: {result.get('final_response', 'No response')}")
            print("\n" + "="*50)
            print("Listening again... (Press Ctrl+C to stop)")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()

