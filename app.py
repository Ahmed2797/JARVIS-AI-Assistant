from jarvis.logger import logging
from jarvis.exception import CustomException

from jarvis.pipeline import Main
import sys

if __name__=='__main__':
    try:
        pipe = Main()
        pipe.main_voice_loop(
            
        )
        logging.info('Pipeline Completed')
    except Exception as e:
        raise CustomException(e,sys)



'''
🟦 1. “Jarvis, open YouTube and search for AI tutorials.”
➡️ Tests internet + search functionality.

🟩 2. “Jarvis, whats the weather today?”
➡️ Shows API call + data extraction.

🟪 3. “Jarvis, increase my laptop brightness to 80%.”
➡️ Hardware control (Linux).

🟧 4. “Jarvis, reduce the volume by 30%.”
➡️ System audio management.

🟨 5. “Jarvis, create a study plan for today.”
➡️ Task planning + LLM reasoning.

🟫 6. “Jarvis, tell me todays top news.”
➡️ News API + TTS response.

🟥 7. “Jarvis, calculate 45 multiplied by 5.”
➡️ Calculator intent.

🟩 8. “Jarvis, search Wikipedia for Machine Learning.”
➡️ Wiki lookup + summarization.

⬜ 9. “Jarvis, read my messages aloud.”
➡️ TTS + notification reading.

🟦 10. “Jarvis, who made you?”
➡️ Personality + general chat mode.

If you want, I can also:
✅ Design a graphical poster (image)
✅ Create a Canva-style layout
✅ Rewrite it in more professional

'''



