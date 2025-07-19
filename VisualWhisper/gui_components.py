import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from PIL import Image, ImageTk
import io


class VoiceToImageGUI:
    def __init__(self, root, audio_recorder=None, openai_client=None, stability_client=None):
        self.root = root
        self.audio_recorder = audio_recorder
        self.openai_client = openai_client
        self.stability_client = stability_client
        self.recording = False
        self.current_image = None
        self.current_image_tk = None
        
        # Determine which API provider to use for image generation
        if self.stability_client:
            self.api_provider = "Stability AI"
        elif self.openai_client:
            self.api_provider = "OpenAI"
        else:
            self.api_provider = "No API"
        
        # Initialize GUI components
        self.setup_gui()
        
        # Check microphone availability
        self.check_microphone()
    
    def setup_gui(self):
        """Set up the GUI layout"""
        # Configure root window
        self.root.title(f"Voice-to-Image Generator ({self.api_provider})")
        self.root.geometry("800x700")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Voice-to-Image Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Voice Recording Section
        voice_frame = ttk.LabelFrame(main_frame, text="Voice Recording", padding="10")
        voice_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        voice_frame.columnconfigure(1, weight=1)
        
        # Record button
        self.record_button = ttk.Button(
            voice_frame, 
            text="Start Recording", 
            command=self.toggle_recording
        )
        self.record_button.grid(row=0, column=0, padx=(0, 10))
        
        # Recording status
        self.recording_status = ttk.Label(voice_frame, text="Ready to record")
        self.recording_status.grid(row=0, column=1, sticky=(tk.W))
        
        # Audio devices info
        self.audio_info = ttk.Label(voice_frame, text="", foreground="gray")
        self.audio_info.grid(row=1, column=0, columnspan=2, sticky=(tk.W), pady=(5, 0))
        
        # Text Input Section
        text_frame = ttk.LabelFrame(main_frame, text="Text Input", padding="10")
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(
            text_frame, 
            height=4, 
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Clear button
        clear_button = ttk.Button(
            text_frame, 
            text="Clear Text", 
            command=self.clear_text
        )
        clear_button.grid(row=1, column=0, sticky=(tk.W))
        
        # Generation Section
        gen_frame = ttk.LabelFrame(main_frame, text="Image Generation", padding="10")
        gen_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        gen_frame.columnconfigure(1, weight=1)
        
        # Generate button
        self.generate_button = ttk.Button(
            gen_frame, 
            text="Generate Image", 
            command=self.generate_image
        )
        self.generate_button.grid(row=0, column=0, padx=(0, 10))
        
        # Generation status
        self.generation_status = ttk.Label(gen_frame, text="Ready to generate")
        self.generation_status.grid(row=0, column=1, sticky=(tk.W))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            gen_frame, 
            mode='indeterminate'
        )
        self.progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Image Display Section
        image_frame = ttk.LabelFrame(main_frame, text="Generated Image", padding="10")
        image_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Image display canvas
        self.image_canvas = tk.Canvas(
            image_frame, 
            bg="white", 
            relief=tk.SUNKEN, 
            borderwidth=2
        )
        self.image_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image scrollbars
        v_scrollbar = ttk.Scrollbar(image_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.image_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(image_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.image_canvas.configure(xscrollcommand=h_scrollbar.set)
        
        # Initial canvas text
        self.image_canvas.create_text(
            200, 100, 
            text="Generated image will appear here", 
            fill="gray", 
            font=("Arial", 12)
        )
        
        # Save button
        self.save_button = ttk.Button(
            image_frame, 
            text="Save Image", 
            command=self.save_image,
            state=tk.DISABLED
        )
        self.save_button.grid(row=2, column=0, pady=(10, 0))
    
    def check_microphone(self):
        """Check microphone availability and update UI"""
        if self.audio_recorder and self.audio_recorder.is_available():
            device_info = self.audio_recorder.get_device_info()
            self.audio_info.config(text=f"Microphone: {device_info}")
        else:
            self.audio_info.config(text="Audio recording not available")
            self.record_button.config(state=tk.DISABLED)
    
    def toggle_recording(self):
        """Toggle voice recording"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        if not self.audio_recorder or not self.audio_recorder.is_available():
            messagebox.showerror("Audio Error", "Audio recording is not available")
            return
        
        self.recording = True
        self.update_recording_ui(True)
        
        def record_thread():
            try:
                self.audio_recorder.start_recording()
                self.root.after(0, self.update_recording_status, "Recording started")
            except Exception as e:
                self.root.after(0, self.update_recording_status, f"Recording error: {str(e)}")
                self.recording = False
                self.root.after(0, self.update_recording_ui, False)
        
        threading.Thread(target=record_thread, daemon=True).start()
    
    def stop_recording(self):
        """Stop recording and transcribe"""
        if not self.recording:
            return
        
        self.recording = False
        self.update_recording_ui(False)
        self.update_recording_status("Processing audio...")
        
        def stop_and_transcribe():
            try:
                audio_file = self.audio_recorder.stop_recording()
                self.root.after(0, self.update_recording_status, "Transcribing audio...")
                
                # Use OpenAI for transcription (MonsterAPI doesn't have speech-to-text)
                if self.openai_client:
                    result = self.openai_client.transcribe_audio(audio_file)
                    
                    if result["success"]:
                        self.root.after(0, self.update_transcription, result["text"])
                        self.root.after(0, self.update_recording_status, "Transcription completed")
                    else:
                        self.root.after(0, self.update_recording_status, result["error"])
                else:
                    self.root.after(0, self.update_recording_status, 
                                  "Audio transcription requires OpenAI API key. Please use text input instead.")
            except Exception as e:
                self.root.after(0, self.update_recording_status, f"Error: {str(e)}")
        
        threading.Thread(target=stop_and_transcribe, daemon=True).start()
    
    def update_recording_ui(self, recording: bool):
        """Update recording UI state"""
        if recording:
            self.record_button.config(text="Stop Recording")
            self.recording_status.config(text="Recording...", foreground="red")
        else:
            self.record_button.config(text="Start Recording")
            self.recording_status.config(text="Ready to record", foreground="black")
    
    def update_recording_status(self, message: str):
        """Update recording status message"""
        self.recording_status.config(text=message)
    
    def update_transcription(self, text: str):
        """Update text input with transcribed text"""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, text)
    
    def clear_text(self):
        """Clear the text input area"""
        self.text_input.delete(1.0, tk.END)
    
    def generate_image(self):
        """Generate image from text in a separate thread"""
        prompt = self.text_input.get(1.0, tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Empty Prompt", "Please enter some text or record voice first.")
            return
        
        # Use the active API client for validation and generation
        active_client = self.stability_client if self.stability_client else self.openai_client
        
        # Validate prompt
        validation = active_client.validate_prompt(prompt)
        if not validation["valid"]:
            messagebox.showerror("Invalid Prompt", validation["error"])
            return
        
        def generation_thread():
            self.root.after(0, self.start_generation_ui)
            
            result = active_client.generate_image(prompt)
            
            if result["success"]:
                self.root.after(0, self.display_image, result["image_data"])
                self.root.after(0, self.update_generation_status, 
                              f"Image generated successfully using {self.api_provider}")
            else:
                self.root.after(0, self.update_generation_status, result["error"])
            
            self.root.after(0, self.stop_generation_ui)
        
        threading.Thread(target=generation_thread, daemon=True).start()
    
    def start_generation_ui(self):
        """Start generation UI feedback"""
        self.generate_button.config(state=tk.DISABLED)
        self.generation_status.config(text="Generating image...", foreground="blue")
        self.progress.start()
    
    def stop_generation_ui(self):
        """Stop generation UI feedback"""
        self.generate_button.config(state=tk.NORMAL)
        self.progress.stop()
    
    def update_generation_status(self, message: str):
        """Update generation status message"""
        self.generation_status.config(text=message)
    
    def display_image(self, pil_image: Image.Image):
        """Display generated image in the canvas"""
        try:
            # Store the original image
            self.current_image = pil_image
            
            # Get canvas dimensions
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # Canvas not initialized yet, use default size
                canvas_width = 400
                canvas_height = 300
            
            # Calculate scaling to fit image in canvas
            img_width, img_height = pil_image.size
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            scale = min(scale_x, scale_y, 1.0)  # Don't upscale
            
            # Resize image if needed
            if scale < 1.0:
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                display_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                display_image = pil_image
            
            # Convert to tkinter format
            self.current_image_tk = ImageTk.PhotoImage(display_image)
            
            # Clear canvas and display image
            self.image_canvas.delete("all")
            
            # Center the image in canvas
            canvas_center_x = canvas_width // 2
            canvas_center_y = canvas_height // 2
            
            self.image_canvas.create_image(
                canvas_center_x, canvas_center_y,
                image=self.current_image_tk,
                anchor=tk.CENTER
            )
            
            # Update scroll region
            self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
            
            # Enable save button
            self.save_button.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Image Display Error", f"Failed to display image: {str(e)}")
    
    def save_image(self):
        """Save the current image"""
        if not self.current_image:
            messagebox.showwarning("No Image", "No image to save")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.current_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save image: {str(e)}")
    def cleanup(self):
        """Clean up resources before closing"""
        if self.audio_recorder:
            self.audio_recorder.cleanup()
