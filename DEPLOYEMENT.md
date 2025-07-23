# 🚀 Deployment Guide

## 1. System Requirements
- **Python**: 3.11 or higher
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Hardware**: Microphone (built-in or external)
- **API Key**: [Get Stability AI key](https://platform.stability.ai/)

## 2. Step-by-Step Setup

### A. Clone the Repository
```bash
git clone https://github.com/your-username/speech-to-image.git
cd speech-to-image
B. Set Up Virtual Environment (Recommended)
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

C. Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt
D. Configure API Key
Create .env file in project root

Add your API key:

env
STABILITY_API_KEY=your_api_key_here

3. Running the Application

Normal Mode
python speechtoimage.py
Debug Mode (For troubleshooting)
python -O speechtoimage.py 2> debug.log

4. Build Executable (Optional)

pip install pyinstaller
pyinstaller --onefile --windowed --icon=app.ico speechtoimage.py
Output: dist/speechtoimage.exe

5. Troubleshooting

Error	Solution
No module named 'dotenv'	Run pip install python-dotenv
Microphone not detected	Check system sound settings
API 401 Error	Verify .env file exists with correct key
Pillow installation fails	Install system dependencies first:
brew install libjpeg (macOS)
sudo apt-get install libjpeg-dev (Linux)

6. Docker Deployment (Advanced)

dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "speechtoimage.py"]
Build and run:

docker build -t speech-to-image .
docker run -e STABILITY_API_KEY=your_key speech-to-image

7. Uninstall

deactivate  # Exit virtual environment
rm -rf venv/  # Remove virtual environment
Note: Always keep your .env file private! Never commit it to version control.


### Key Features:
1. **Multi-OS Support**: Clear instructions for Windows/macOS/Linux
2. **Troubleshooting Table**: Quick solutions to common errors
3. **Optional Builds**: EXE creation and Docker support
4. **Safety Notes**: Reminders about API key security

Would you like me to add any specific sections like:
- Cloud deployment (AWS/Azure)
- CI/CD pipeline setup
- Multi-user configuration?
New chat

