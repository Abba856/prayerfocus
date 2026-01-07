import threading
import time
from datetime import datetime
import os
import requests
import tempfile

# Try to import pygame, but make it optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

class NotificationManager:
    """
    Manages notifications and Adhan audio playback
    """

    def __init__(self):
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
        self.current_sound = None
        self.is_playing = False
        self.volume = 0.7  # Default volume (0.0 to 1.0)
        self.adhan_files = {}
        self.notification_callback = None
    
    def set_volume(self, volume):
        """Set the volume for audio playback (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0.0 and 1.0

    def set_notification_callback(self, callback):
        """Set callback function to be called when notifications are shown"""
        self.notification_callback = callback

    def play_adhan(self, prayer_name, adhan_url=None):
        """
        Play Adhan for the specified prayer
        """
        if not PYGAME_AVAILABLE:
            print("Pygame not available, cannot play Adhan audio")
            # Still show notification even if audio is not available
            self.show_notification(f"Time for {prayer_name} Prayer", f"It's time to pray {prayer_name}")
            return False

        try:
            if self.is_playing and pygame:
                pygame.mixer.music.stop()

            # If no URL provided, use a default Adhan
            if not adhan_url:
                adhan_url = self._get_default_adhan_url(prayer_name)

            # Download the Adhan file if it's a URL
            if adhan_url.startswith(('http://', 'https://')):
                audio_file = self._download_audio(adhan_url)
            else:
                audio_file = adhan_url  # Assume it's a local file path

            if audio_file and pygame:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                self.is_playing = True

                # Notify about the prayer
                self.show_notification(f"Time for {prayer_name} Prayer", f"It's time to pray {prayer_name}")

                # Clean up downloaded file if it was temporary
                if adhan_url.startswith(('http://', 'https://')):
                    threading.Timer(10, lambda: self._cleanup_temp_file(audio_file)).start()

                return True
        except Exception as e:
            print(f"Error playing Adhan: {e}")
            return False
    
    def _get_default_adhan_url(self, prayer_name):
        """
        Get a default Adhan URL based on prayer name
        In a real implementation, this would point to actual Adhan audio files
        """
        # Using a placeholder - in real implementation, use actual Adhan URLs
        adhan_urls = {
            'fajr': 'https://example.com/adhan_fajr.mp3',
            'dhuhr': 'https://example.com/adhan_dhuhr.mp3',
            'asr': 'https://example.com/adhan_asr.mp3',
            'maghrib': 'https://example.com/adhan_maghrib.mp3',
            'isha': 'https://example.com/adhan_isha.mp3'
        }
        return adhan_urls.get(prayer_name.lower(), 'https://example.com/adhan_default.mp3')
    
    def _download_audio(self, url):
        """
        Download audio file from URL to a temporary location
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_file.write(response.content)
                temp_file.close()
                return temp_file.name
        except Exception as e:
            print(f"Error downloading audio: {e}")
        return None
    
    def _cleanup_temp_file(self, file_path):
        """
        Clean up temporary audio file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temp file: {e}")
    
    def stop_adhan(self):
        """Stop currently playing Adhan"""
        if self.is_playing and PYGAME_AVAILABLE and pygame:
            pygame.mixer.music.stop()
            self.is_playing = False
    
    def show_notification(self, title, message):
        """
        Show a notification to the user
        """
        try:
            # In a real implementation, this would use a notification system
            # For now, we'll just print the notification
            print(f"NOTIFICATION: {title}")
            print(f"Message: {message}")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Call the notification callback if set
            if self.notification_callback:
                self.notification_callback(title, message)
                
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def play_reminder_sound(self, sound_type="beep"):
        """
        Play a reminder sound (non-Adhan)
        """
        if not PYGAME_AVAILABLE:
            print(f"Pygame not available, simulating {sound_type} sound")
            return False

        try:
            if self.is_playing and pygame:
                pygame.mixer.music.stop()

            # For now, we'll simulate a beep sound
            # In a real implementation, this would play an actual sound file
            print(f"Playing {sound_type} sound")

            # For actual implementation, you could generate a simple beep:
            # frequency = 440  # Hz
            # duration = 1000  # ms
            # pygame.mixer.Sound.play(pygame.mixer.Sound(buffer=self._generate_tone(frequency, duration)))

        except Exception as e:
            print(f"Error playing reminder sound: {e}")
            return False
    
    def _generate_tone(self, frequency, duration, sample_rate=22050):
        """
        Generate a simple tone for reminder sounds
        """
        import numpy as np
        frames = int(duration)
        arr = np.zeros(frames)
        
        for i in range(frames):
            arr[i] = np.sin(2 * np.pi * frequency * i / sample_rate)
        
        # Convert to 16-bit integers
        arr = (arr * 32767).astype(np.int16)
        stereo_arr = np.zeros((frames, 2), dtype=np.int16)
        stereo_arr[:, 0] = arr
        stereo_arr[:, 1] = arr
        
        return stereo_arr.tobytes()
    
    def cleanup(self):
        """
        Clean up resources
        """
        self.stop_adhan()
        if PYGAME_AVAILABLE and pygame:
            pygame.mixer.quit()


# Example usage and testing
if __name__ == "__main__":
    import time
    
    def notification_callback(title, message):
        print(f"Callback received: {title} - {message}")
    
    notifier = NotificationManager()
    notifier.set_notification_callback(notification_callback)
    notifier.set_volume(0.5)
    
    print("Testing notification...")
    notifier.show_notification("Test Title", "This is a test notification")
    
    print("Testing Adhan playback (simulated)...")
    # This will show a notification but won't play actual audio in this test
    notifier.play_adhan("Fajr")
    
    time.sleep(2)
    
    print("Stopping Adhan...")
    notifier.stop_adhan()
    
    print("Playing reminder sound...")
    notifier.play_reminder_sound()
    
    print("Cleanup...")
    notifier.cleanup()