# Prayer Time Reminder and Auto Lock System - Windows Installation

## Distribution Package Contents

This package contains everything needed to run the Prayer Time Reminder application on Windows:

- `PrayerTimeReminder.exe` - Main application executable
- `README.txt` - Installation and usage instructions
- `requirements.txt` - Python dependencies (for reference)

## Installation Instructions

### Method 1: Direct Executable (Recommended)
1. Extract all files from this distribution package to a folder on your Windows computer
2. Run `PrayerTimeReminder.exe` directly
3. The application will create a `prayer_settings.json` file automatically

### Method 2: Create Desktop Shortcut
1. After extracting, right-click on `PrayerTimeReminder.exe`
2. Select "Create shortcut"
3. Move the shortcut to your desktop for easy access

## Usage Instructions

1. **First Run**: 
   - Launch `PrayerTimeReminder.exe`
   - Click "Settings" to configure your city/country
   - Set your preferred lock duration (10-15 minutes recommended)

2. **Daily Use**:
   - Click "Start" to begin monitoring prayer times
   - The app runs in background and will lock at prayer times
   - Beautiful lock screen appears with countdown timer
   - Computer automatically unlocks after set duration

3. **Emergency Exit**:
   - During lock screen, press and hold ESC key
   - Confirm emergency exit if needed

4. **Exiting the Application**:
   - Click "Exit" button
   - Reflect on the 3 meaningful questions about prayer
   - Confirm if you still wish to exit

## System Requirements

- Windows 7 or later (32-bit or 64-bit)
- At least 500MB free disk space
- Internet connection for fetching prayer times
- Administrator privileges (for system lock functionality)

## Troubleshooting

### If the application doesn't run:
- Make sure you're running on Windows
- Check that Windows Defender or other antivirus isn't blocking the executable
- Try running as administrator

### If prayer times don't appear:
- Verify internet connection
- Check that your city/country settings are correct
- Ensure the application can access the AlAdhan API

### If locking doesn't work:
- Run the application as administrator
- Check Windows security settings
- Verify the application has permission to lock the workstation

## Security Information

- The executable is created from verified Python source code
- No external tracking or data collection
- All settings stored locally in JSON format
- Emergency exit always available with ESC key

## Uninstallation

To completely remove the application:
1. Close the application
2. Delete the entire application folder
3. The application does not install system-wide components

## Support

If you experience issues:
1. Verify all system requirements are met
2. Check Windows Event Viewer for any error messages
3. Contact the application maintainer if issues persist

## License

This application is provided as-is for personal use. See the original source code for licensing information.