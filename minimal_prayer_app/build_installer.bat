@echo off
echo Building Prayer Time Reminder Installer...
echo.

REM Change to the application directory
cd /d "%~dp0"

REM Create the executable using PyInstaller
echo Creating executable...
pyinstaller prayer_app.spec

echo.
echo Build completed! The executable is located in the 'dist' folder.
echo Look for the 'PrayerTimeReminder.exe' file.
echo.
echo To create a Windows installer (.msi), you would typically use:
echo 1. Advanced Installer
echo 2. Inno Setup
echo 3. WiX Toolset
echo.
echo For a simple distribution, the .exe file in the dist folder is sufficient.
pause