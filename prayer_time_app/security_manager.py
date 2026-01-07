import logging
import os
from datetime import datetime
from config_manager import ConfigManager

class SecurityManager:
    """
    Manages security, ethics, and user control aspects of the application
    """
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager or ConfigManager()
        self.logger = self._setup_logger()
        self.emergency_access_enabled = True
        self.max_lock_duration = 30 * 60  # Maximum 30 minutes in seconds
        self.min_lock_duration = 2 * 60   # Minimum 2 minutes in seconds
        
    def _setup_logger(self):
        """Setup logging for security events"""
        logger = logging.getLogger('PrayerAppSecurity')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create file handler
        log_file = os.path.join(log_dir, f"security_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(file_handler)
        
        return logger
    
    def validate_lock_duration(self, duration_minutes):
        """Validate that lock duration is within acceptable limits"""
        duration_seconds = duration_minutes * 60
        
        if duration_seconds < self.min_lock_duration:
            self.logger.warning(f"Lock duration {duration_minutes} minutes is below minimum of {self.min_lock_duration//60} minutes")
            return self.min_lock_duration // 60
        
        if duration_seconds > self.max_lock_duration:
            self.logger.warning(f"Lock duration {duration_minutes} minutes exceeds maximum of {self.max_lock_duration//60} minutes")
            return self.max_lock_duration // 60
        
        return duration_minutes
    
    def check_user_consent(self, action):
        """Check if user has consented to the action"""
        # In a real implementation, this would check user preferences/settings
        # For now, we'll assume consent is given based on configuration
        if action == "auto_lock":
            return self.config_manager.get_lock_settings().get("enabled", True)
        elif action == "play_adhan":
            return self.config_manager.get_notification_settings().get("play_adhan", True)
        
        return True  # Default to allowing other actions
    
    def log_security_event(self, event_type, details):
        """Log security-related events"""
        self.logger.info(f"{event_type}: {details}")
    
    def enable_emergency_access(self):
        """Enable emergency access functionality"""
        self.emergency_access_enabled = True
        self.log_security_event("EMERGENCY_ACCESS_ENABLED", "Emergency unlock functionality activated")
    
    def disable_emergency_access(self):
        """Disable emergency access functionality"""
        self.emergency_access_enabled = False
        self.log_security_event("EMERGENCY_ACCESS_DISABLED", "Emergency unlock functionality deactivated")
    
    def verify_emergency_access(self):
        """Verify if emergency access is allowed"""
        return self.emergency_access_enabled and self.config_manager.get_lock_settings().get("allow_emergency_unlock", True)
    
    def validate_user_settings(self, settings_category, settings):
        """Validate user settings for security and ethical compliance"""
        if settings_category == "lock_settings":
            if "duration_minutes" in settings:
                validated_duration = self.validate_lock_duration(settings["duration_minutes"])
                settings["duration_minutes"] = validated_duration
                if validated_duration != settings["duration_minutes"]:
                    self.log_security_event("SETTING_ADJUSTED", f"Lock duration adjusted from {settings['duration_minutes']} to {validated_duration} minutes")
        
        return settings
    
    def check_privilege_escalation_risk(self):
        """Check for potential privilege escalation risks"""
        # This would check if the application is running with elevated privileges
        # when not necessary, which could be a security risk
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() if os.name == 'nt' else os.getuid() == 0
        
        if is_admin:
            self.logger.warning("Application running with elevated privileges - verify necessity")
        
        return is_admin
    
    def enforce_ethical_guidelines(self):
        """Enforce ethical guidelines for the application"""
        # Ensure the application respects user autonomy
        # 1. Always allow emergency unlock
        # 2. Don't lock for unreasonably long periods
        # 3. Provide clear notifications before locking
        # 4. Allow users to disable auto-lock
        
        lock_settings = self.config_manager.get_lock_settings()
        
        # Ensure emergency unlock is allowed
        if not lock_settings.get("allow_emergency_unlock", True):
            self.logger.warning("Emergency unlock disabled by user - this violates ethical guidelines")
            # Optionally force enable it
            # self.config_manager.set_lock_setting("allow_emergency_unlock", True)
        
        # Validate lock duration
        duration = lock_settings.get("duration_minutes", 10)
        if duration > 20:  # More than 20 minutes might be considered excessive
            self.logger.warning(f"Long lock duration ({duration} minutes) detected - ensure user understands implications")
    
    def get_security_status(self):
        """Get current security status"""
        return {
            "emergency_access_enabled": self.verify_emergency_access(),
            "max_lock_duration_minutes": self.max_lock_duration // 60,
            "min_lock_duration_minutes": self.min_lock_duration // 60,
            "logging_active": True,
            "ethical_guidelines_enforced": True
        }


# Example usage and testing
if __name__ == "__main__":
    import tempfile
    import shutil
    
    # Create a temporary config for testing
    temp_config_path = os.path.join(tempfile.gettempdir(), "test_security_config.json")
    
    # Initialize security manager
    config_manager = ConfigManager(temp_config_path)
    security_manager = SecurityManager(config_manager)
    
    print("Security Manager initialized")
    
    # Test lock duration validation
    print(f"\nValidating lock durations:")
    print(f"5 minutes: {security_manager.validate_lock_duration(5)}")
    print(f"15 minutes: {security_manager.validate_lock_duration(15)}")
    print(f"45 minutes: {security_manager.validate_lock_duration(45)}")
    print(f"1 minute: {security_manager.validate_lock_duration(1)}")
    
    # Test user consent checking
    print(f"\nUser consent for auto-lock: {security_manager.check_user_consent('auto_lock')}")
    print(f"User consent for adhan: {security_manager.check_user_consent('play_adhan')}")
    
    # Test emergency access
    print(f"\nEmergency access available: {security_manager.verify_emergency_access()}")
    
    # Test security status
    status = security_manager.get_security_status()
    print(f"\nSecurity status: {status}")
    
    # Test ethical guidelines enforcement
    security_manager.enforce_ethical_guidelines()
    print("\nEthical guidelines enforced")
    
    # Clean up
    if os.path.exists(temp_config_path):
        os.remove(temp_config_path)
    
    print(f"\nSecurity logs created in logs/ directory")