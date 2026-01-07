# Prayer Time Reminder and Auto Lock System

A minimal, focused Windows application that helps Muslim users observe daily prayers by automatically fetching prayer times, showing notifications, and temporarily locking the computer.

## Features

- Fetches accurate prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha) using AlAdhan API
- Runs quietly in the background
- Shows desktop notifications at prayer times
- Optionally plays Adhan (audio feature coming soon)
- Temporarily locks Windows computer for configurable duration (10-15 min)
- Beautiful lock screen with countdown timer
- Emergency exit with long-press ESC key
- Safe and ethical design (no permanent lock, easy exit)
- Simple configuration via GUI
- Local JSON settings storage

## Requirements

- Windows OS
- Python 3.6+
- Internet connection for fetching prayer times

## Installation

1. Clone or download this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python prayer_app.py
```

1. Click "Settings" to configure your city/country and lock duration
2. Click "Start" to begin monitoring prayer times
3. The app will automatically lock your computer at prayer times
4. To exit the lock screen in emergency, press and hold ESC key
5. To exit the app, click "Exit" and answer the confirmation questions

## Safety Features

- Maximum lock duration is configurable (recommended 10-15 minutes)
- Emergency exit available with ESC key
- No tracking or data collection
- Easy uninstall (just delete the folder)
- Questions required for exit to encourage prayer commitment

## Architecture

- `prayer_app.py` - Main application with GUI, scheduling, and lock functionality
- Settings stored in `prayer_settings.json`
- Uses Windows API via ctypes for locking
- AlAdhan API for prayer times
- Tkinter for GUI and lock screen
- Plyer for notifications

## Security & Ethics

- No permanent lock - always has unlock mechanism
- Emergency exit available
- No data tracking
- Transparent code
- User-controlled settings
- Confirmation questions for exit to promote prayer commitment