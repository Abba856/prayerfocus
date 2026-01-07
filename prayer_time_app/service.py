import threading
import time
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to the path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prayer_calculator import PrayerCalculator
from system_lock import SystemLockManager
from notification_manager import NotificationManager
from config_manager import ConfigManager
from security_manager import SecurityManager

class PrayerTimeService:
    """
    Main service that monitors prayer times and manages notifications/locking
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.security_manager = SecurityManager(self.config_manager)
        self.prayer_calculator = None
        self.system_lock_manager = SystemLockManager()
        self.notification_manager = NotificationManager()

        # Initialize calculator with current config
        location = self.config_manager.get_location()
        coords = (location['latitude'], location['longitude'])
        self.prayer_calculator = PrayerCalculator(
            method=self.config_manager.get_calculation_method(),
            coordinates=coords
        )

        # Set up callbacks
        self.system_lock_manager.set_lock_callback(self._on_lock_change)
        self.notification_manager.set_notification_callback(self._on_notification)

        # Service control
        self.is_running = False
        self.service_thread = None
        self.today_prayer_times = {}
        self.next_prayer_check = None

        # Update volume settings
        notif_settings = self.config_manager.get_notification_settings()
        self.notification_manager.set_volume(notif_settings.get('adhan_volume', 0.7))

        # Enforce ethical guidelines
        self.security_manager.enforce_ethical_guidelines()
    
    def _on_lock_change(self, is_locked):
        """Callback when system lock state changes"""
        status = "LOCKED" if is_locked else "UNLOCKED"
        print(f"System {status}")
        # In a real implementation, this might update the UI or log the event
    
    def _on_notification(self, title, message):
        """Callback when notification is shown"""
        print(f"Notification: {title} - {message}")
        # In a real implementation, this might update the UI
    
    def update_location(self):
        """Update location from config"""
        location = self.config_manager.get_location()
        coords = (location['latitude'], location['longitude'])
        timezone = self._get_timezone_from_location(coords)  # Simplified
        self.prayer_calculator.set_location(coords, timezone)
    
    def _get_timezone_from_location(self, coordinates):
        """Get timezone from coordinates (simplified implementation)"""
        # In a real implementation, this would use a timezone API or library
        # For now, we'll return a simple approximation based on longitude
        longitude = coordinates[1]
        # Each 15 degrees of longitude is approximately 1 hour difference
        return round(longitude / 15.0)
    
    def get_today_prayer_times(self):
        """Get today's prayer times"""
        return self.prayer_calculator.get_times_online()
    
    def _check_prayer_times(self):
        """Check if it's time for prayer and take appropriate action"""
        current_time = datetime.now().time()
        current_time_str = current_time.strftime("%H:%M")
        
        # Get today's prayer times if not already loaded or if it's a new day
        if not self.today_prayer_times or self._is_new_day():
            self.today_prayer_times = self.get_today_prayer_times()
            self._schedule_prayer_notifications()
        
        # Check each prayer time
        for prayer_name, prayer_time in self.today_prayer_times.items():
            if prayer_time and self._is_time_for_prayer(prayer_name, prayer_time, current_time_str):
                self._handle_prayer_time(prayer_name)
    
    def _is_new_day(self):
        """Check if it's a new day and we need to refresh prayer times"""
        if self.next_prayer_check:
            return datetime.now().date() > self.next_prayer_check.date()
        return True
    
    def _is_time_for_prayer(self, prayer_name, prayer_time, current_time_str):
        """Check if it's time for a specific prayer"""
        # Simple check: if the prayer time matches current time (within a minute)
        # In a real implementation, you might want to allow a small window
        return prayer_time == current_time_str
    
    def _handle_prayer_time(self, prayer_name):
        """Handle when it's time for a prayer"""
        print(f"It's time for {prayer_name} prayer!")

        # Check user consent for actions
        if not self.security_manager.check_user_consent("play_adhan"):
            print("Adhan playing disabled by user preference")
            return

        # Check if this prayer should trigger auto-lock
        lock_settings = self.config_manager.get_lock_settings()
        auto_lock_prayers = lock_settings.get("auto_lock_prayers", [])

        # Play Adhan
        if lock_settings.get("play_adhan", True):
            self.notification_manager.play_adhan(prayer_name)

        # Show notification
        self.notification_manager.show_notification(
            f"Time for {prayer_name.capitalize()} Prayer",
            f"It's now time for {prayer_name.capitalize()} prayer. Computer will lock in 30 seconds to help you focus on prayer."
        )

        # Auto-lock if enabled and this prayer is in the auto-lock list
        if (lock_settings.get("enabled", True) and
            prayer_name.lower() in [p.lower() for p in auto_lock_prayers]):

            # Validate lock duration for security
            lock_duration = lock_settings.get("duration_minutes", 10)
            validated_duration = self.security_manager.validate_lock_duration(lock_duration)

            # Log the locking action for security
            self.security_manager.log_security_event(
                "AUTO_LOCK_TRIGGERED",
                f"Locking system for {validated_duration} minutes at {prayer_name} time"
            )

            self.system_lock_manager.lock_system_for_duration(validated_duration)
    
    def _schedule_prayer_notifications(self):
        """Schedule notifications for all prayer times today"""
        # In a real implementation, you might use the schedule library
        # For now, we'll just store the times and check them manually
        pass
    
    def start_service(self):
        """Start the prayer time monitoring service"""
        if self.is_running:
            print("Service is already running")
            return
        
        self.is_running = True
        self.service_thread = threading.Thread(target=self._service_loop, daemon=True)
        self.service_thread.start()
        print("Prayer time service started")
    
    def stop_service(self):
        """Stop the prayer time monitoring service"""
        self.is_running = False
        if self.service_thread:
            self.service_thread.join(timeout=2)  # Wait up to 2 seconds for thread to finish
        print("Prayer time service stopped")
    
    def _service_loop(self):
        """Main service loop that runs in a separate thread"""
        while self.is_running:
            try:
                self._check_prayer_times()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Error in service loop: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def emergency_unlock(self):
        """Emergency unlock functionality"""
        if self.security_manager.verify_emergency_access():
            success = self.system_lock_manager.emergency_unlock()
            if success:
                self.security_manager.log_security_event(
                    "EMERGENCY_UNLOCK",
                    "System unlocked via emergency access"
                )
            return success
        else:
            print("Emergency unlock not permitted")
            return False
    
    def get_current_status(self):
        """Get current service status"""
        return {
            "is_running": self.is_running,
            "is_system_locked": self.system_lock_manager.is_system_locked(),
            "today_prayer_times": self.today_prayer_times,
            "next_check": self.next_prayer_check
        }


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    # Check if running on Windows
    if sys.platform != 'win32':
        print("This service is designed for Windows systems only")
        sys.exit(1)
    
    print("Starting Prayer Time Service for testing...")
    
    service = PrayerTimeService()
    
    # Update location to New York for testing
    service.config_manager.set_location(40.7128, -74.0060, "New York", "USA")
    service.update_location()
    
    # Print today's prayer times
    times = service.get_today_prayer_times()
    print("Today's prayer times:", times)
    
    # Start the service
    service.start_service()
    
    # Let it run for a short time for testing
    try:
        time.sleep(10)  # Run for 10 seconds for testing
    except KeyboardInterrupt:
        print("\nStopping service...")
    
    service.stop_service()
    print("Service stopped.")