import os
import threading
from dotenv import load_dotenv
import speech_recognition as sr
import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from io import BytesIO

# Load environment variables
load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

class SpeechToImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Image Generator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        self.center_window()
        self.create_widgets()
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.current_image = None

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Speech to Image Generator", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=(0, 20))

        text_frame = ttk.LabelFrame(main_frame, text="Transcribed Text", padding=10)
        text_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.text_display = tk.Text(text_frame, height=5, wrap=tk.WORD, font=("Segoe UI", 10), padx=5, pady=5)
        self.text_display.pack(fill=tk.BOTH, expand=True)

        self.mic_button = ttk.Button(main_frame, text="🎤 Start Recording", command=self.toggle_recording)
        self.mic_button.pack(pady=10)

        self.status_label = ttk.Label(main_frame, text="Ready to record", font=("Segoe UI", 9))
        self.status_label.pack()

        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=300, mode='indeterminate')

        image_frame = ttk.LabelFrame(main_frame, text="Generated Image", padding=10)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(main_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=10)

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.mic_button.config(text="🎤 Recording... Click to Stop")
        self.status_label.config(text="Recording... Speak now")
        self.text_display.delete(1.0, tk.END)
        threading.Thread(target=self.record_and_transcribe, daemon=True).start()

    def stop_recording(self):
        self.is_recording = False
        self.mic_button.config(text="🎤 Start Recording")
        self.status_label.config(text="Processing audio...")

    def record_and_transcribe(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = None
                
                while self.is_recording:
                    try:
                        audio = self.recognizer.listen(source, timeout=3)
                    except sr.WaitTimeoutError:
                        continue
                
                if audio:
                    try:
                        text = self.recognizer.recognize_google(audio)
                        self.root.after(0, self.update_transcribed_text, text)
                        self.root.after(0, self.generate_image, text)
                    except sr.UnknownValueError:
                        self.root.after(0, self.update_status, "Could not understand audio")
                    except sr.RequestError:
                        self.root.after(0, self.update_status, "Speech recognition service error")
                else:
                    self.root.after(0, self.update_status, "No audio recorded")
        except OSError:
            self.root.after(0, self.show_error, "Microphone not found")
            self.root.after(0, self.reset_ui)

    def update_transcribed_text(self, text):
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)

    def update_status(self, message):
        self.status_label.config(text=message)

    def reset_ui(self):
        self.is_recording = False
        self.mic_button.config(text="🎤 Start Recording")
        self.status_label.config(text="Ready to record")

    def generate_image(self, prompt):
        self.progress.pack(pady=10)
        self.progress.start()
        self.status_label.config(text="Generating image...")
        threading.Thread(target=self.call_stability_api, args=(prompt,), daemon=True).start()

    def call_stability_api(self, prompt):
        """FIXED API CALL - uses correct multipart format"""
        try:
            headers = {
                "authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "image/*"
            }
            
            # CORRECTED: Using multipart form-data
            files = {'none': ('', '')}  # Required empty file part
            data = {
                'prompt': prompt,
                'output_format': 'png'
            }
            
            response = requests.post(
                STABILITY_API_URL,
                headers=headers,
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                self.root.after(0, self.display_image, image)
                self.root.after(0, self.update_status, "Image generated successfully")
            else:
                error_msg = f"API Error {response.status_code}: {response.text[:100]}..."
                self.root.after(0, self.show_error, error_msg)
        except Exception as e:
            self.root.after(0, self.show_error, f"Network error: {str(e)}")
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, self.progress.pack_forget)

    def display_image(self, image):
        max_width = 550
        max_height = 350
        width, height = image.size
        ratio = min(max_width/width, max_height/height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.current_image = image
        self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save Image As"
            )
            if file_path:
                try:
                    self.current_image.save(file_path)
                    self.update_status(f"Image saved to {file_path}")
                except Exception as e:
                    self.show_error(f"Failed to save image: {str(e)}")

    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.reset_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToImageApp(root)
    root.mainloop()