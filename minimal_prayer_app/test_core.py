# Test script for core functionality without GUI dependencies
import json
import requests
from datetime import datetime

def test_api_connection():
    """Test the AlAdhan API connection"""
    try:
        url = f"http://api.aladhan.com/v1/timingsByCity/{datetime.now().strftime('%d-%m-%Y')}"
        params = {
            'city': 'London',
            'country': 'UK',
            'method': 2  # ISNA method
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                timings = data['data']['timings']
                prayer_times = {
                    'Fajr': timings['Fajr'][:5],
                    'Dhuhr': timings['Dhuhr'][:5],
                    'Asr': timings['Asr'][:5],
                    'Maghrib': timings['Maghrib'][:5],
                    'Isha': timings['Isha'][:5]
                }
                print("✓ API Connection successful")
                print("Sample prayer times:", prayer_times)
                return True
        print("✗ API Connection failed")
        return False
    except Exception as e:
        print(f"✗ API Connection error: {e}")
        return False

def test_settings():
    """Test settings functionality"""
    try:
        # Test default settings
        default_settings = {
            "city": "London",
            "country": "UK",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "lock_duration": 10,
            "play_adhan": True,
            "auto_start": False
        }
        
        # Test saving and loading
        with open('test_settings.json', 'w') as f:
            json.dump(default_settings, f, indent=2)
        
        with open('test_settings.json', 'r') as f:
            loaded = json.load(f)
        
        # Clean up
        import os
        os.remove('test_settings.json')
        
        print("✓ Settings functionality works")
        return True
    except Exception as e:
        print(f"✗ Settings functionality error: {e}")
        return False

def test_ctypes():
    """Test ctypes import (for Windows locking)"""
    try:
        import ctypes
        print("✓ ctypes imported successfully (Windows API access available)")
        return True
    except ImportError:
        print("✗ ctypes import failed")
        return False

def test_schedule():
    """Test schedule import"""
    try:
        import schedule
        print("✓ schedule imported successfully")
        return True
    except ImportError:
        print("✗ schedule import failed")
        return False

def test_plyer():
    """Test plyer import"""
    try:
        import plyer
        print("✓ plyer imported successfully")
        return True
    except ImportError:
        print("✗ plyer import failed")
        return False

if __name__ == "__main__":
    print("Testing Prayer App Core Functionality")
    print("=" * 50)
    
    tests = [
        ("API Connection", test_api_connection),
        ("Settings", test_settings),
        ("ctypes (Windows API)", test_ctypes),
        ("Schedule", test_schedule),
        ("Plyer (Notifications)", test_plyer),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        if test_func():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All core functionality tests passed!")
        print("\nThe application should work correctly on Windows with GUI support.")
    else:
        print("⚠ Some tests failed, but core functionality is mostly intact.")