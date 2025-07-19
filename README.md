#  Speech-to-Image Generator (Stability AI)

Transform your **voice or text prompts into stunning AI-generated images** using this beautiful, modern desktop app with a dark neon-themed GUI — powered by **Stability AI (SDXL)** and optionally **OpenAI** for speech-to-text.
# A perfect sppech to image generator made with stability ai. 
# How to run it in your machine?
* Install the packages
* get you api keys for open ai and stability ai , and create a .env file, and make modifications in the main.py file or simply add them as environment variables. 

---

##  Features

-  Record voice input and convert it into text using OpenAI Whisper
-  Enter text prompts directly
-  Generate high-quality 1024x1024 images via Stability AI's SDXL
-  Save your AI-generated masterpieces
-  Beautiful neon dark UI using Tkinter
-  Supports both voice and text-to-image workflows
-  Intelligent status updates and error handling

---

##  Installation

### 1. Clone the Repository

bash
git clone https://github.com/yourusername/VisualWhisper.git
cd VisualWhisper
2. Create a Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate   # On Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist, manually install:

bash
Copy
Edit
pip install sounddevice pillow requests openai numpy python-dotenv
 Set Your API Keys
The app requires:

Stability AI API Key for image generation

(Optional) OpenAI API Key for voice-to-text transcription

Create a .env file in the root directory and add:

env
Copy
Edit
STABILITY_AI_API_KEY=your-stability-ai-api-key
OPENAI_API_KEY=your-openai-api-key
 Running the App
After setting the keys:

bash
Copy
Edit
python main.py
The app window will launch with a stylish interface ready to convert your ideas into images!

 Project Structure
bash
Copy
Edit
VisualWhisper/
│
├── audio_recorder.py         # Handles microphone input
├── openai_client.py          # Handles speech-to-text with OpenAI
├── stability_ai_client.py    # Handles image generation using SDXL
├── gui_components.py         # All GUI layout and styling (neon themed)
├── main.py                   # Entry point of the app
├── .env                      # Your secret API keys (never commit this!)
├── requirements.txt          # Dependencies
└── README.md                 # This file
 Screenshots
Add screenshots of the GUI and generated images here

 To-Do
 Add language translation support

 Add model selection dropdown

 Upload image history view

 Add theming toggle (dark / light)

 License
This project is licensed under the MIT License. Feel free to fork, modify, and share!

 Credits
Stability AI — Image generation

OpenAI — Speech-to-text (Whisper)

Built with using Python & Tkinter

 Contact
Have ideas, suggestions, or bugs? Open an issue or email me at aravindhshankar.r@gmail.com
-Aravindh

