# Prayer Time Reminder and Auto Lock System - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Prayer App Main Loop                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  API Handler    │  │  Scheduler      │  │  Lock       │ │
│  │                 │  │                 │  │  Manager    │ │
│  │ • AlAdhan API   │  │ • Prayer times  │  │             │ │
│  │ • Fetch times   │  │ • Schedule jobs │  │ • ctypes    │ │
│  │ • Parse JSON    │  │ • Run daily     │  │ • Fullscreen│ │
│  └─────────────────┘  └─────────────────┘  │ • ESC exit  │ │
│                                            └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────┐
                   │  Settings       │
                   │  Manager        │
                   │ • JSON storage  │
                   │ • GUI config    │
                   └─────────────────┘
```

## Component Details

### 1. API Handler (`get_prayer_times`)
- Fetches prayer times from AlAdhan API
- Parses JSON response
- Returns structured prayer times

### 2. Scheduler (`schedule` library)
- Schedules prayer time events
- Runs continuously in background thread
- Triggers prayer handlers at specified times

### 3. Lock Manager (`ctypes` + Tkinter)
- Uses Windows API to lock computer
- Shows beautiful fullscreen lock screen
- Implements ESC emergency exit
- Manages countdown timer

### 4. Settings Manager
- Loads/stores settings in JSON file
- Manages user preferences
- Handles configuration via GUI

### 5. Notification System (`plyer`)
- Shows desktop notifications
- Cross-platform notification support

## Folder Structure
```
minimal_prayer_app/
├── prayer_app.py          # Main application
├── requirements.txt       # Dependencies
├── README.md            # Documentation
├── test_core.py         # Core functionality test
├── prayer_settings.json # User settings (created automatically)
└── __pycache__/         # Python cache (runtime)
```

## Key Features Implementation

### Prayer Time Fetching
- Uses AlAdhan API: `http://api.aladhan.com/v1/timingsByCity`
- Method 2 (ISNA) for calculation
- Returns Fajr, Dhuhr, Asr, Maghrib, Isha times

### Lock Mechanism
- `ctypes.windll.user32.LockWorkStation()` for Windows lock
- Beautiful Tkinter fullscreen overlay
- Configurable duration (10-15 min default)
- Emergency ESC key exit with confirmation

### Safety & Ethics
- No permanent lock (always has unlock mechanism)
- Emergency exit available
- Questions required for exit to promote prayer commitment
- No tracking or data collection
- Local-only settings storage

### User Experience
- Simple GUI with settings window
- Clear status indicators
- Desktop notifications
- Visual countdown timer
- Intuitive controls