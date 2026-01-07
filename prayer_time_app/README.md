# Prayer Time Reminder and Auto Computer Lock System

A comprehensive Windows desktop application that helps Muslims maintain their prayer schedule by calculating accurate prayer times, providing Adhan notifications, and temporarily locking the computer during prayer times to encourage focus and devotion.

## Features

- **Accurate Prayer Times**: Calculates prayer times based on your geographic location using multiple calculation methods
- **Adhan Notifications**: Plays authentic Adhan audio at prayer times
- **Automatic Computer Locking**: Temporarily locks your computer for 10-15 minutes during prayer times
- **Emergency Unlock**: Allows immediate unlocking when needed
- **Customizable Settings**: Configure lock duration, enabled prayers, and notification preferences
- **System Tray Integration**: Runs quietly in the system tray
- **Windows Startup Integration**: Automatically starts with Windows
- **Security Focused**: Implements ethical guidelines and user consent

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Dependencies

The application requires the following Python packages:
- `requests` - For online prayer time API calls
- `pygame` - For audio playback
- `pystray` - For system tray integration
- `Pillow` - For image handling in system tray
- `pywin32` - For Windows-specific functionality
- `numpy` - For audio generation

## Usage

### Quick Start
Run the main application:
```
python main.py
```

This will present you with options to:
1. Add the application to Windows startup
2. Remove from Windows startup
3. Check startup status
4. Run the application normally
5. Exit

### Configuration

The application can be configured through the GUI:
- **Location Settings**: Set your latitude and longitude for accurate prayer times
- **Calculation Method**: Choose from multiple calculation methods (MWL, ISNA, Egypt, etc.)
- **Lock Settings**: Enable/disable auto-lock, set duration, select which prayers trigger locking
- **Notification Settings**: Configure volume and enable/disable Adhan

### Emergency Access

If you need to unlock your computer immediately during a lock period:
- Use the "Emergency Unlock" button in the application
- Or use the system tray menu if available

## Architecture

The application consists of several modules:

- `prayer_calculator.py`: Handles prayer time calculations with online/offline fallback
- `system_lock.py`: Manages Windows workstation locking/unlocking
- `notification_manager.py`: Handles Adhan playback and notifications
- `config_manager.py`: Manages user preferences and settings
- `security_manager.py`: Implements security, ethics, and user control
- `service.py`: Main background service that monitors prayer times
- `gui.py`: Graphical user interface with system tray integration
- `main.py`: Entry point with Windows startup integration

## Security and Ethics

The application implements several security and ethical measures:
- Maximum lock duration limits (30 minutes)
- Emergency unlock functionality always available
- User consent for all actions
- Detailed logging of security events
- Respect for user autonomy

## Customization

You can customize various aspects of the application:
- Prayer time calculation method
- Lock duration (5-30 minutes)
- Which prayers trigger auto-lock
- Audio volume levels
- Whether to play Adhan

## Troubleshooting

- If the application fails to start, ensure all dependencies are installed
- If locking doesn't work, ensure the application has necessary Windows permissions
- If Adhan doesn't play, check your system audio settings

## Academic Use

This application is designed to be suitable for academic submission with:
- Comprehensive documentation
- Modular architecture
- Security and ethical considerations
- Proper error handling
- Configurable settings

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is designed to help maintain prayer times but should not replace personal responsibility. Always ensure you can access your computer in emergency situations.