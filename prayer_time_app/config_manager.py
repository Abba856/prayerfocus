import json
import os
from datetime import datetime

class ConfigManager:
    """
    Manages application configuration and user preferences
    """
    
    def __init__(self, config_file="prayer_app_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default"""
        default_config = {
            "location": {
                "latitude": 0.0,
                "longitude": 0.0,
                "city": "",
                "country": ""
            },
            "calculation_method": "MWL",  # Default calculation method
            "time_format": "24h",  # "12h" or "24h"
            "lock_settings": {
                "enabled": True,
                "duration_minutes": 10,
                "auto_lock_prayers": ["fajr", "dhuhr", "asr", "maghrib", "isha"],
                "allow_emergency_unlock": True
            },
            "notification_settings": {
                "volume": 0.7,
                "show_visual_notifications": True,
                "play_adhan": True,
                "adhan_volume": 0.8
            },
            "app_settings": {
                "start_with_windows": True,
                "minimize_to_tray": True,
                "check_for_updates": True
            },
            "last_updated": datetime.now().isoformat()
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return self._merge_configs(default_config, loaded_config)
            except Exception as e:
                print(f"Error loading config, using defaults: {e}")
        
        # Save default config to file
        self.config = default_config
        self.save_config()
        return default_config
    
    def _merge_configs(self, default, loaded):
        """Merge loaded config with defaults to ensure all keys exist"""
        for key, value in default.items():
            if key not in loaded:
                loaded[key] = value
            elif isinstance(value, dict) and isinstance(loaded[key], dict):
                loaded[key] = self._merge_configs(value, loaded[key])
        return loaded
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            self.config["last_updated"] = datetime.now().isoformat()
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_location(self):
        """Get location settings"""
        return self.config["location"]
    
    def set_location(self, latitude, longitude, city="", country=""):
        """Set location settings"""
        self.config["location"] = {
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "country": country
        }
    
    def get_calculation_method(self):
        """Get the prayer time calculation method"""
        return self.config["calculation_method"]
    
    def set_calculation_method(self, method):
        """Set the prayer time calculation method"""
        self.config["calculation_method"] = method
    
    def get_lock_settings(self):
        """Get lock settings"""
        return self.config["lock_settings"]
    
    def set_lock_setting(self, key, value):
        """Set a specific lock setting"""
        self.config["lock_settings"][key] = value
    
    def get_notification_settings(self):
        """Get notification settings"""
        return self.config["notification_settings"]
    
    def set_notification_setting(self, key, value):
        """Set a specific notification setting"""
        self.config["notification_settings"][key] = value
    
    def get_app_settings(self):
        """Get application settings"""
        return self.config["app_settings"]
    
    def set_app_setting(self, key, value):
        """Set a specific app setting"""
        self.config["app_settings"][key] = value
    
    def get_time_format(self):
        """Get time format setting"""
        return self.config["time_format"]
    
    def set_time_format(self, time_format):
        """Set time format setting"""
        self.config["time_format"] = time_format
    
    def update_last_used(self):
        """Update the last used timestamp"""
        self.config["last_updated"] = datetime.now().isoformat()
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        default_config = {
            "location": {
                "latitude": 0.0,
                "longitude": 0.0,
                "city": "",
                "country": ""
            },
            "calculation_method": "MWL",
            "time_format": "24h",
            "lock_settings": {
                "enabled": True,
                "duration_minutes": 10,
                "auto_lock_prayers": ["fajr", "dhuhr", "asr", "maghrib", "isha"],
                "allow_emergency_unlock": True
            },
            "notification_settings": {
                "volume": 0.7,
                "show_visual_notifications": True,
                "play_adhan": True,
                "adhan_volume": 0.8
            },
            "app_settings": {
                "start_with_windows": True,
                "minimize_to_tray": True,
                "check_for_updates": True
            },
            "last_updated": datetime.now().isoformat()
        }
        self.config = default_config
        return self.save_config()


# Example usage and testing
if __name__ == "__main__":
    config_manager = ConfigManager("test_config.json")
    
    print("Initial config:")
    print(json.dumps(config_manager.config, indent=2))
    
    print("\nUpdating location...")
    config_manager.set_location(40.7128, -74.0060, "New York", "USA")
    print(f"New location: {config_manager.get_location()}")
    
    print("\nUpdating calculation method...")
    config_manager.set_calculation_method("ISNA")
    print(f"Calculation method: {config_manager.get_calculation_method()}")
    
    print("\nUpdating lock settings...")
    config_manager.set_lock_setting("duration_minutes", 15)
    print(f"Lock duration: {config_manager.get_lock_settings()['duration_minutes']} minutes")
    
    print("\nSaving config...")
    config_manager.save_config()
    
    print("\nTesting config reload...")
    new_config_manager = ConfigManager("test_config.json")
    print(f"Reloaded location: {new_config_manager.get_location()}")
    
    # Clean up test file
    if os.path.exists("test_config.json"):
        os.remove("test_config.json")