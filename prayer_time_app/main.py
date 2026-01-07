import sys
import os
import subprocess
import winreg

def add_to_startup():
    """
    Add the application to Windows startup
    """
    try:
        # Get the path to this script
        script_path = os.path.abspath(__file__)
        # Get the directory containing this script
        script_dir = os.path.dirname(script_path)
        # Main executable path
        main_exe = os.path.join(script_dir, "main.py")
        
        # Use the Python executable that's running this script
        python_exe = sys.executable
        
        # Create the command to run the application
        command = f'"{python_exe}" "{main_exe}" --minimized'
        
        # Open the registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Set the value for our application
        winreg.SetValueEx(key, "PrayerTimeReminder", 0, winreg.REG_SZ, command)
        
        # Close the key
        winreg.CloseKey(key)
        
        print("Successfully added to Windows startup")
        return True
    except Exception as e:
        print(f"Error adding to startup: {e}")
        return False

def remove_from_startup():
    """
    Remove the application from Windows startup
    """
    try:
        # Open the registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Delete the value for our application
        winreg.DeleteValue(key, "PrayerTimeReminder")
        
        # Close the key
        winreg.CloseKey(key)
        
        print("Successfully removed from Windows startup")
        return True
    except FileNotFoundError:
        print("Application not found in startup")
        return False
    except Exception as e:
        print(f"Error removing from startup: {e}")
        return False

def is_in_startup():
    """
    Check if the application is in Windows startup
    """
    try:
        # Open the registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        
        # Try to get the value for our application
        try:
            value, _ = winreg.QueryValueEx(key, "PrayerTimeReminder")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception as e:
        print(f"Error checking startup status: {e}")
        return False

def setup_startup_option():
    """
    Provide option to add/remove from startup
    """
    print("Prayer Time Reminder Setup")
    print("1. Add to Windows startup")
    print("2. Remove from Windows startup")
    print("3. Check startup status")
    print("4. Run application normally")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        add_to_startup()
    elif choice == "2":
        remove_from_startup()
    elif choice == "3":
        if is_in_startup():
            print("Application is in Windows startup")
        else:
            print("Application is NOT in Windows startup")
    elif choice == "4":
        # Run the main application
        from gui import PrayerTimeGUI
        app = PrayerTimeGUI()
        app.run()
    elif choice == "5":
        print("Exiting...")
        return
    else:
        print("Invalid choice")
        return
    
    # Ask if user wants to run the application
    if choice in ["1", "2", "3"]:
        run_now = input("Do you want to run the application now? (y/n): ").lower().strip()
        if run_now == 'y':
            from gui import PrayerTimeGUI
            app = PrayerTimeGUI()
            app.run()

if __name__ == "__main__":
    if sys.platform != 'win32':
        print("This setup is designed for Windows systems only")
        sys.exit(1)
    
    # If command line argument for minimized startup is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--minimized":
        # Run the application minimized (in system tray)
        from gui import PrayerTimeGUI
        app = PrayerTimeGUI()
        # Start minimized to system tray
        app.root.withdraw()  # Hide the window initially
        app.create_system_tray_icon()
        app.root.mainloop()
    else:
        # Show setup options
        setup_startup_option()