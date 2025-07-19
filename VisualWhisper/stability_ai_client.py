"""
Stability AI Client Module
Handles interactions with Stability AI API for text-to-image generation
"""

import os
import requests
import base64
from typing import Dict, Any
from PIL import Image
from io import BytesIO

class StabilityAIClient:
    """Stability AI client for text-to-image generation"""
    
    def __init__(self):
        self.api_key = os.getenv("STABILITY_AI_API_KEY")
        if not self.api_key:
            raise ValueError("STABILITY_AI_API_KEY environment variable is required")
        
        self.base_url = "https://api.stability.ai/v1/generation"
        self.engine = "stable-diffusion-xl-1024-v1-0"  # Using SDXL as default
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_image(self, prompt: str, negative_prompt: str = "", width: int = 1024, height: int = 1024) -> Dict[str, Any]:
        """
        Generate image using Stability AI text-to-image
        
        Args:
            prompt: Text prompt for image generation
            negative_prompt: What to avoid in the image
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            
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
            
            # Prepare text prompts
            text_prompts = [
                {"text": prompt, "weight": 1}
            ]
            
            if negative_prompt.strip():
                text_prompts.append({"text": negative_prompt, "weight": -1})
            
            # API request body
            body = {
                "text_prompts": text_prompts,
                "cfg_scale": 7,
                "height": height,
                "width": width,
                "samples": 1,
                "steps": 30,
                "seed": 0,
                "style_preset": "enhance"
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/{self.engine}/text-to-image",
                headers=self.headers,
                json=body,
                timeout=60
            )
            
            if response.status_code != 200:
                if response.status_code == 401:
                    error_msg = "Invalid API key. Please check your Stability AI key."
                elif response.status_code == 403:
                    error_msg = "Access denied. Your Stability AI account might need credits."
                elif response.status_code == 400:
                    error_msg = "Bad request. Check your prompt and parameters."
                else:
                    error_msg = f"API request failed: {response.status_code} - {response.text}"
                
                return {
                    "success": False,
                    "image_url": None,
                    "image_data": None,
                    "error": error_msg
                }
            
            # Process response
            data = response.json()
            
            if not data.get("artifacts"):
                return {
                    "success": False,
                    "image_url": None,
                    "image_data": None,
                    "error": "No image generated"
                }
            
            # Get the first generated image
            artifact = data["artifacts"][0]
            
            if artifact.get("finishReason") == "CONTENT_FILTERED":
                return {
                    "success": False,
                    "image_url": None,
                    "image_data": None,
                    "error": "Content filtered. Please modify your prompt."
                }
            
            # Decode base64 image
            image_data = base64.b64decode(artifact["base64"])
            pil_image = Image.open(BytesIO(image_data))
            
            return {
                "success": True,
                "image_url": None,  # Stability AI returns base64, not URL
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
            
            if len(prompt) > 2000:
                return {
                    "valid": False,
                    "enhanced_prompt": "",
                    "error": "Prompt is too long (maximum 2000 characters)"
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
    
    def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Placeholder for audio transcription - Stability AI focuses on image generation
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary with transcription result and status
        """
        return {
            "success": False,
            "text": "",
            "error": "Audio transcription not available with Stability AI. Please use text input instead."
        }