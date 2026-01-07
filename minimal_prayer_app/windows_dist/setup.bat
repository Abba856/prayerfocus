@echo off
echo.
echo ================================================
echo Prayer Time Reminder and Auto Lock System Setup
echo ================================================
echo.
echo This will install the Prayer Time Reminder application on your Windows system.
echo.
echo Requirements:
echo - Windows 7 or later
echo - At least 500MB free disk space
echo.
echo The application will:
echo - Help you observe daily prayers
echo - Lock your computer during prayer times
echo - Show beautiful lock screens with countdown
echo - Ask meaningful questions before exit
echo.
echo Press any key to continue with installation...
pause >nul

echo.
echo Creating application directory...
if not exist "%USERPROFILE%\PrayerTimeReminder" mkdir "%USERPROFILE%\PrayerTimeReminder"

echo Copying application files...
copy "PrayerTimeReminder.exe" "%USERPROFILE%\PrayerTimeReminder\" >nul

echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Prayer Time Reminder.lnk'); $Shortcut.TargetPath = '%USERPROFILE%\PrayerTimeReminder\PrayerTimeReminder.exe'; $Shortcut.Save()" >nul 2>&1 || echo Warning: Could not create desktop shortcut

echo.
echo Installation completed successfully!
echo.
echo To run the application:
echo 1. Go to %USERPROFILE%\PrayerTimeReminder
echo 2. Run PrayerTimeReminder.exe
echo.
echo Or use the desktop shortcut if created successfully.
echo.
echo Press any key to exit...
pause >nul