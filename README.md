# 🎤 Speech to Image Generator

Convert spoken words into AI-generated images using Stability AI's API.

## Features
- Voice recording with microphone
- Real-time speech-to-text conversion
- AI image generation from transcribed text
- Save generated images to disk

## Prerequisites
- Python 3.11+
- Microphone (built-in or external)
- [Stability AI API key](https://platform.stability.ai/)

---

## **DEPLOYMENT.md**
# Deployment Guide

## 1. Local Setup

### Windows/macOS/Linux

# Clone repository
git clone https://github.com/your-username/speech-to-image.git
cd speech-to-image

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "STABILITY_API_KEY=your_api_key_here" > .env
2. Running the Application
bash
python speechtoimage.py
3. Troubleshooting
Error	Solution
ModuleNotFoundError	Re-run pip install -r requirements.txt
Microphone not found	Check sound device permissions
API errors	Verify .env contains valid key
4. Build Executable (Optional)
bash
pip install pyinstaller
pyinstaller --onefile --windowed speechtoimage.py
# Output: dist/speechtoimage.exe





