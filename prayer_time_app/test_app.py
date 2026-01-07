"""
Comprehensive test suite for Prayer Time Reminder and Auto Computer Lock System
"""

import unittest
import sys
import os
import time
from datetime import datetime, timedelta

# Add the current directory to the path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prayer_calculator import PrayerCalculator
from system_lock import SystemLockManager
from notification_manager import NotificationManager
from config_manager import ConfigManager
from service import PrayerTimeService
from security_manager import SecurityManager


class TestPrayerCalculator(unittest.TestCase):
    """Test prayer time calculation functionality"""
    
    def setUp(self):
        self.calculator = PrayerCalculator(
            method='MWL',
            coordinates=(40.7128, -74.0060),  # New York
            timezone=-5
        )
    
    def test_init(self):
        """Test initialization of prayer calculator"""
        self.assertEqual(self.calculator.method, 'MWL')
        self.assertEqual(self.calculator.lat, 40.7128)
        self.assertEqual(self.calculator.lng, -74.0060)
    
    def test_get_times_offline(self):
        """Test offline prayer time calculation"""
        times = self.calculator.get_times_offline()
        self.assertIsInstance(times, dict)
        self.assertIn('fajr', times)
        self.assertIn('dhuhr', times)
        self.assertIn('asr', times)
        self.assertIn('maghrib', times)
        self.assertIn('isha', times)
    
    def test_set_location(self):
        """Test setting location"""
        self.calculator.set_location((35.6895, 139.6917), 9)  # Tokyo
        self.assertEqual(self.calculator.lat, 35.6895)
        self.assertEqual(self.calculator.lng, 139.6917)
        self.assertEqual(self.calculator.timezone, 9)


class TestSystemLockManager(unittest.TestCase):
    """Test system lock functionality"""
    
    def setUp(self):
        self.lock_manager = SystemLockManager()
    
    @unittest.skipIf(sys.platform != 'win32', "Windows-specific functionality")
    def test_lock_workstation(self):
        """Test workstation locking (manual verification needed)"""
        # This test would actually lock the workstation, so we'll just test the method exists
        self.assertTrue(hasattr(self.lock_manager, 'lock_workstation'))
        self.assertTrue(callable(getattr(self.lock_manager, 'lock_workstation')))
    
    def test_set_lock_duration(self):
        """Test setting lock duration"""
        self.lock_manager.set_lock_duration(15)
        self.assertEqual(self.lock_manager.lock_duration, 15 * 60)  # Convert to seconds
    
    def test_is_system_locked(self):
        """Test checking if system is locked"""
        # Initially should be unlocked
        self.assertFalse(self.lock_manager.is_system_locked())


class TestNotificationManager(unittest.TestCase):
    """Test notification functionality"""
    
    def setUp(self):
        self.notifier = NotificationManager()
    
    def test_set_volume(self):
        """Test setting volume"""
        self.notifier.set_volume(0.5)
        self.assertEqual(self.notifier.volume, 0.5)
        
        # Test clamping
        self.notifier.set_volume(1.5)
        self.assertEqual(self.notifier.volume, 1.0)
        
        self.notifier.set_volume(-0.5)
        self.assertEqual(self.notifier.volume, 0.0)
    
    def test_show_notification(self):
        """Test showing notification"""
        # Just test that the method exists and doesn't crash
        try:
            self.notifier.show_notification("Test", "This is a test notification")
            success = True
        except Exception:
            success = False
        self.assertTrue(success)


class TestConfigManager(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        self.config_manager = ConfigManager("test_config.json")
    
    def tearDown(self):
        # Clean up test config file
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
    
    def test_get_set_location(self):
        """Test getting and setting location"""
        self.config_manager.set_location(40.7128, -74.0060, "New York", "USA")
        location = self.config_manager.get_location()
        self.assertEqual(location['latitude'], 40.7128)
        self.assertEqual(location['longitude'], -74.0060)
        self.assertEqual(location['city'], "New York")
        self.assertEqual(location['country'], "USA")
    
    def test_get_set_calculation_method(self):
        """Test getting and setting calculation method"""
        self.config_manager.set_calculation_method("ISNA")
        method = self.config_manager.get_calculation_method()
        self.assertEqual(method, "ISNA")
    
    def test_lock_settings(self):
        """Test lock settings"""
        self.config_manager.set_lock_setting("duration_minutes", 15)
        settings = self.config_manager.get_lock_settings()
        self.assertEqual(settings["duration_minutes"], 15)
    
    def test_save_load_config(self):
        """Test saving and loading configuration"""
        self.config_manager.set_location(34.0522, -118.2437, "Los Angeles", "USA")
        self.config_manager.set_calculation_method("Egypt")
        self.config_manager.save_config()
        
        # Create new instance to test loading
        new_config = ConfigManager("test_config.json")
        self.assertEqual(new_config.get_location()['latitude'], 34.0522)
        self.assertEqual(new_config.get_calculation_method(), "Egypt")


class TestSecurityManager(unittest.TestCase):
    """Test security functionality"""
    
    def setUp(self):
        self.config_manager = ConfigManager("test_security_config.json")
        self.security_manager = SecurityManager(self.config_manager)
    
    def tearDown(self):
        # Clean up test config file
        if os.path.exists("test_security_config.json"):
            os.remove("test_security_config.json")
        # Clean up logs directory if it exists
        if os.path.exists("logs"):
            import shutil
            shutil.rmtree("logs")
    
    def test_validate_lock_duration(self):
        """Test lock duration validation"""
        # Test normal duration
        self.assertEqual(self.security_manager.validate_lock_duration(10), 10)
        
        # Test too short duration
        self.assertEqual(self.security_manager.validate_lock_duration(1), 2)  # Minimum is 2 minutes
        
        # Test too long duration
        self.assertEqual(self.security_manager.validate_lock_duration(45), 30)  # Maximum is 30 minutes
    
    def test_check_user_consent(self):
        """Test user consent checking"""
        # By default, auto-lock should be enabled
        self.assertTrue(self.security_manager.check_user_consent("auto_lock"))
        
        # By default, play_adhan should be enabled
        self.assertTrue(self.security_manager.check_user_consent("play_adhan"))
    
    def test_verify_emergency_access(self):
        """Test emergency access verification"""
        self.assertTrue(self.security_manager.verify_emergency_access())


class TestPrayerTimeService(unittest.TestCase):
    """Test the main service"""
    
    def setUp(self):
        self.service = PrayerTimeService()
    
    def test_init(self):
        """Test service initialization"""
        self.assertIsNotNone(self.service.config_manager)
        self.assertIsNotNone(self.service.prayer_calculator)
        self.assertIsNotNone(self.service.system_lock_manager)
        self.assertIsNotNone(self.service.notification_manager)
        self.assertIsNotNone(self.service.security_manager)
        self.assertFalse(self.service.is_running)
    
    def test_get_today_prayer_times(self):
        """Test getting today's prayer times"""
        times = self.service.get_today_prayer_times()
        self.assertIsInstance(times, dict)
        self.assertIn('fajr', times)
        self.assertIn('dhuhr', times)
        self.assertIn('asr', times)
        self.assertIn('maghrib', times)
        self.assertIn('isha', times)
    
    def test_update_location(self):
        """Test updating location"""
        # Update location to London
        self.service.config_manager.set_location(51.5074, -0.1278, "London", "UK")
        self.service.update_location()
        # Just verify it doesn't crash


def run_comprehensive_test():
    """Run a comprehensive end-to-end test"""
    print("=" * 60)
    print("COMPREHENSIVE APPLICATION TEST")
    print("=" * 60)
    
    # Test 1: Prayer calculation
    print("\n1. Testing Prayer Calculation...")
    calc = PrayerCalculator(coordinates=(40.7128, -74.0060), method='MWL')
    times = calc.get_times_offline()
    print(f"   Prayer times calculated: {list(times.keys())}")
    print(f"   Fajr time: {times.get('fajr', 'Not found')}")
    
    # Test 2: Configuration
    print("\n2. Testing Configuration Management...")
    config = ConfigManager()
    config.set_location(35.6895, 139.6917, "Tokyo", "Japan")
    config.set_calculation_method("ISNA")
    config.save_config()
    print(f"   Location set to: {config.get_location()['city']}")
    print(f"   Calculation method: {config.get_calculation_method()}")
    
    # Test 3: Security
    print("\n3. Testing Security Features...")
    security = SecurityManager(config)
    print(f"   Security status: {security.get_security_status()}")
    print(f"   Validated 25-minute duration: {security.validate_lock_duration(25)} minutes")
    print(f"   Validated 45-minute duration: {security.validate_lock_duration(45)} minutes (max)")
    
    # Test 4: Notifications
    print("\n4. Testing Notification System...")
    notifier = NotificationManager()
    notifier.set_volume(0.6)
    notifier.show_notification("Test", "This is a test notification")
    print(f"   Notification volume set to: {notifier.volume}")
    
    # Test 5: Service
    print("\n5. Testing Main Service...")
    service = PrayerTimeService()
    service.config_manager.set_location(48.8566, 2.3522, "Paris", "France")
    service.update_location()
    times = service.get_today_prayer_times()
    print(f"   Paris prayer times retrieved: {len(times)} prayers")
    
    # Test 6: Emergency unlock
    print("\n6. Testing Emergency Unlock...")
    unlock_result = service.emergency_unlock()
    print(f"   Emergency unlock attempted: {unlock_result}")
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE TEST COMPLETED")
    print("=" * 60)


if __name__ == '__main__':
    # Run the comprehensive test
    run_comprehensive_test()
    
    print("\nRunning unit tests...")
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)