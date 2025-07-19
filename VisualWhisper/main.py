#!/usr/bin/env python3
"""
Voice-to-Image Generation Desktop Application
Main entry point for the tkinter GUI application
"""
from dotenv import load_dotenv
load_dotenv()

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from gui_components import VoiceToImageGUI

def main():
    """Main function to initialize and run the application"""
    # Check for required API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("STABILITY_AI_API_KEY"):
        messagebox.showerror(
            "API Key Missing",
            "Please set either OPENAI_API_KEY or STABILITY_AI_API_KEY environment variable before running the application."
        )
        return
    
    # Create and configure the main window
    root = tk.Tk()
    root.title("Speech-to-Image Generator")
    root.geometry("800x700")
    root.resizable(True, True)
    
    # Set minimum window size
    root.minsize(600, 500)
    
    # Create the main application
    app = VoiceToImageGUI(root)
    
    # Handle window closing
    def on_closing():
        """Handle application shutdown"""
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
