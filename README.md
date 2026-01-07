# Prayer Time Reminder and Auto Computer Lock System - Project Summary

## Overview

This project contains two implementations of a Windows desktop application designed to help Muslim users observe daily prayers by automatically fetching prayer times, showing notifications, and temporarily locking the computer during prayer times.

## Folder Structure

### 1. `prayer_time_app` - Full-Featured Implementation
A comprehensive, enterprise-level implementation with advanced features:

**Features:**
- Complete prayer time calculation with online API and offline fallback
- Advanced system lock management with Windows API integration
- Full notification system with Adhan audio playback
- Configuration management with JSON storage
- Security and ethics management module
- Full GUI with system tray integration
- Windows startup integration
- Comprehensive logging and security features
- Multiple calculation methods support
- Emergency unlock functionality

**Architecture:**
- Modular design with separate components
- Professional software engineering practices
- Security-focused implementation
- Comprehensive error handling

### 2. `minimal_prayer_app` - Minimal Implementation (Recommended)
A focused, lightweight implementation meeting specific requirements:

**Features:**
- Fetches prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha) from AlAdhan API
- Runs quietly in background with scheduler
- Shows desktop notifications at prayer times
- Temporarily locks Windows computer for 10-15 minutes using ctypes
- Beautiful lock screen with countdown timer
- Emergency exit with long-press ESC key
- Exit confirmation with meaningful questions:
  - "If Allah is the One who gives you life, time, and every blessing you enjoy, what is holding you back from meeting Him for a few minutes in Ṣalāh?"
  - "When you stand before Allah on the Day of Judgment and He asks about your prayers, what answer do you hope to give?"
  - "If this prayer was the last chance Allah gave you to return to Him, would you still choose to ignore it?"
- Local JSON settings storage
- Simple Tkinter GUI for configuration
- Safe and ethical design (no permanent lock, easy exit)
- Windows executable ready for distribution

**Distribution:**
- Contains complete Windows distribution package in `windows_dist/` folder
- Includes `PrayerTimeReminder.exe` (ready-to-run executable)
- Setup script and documentation included

## Key Differences

| Aspect | Full Implementation | Minimal Implementation |
|--------|-------------------|----------------------|
| Complexity | Advanced, feature-rich | Simple, focused |
| Size | Larger codebase | Minimal, lightweight |
| Features | Comprehensive | Essential features only |
| Target | Enterprise/advanced users | Personal use |
| Distribution | Source code | Ready-to-run executable |

## Usage

### For End Users (Recommended):
Use the **`minimal_prayer_app`** folder, specifically the `windows_dist` subfolder which contains:
- `PrayerTimeReminder.exe` - Ready-to-run Windows application
- Installation instructions and documentation
- Setup script for easy installation

### For Developers:
Both implementations provide complete source code for customization and further development.

## Technologies Used

- Python 3.x
- Windows API (ctypes)
- AlAdhan API for prayer times
- Tkinter for GUI
- Plyer for notifications
- Schedule library for timing
- JSON for settings storage

## Security & Ethics

Both implementations prioritize:
- User safety with emergency exit options
- No permanent locks
- Local-only data storage
- Meaningful exit confirmations
- Transparent codebase

## License
This project is designed for personal use with no tracking or data collection.
