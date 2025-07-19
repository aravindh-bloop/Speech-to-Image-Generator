"""
OpenAI API Client Module
Handles interactions with OpenAI Whisper and DALL-E APIs
"""

import os
import requests
from openai import OpenAI
from typing import Optional, Dict, Any
import tempfile
import base64
from io import BytesIO
from PIL import Image

class OpenAIClient:
    """OpenAI API client for Whisper and DALL-E"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using OpenAI Whisper
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary with transcription result and status
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                # do not change this unless explicitly requested by the user
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            return {
                "success": True,
                "text": response.strip(),
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "error": f"Transcription failed: {str(e)}"
            }
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """
        Generate image using DALL-E
        
        Args:
            prompt: Text prompt for image generation
            size: Image size (1024x1024, 1792x1024, or 1024x1792)
            
        Returns:
            Dictionary with image data and status
        """
        try:
            if not prompt.strip():
                return {
                    "success": False,
                    "image_url": None,
                    "image_data": None,
                    "error": "Empty prompt provided"
                }
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size=size,
                quality="standard",
                response_format="url"
            )
            
            image_url = response.data[0].url
            
            # Download the image
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            
            # Convert to PIL Image
            image_data = BytesIO(image_response.content)
            pil_image = Image.open(image_data)
            
            return {
                "success": True,
                "image_url": image_url,
                "image_data": pil_image,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "image_url": None,
                "image_data": None,
                "error": f"Image generation failed: {str(e)}"
            }
    
    def validate_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Validate and potentially enhance the prompt
        
        Args:
            prompt: User input prompt
            
        Returns:
            Dictionary with validation result
        """
        try:
            prompt = prompt.strip()
            
            if not prompt:
                return {
                    "valid": False,
                    "enhanced_prompt": "",
                    "error": "Prompt cannot be empty"
                }
            
            if len(prompt) < 3:
                return {
                    "valid": False,
                    "enhanced_prompt": "",
                    "error": "Prompt is too short (minimum 3 characters)"
                }
            
            if len(prompt) > 1000:
                return {
                    "valid": False,
                    "enhanced_prompt": "",
                    "error": "Prompt is too long (maximum 1000 characters)"
                }
            
            return {
                "valid": True,
                "enhanced_prompt": prompt,
                "error": None
            }
            
        except Exception as e:
            return {
                "valid": False,
                "enhanced_prompt": "",
                "error": f"Prompt validation failed: {str(e)}"
            }
