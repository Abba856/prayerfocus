import ctypes
import time
import threading
from datetime import datetime, timedelta
import os

class SystemLockManager:
    """
    Manages Windows system locking and unlocking functionality
    """
    
    def __init__(self):
        self.is_locked = False
        self.lock_thread = None
        self.lock_duration = 10 * 60  # Default 10 minutes in seconds
        self._emergency_unlock_flag = False
        self.lock_callback = None
    
    def set_lock_duration(self, minutes):
        """Set the lock duration in minutes"""
        self.lock_duration = minutes * 60  # Convert to seconds
    
    def set_lock_callback(self, callback):
        """Set callback function to be called when lock state changes"""
        self.lock_callback = callback
    
    def lock_workstation(self):
        """Lock the Windows workstation using the Windows API"""
        try:
            # Use the Windows API to lock the workstation
            ctypes.windll.user32.LockWorkStation()
            return True
        except Exception as e:
            print(f"Error locking workstation: {e}")
            return False
    
    def lock_system_for_duration(self, duration_minutes=None):
        """
        Lock the system for a specified duration
        """
        if self.is_locked:
            print("System is already locked")
            return False
        
        if duration_minutes:
            self.set_lock_duration(duration_minutes)
        
        # Lock the workstation immediately
        if not self.lock_workstation():
            return False
        
        self.is_locked = True
        if self.lock_callback:
            self.lock_callback(True)  # Notify that system is locked
        
        # Create a thread to unlock after the specified duration
        self.lock_thread = threading.Thread(
            target=self._unlock_after_duration,
            args=(self.lock_duration,)
        )
        self.lock_thread.daemon = True
        self.lock_thread.start()
        
        return True
    
    def _unlock_after_duration(self, duration_seconds):
        """
        Internal method to unlock the system after a specified duration
        """
        time.sleep(duration_seconds)

        if not self._emergency_unlock_flag:
            self.is_locked = False
            if self.lock_callback:
                self.lock_callback(False)  # Notify that system is unlocked
        else:
            self._emergency_unlock_flag = False  # Reset emergency unlock flag
    
    def emergency_unlock(self):
        """
        Emergency unlock functionality that can be triggered by user
        """
        if self.is_locked:
            self._emergency_unlock_flag = True
            self.is_locked = False
            if self.lock_callback:
                self.lock_callback(False)  # Notify that system is unlocked
            return True
        return False
    
    def is_system_locked(self):
        """
        Check if the system is currently locked
        Note: This is a simplified check - actual Windows lock status detection
        is more complex and may require additional techniques
        """
        return self.is_locked
    
    def set_emergency_hotkey(self, hotkey_func):
        """
        Set a function to be called when an emergency hotkey is pressed
        This would typically be handled by a global hotkey manager
        """
        # In a real implementation, this would register a global hotkey
        # For now, we'll just store the function
        self.emergency_hotkey_func = hotkey_func


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    # Check if running on Windows
    if sys.platform != 'win32':
        print("This module is designed for Windows systems only")
        sys.exit(1)
    
    def lock_status_callback(is_locked):
        status = "LOCKED" if is_locked else "UNLOCKED"
        print(f"System is now {status}")
    
    lock_manager = SystemLockManager()
    lock_manager.set_lock_callback(lock_status_callback)
    
    print("Testing system lock for 30 seconds...")
    lock_manager.lock_system_for_duration(0.5)  # 30 seconds for testing
    
    # Wait for the lock to take effect
    time.sleep(1)
    
    print(f"Is system locked? {lock_manager.is_system_locked()}")
    
    # Wait for auto unlock
    time.sleep(35)  # Wait longer than the lock duration
    
    print(f"Is system locked after duration? {lock_manager.is_system_locked()}")