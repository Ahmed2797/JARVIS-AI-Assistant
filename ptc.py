from gtts import gTTS
import os

text = """Hello everyone, I'm here to work on and share amazing projects.

Today, I'm excited to present a brain tumor detection API built with FastAPI.

Here's how it works:

First, I upload an MRI image and the system processes it automatically.

The AI model predicts whether a tumor is present or not.

You'll see three action buttons on the interface.

You just need to select a button or simply press it and the backend processes the request automatically.

Let me explain what each button does:

Predict VGG performs tumor classification and shows the confidence score.

Detect YOLO identifies tumor regions and draws bounding boxes on the image.

Segment SAM provides precise segmentation, highlighting the affected area at the pixel level.

The amazing part? This entire pipeline runs through a single API.

This project is built using VGG, YOLO, SAM, OpenCV, and FastAPI."""

# Create TTS
tts = gTTS(text=text, lang='en', slow=True)
tts.save("brain_tumor_api_demo.mp3")
print("Audio saved as brain_tumor_api_demo.mp3")

