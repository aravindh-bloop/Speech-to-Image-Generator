"""
Audio Recording Module
Handles audio recording and processing using sounddevice
"""

import numpy as np
import threading
import time
import wave
import tempfile
import os
from typing import Callable, Optional

# Try to import sounddevice, handle gracefully if not available
try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except (ImportError, OSError) as e:
    AUDIO_AVAILABLE = False
    print(f"Audio not available: {e}")
    # Create a mock sounddevice module for fallback
    class MockSoundDevice:
        def query_devices(self, kind=None):
            return None
        def InputStream(self, *args, **kwargs):
            return None
    sd = MockSoundDevice()

class AudioRecorder:
    """Audio recorder class using sounddevice"""
    
    def __init__(self, sample_rate: int = 44100, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.stream = None
        self.temp_file_path = None
        
    def start_recording(self, callback: Optional[Callable] = None):
        """Start recording audio"""
        if not AUDIO_AVAILABLE:
            if callback:
                callback("Audio recording not available on this system")
            return False
            
        if self.recording:
            return False
            
        try:
            self.recording = True
            self.audio_data = []
            
            # Audio callback function
            def audio_callback(indata, frames, time, status):
                if status:
                    print(f"Audio status: {status}")
                if self.recording:
                    self.audio_data.append(indata.copy())
            
            # Start the audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=audio_callback,
                dtype=np.float32
            )
            
            self.stream.start()
            
            if callback:
                callback("Recording started")
                
            return True
            
        except Exception as e:
            self.recording = False
            if callback:
                callback(f"Failed to start recording: {str(e)}")
            return False
    
    def stop_recording(self, callback: Optional[Callable] = None) -> Optional[str]:
        """Stop recording and save to temporary file"""
        if not self.recording:
            return None
            
        try:
            self.recording = False
            
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            
            if not self.audio_data:
                if callback:
                    callback("No audio data recorded")
                return None
            
            # Combine all audio chunks
            audio_array = np.concatenate(self.audio_data, axis=0)
            
            # Convert to int16 for WAV file
            audio_int16 = (audio_array * 32767).astype(np.int16)
            
            # Create temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(
                suffix='.wav', 
                delete=False
            )
            self.temp_file_path = temp_file.name
            temp_file.close()
            
            # Save audio to WAV file
            with wave.open(self.temp_file_path, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_int16.tobytes())
            
            if callback:
                callback("Recording stopped and saved")
                
            return self.temp_file_path
            
        except Exception as e:
            self.recording = False
            if callback:
                callback(f"Failed to stop recording: {str(e)}")
            return None
    
    def is_recording(self) -> bool:
        """Check if currently recording"""
        return self.recording
    
    def cleanup(self):
        """Clean up resources"""
        if self.recording:
            self.stop_recording()
        
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.unlink(self.temp_file_path)
            except:
                pass
    
    @staticmethod
    def get_audio_devices():
        """Get available audio input devices"""
        if not AUDIO_AVAILABLE:
            return []
            
        try:
            devices = sd.query_devices()
            input_devices = []
            
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    input_devices.append({
                        'id': i,
                        'name': device['name'],
                        'channels': device['max_input_channels']
                    })
            
            return input_devices
            
        except Exception as e:
            print(f"Error getting audio devices: {e}")
            return []
    
    @staticmethod
    def test_microphone() -> bool:
        """Test if microphone is available"""
        if not AUDIO_AVAILABLE:
            return False
            
        try:
            # Try to query default input device
            default_device = sd.query_devices(kind='input')
            return default_device is not None
        except:
            return False
