# Prayer Time Reminder and Auto Lock System
# Minimal, focused implementation for Windows

import json
import requests
import time
import threading
import ctypes
import tkinter as tk
from tkinter import messagebox, ttk
from plyer import notification
import schedule
from datetime import datetime
import os
import sys

class PrayerApp:
    def __init__(self):
        self.settings_file = "prayer_settings.json"
        self.settings = self.load_settings()
        self.running = False
        self.lock_window = None
        
    def load_settings(self):
        """Load settings from JSON file"""
        default_settings = {
            "city": "London",
            "country": "UK",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "lock_duration": 10,  # in minutes
            "play_adhan": True,
            "auto_start": False
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key in default_settings:
                        if key not in loaded:
                            loaded[key] = default_settings[key]
                    return loaded
            except:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to JSON file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get_prayer_times(self):
        """Fetch prayer times from AlAdhan API"""
        try:
            url = f"http://api.aladhan.com/v1/timingsByCity/{datetime.now().strftime('%d-%m-%Y')}"
            params = {
                'city': self.settings['city'],
                'country': self.settings['country'],
                'method': 2  # ISNA method
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    timings = data['data']['timings']
                    return {
                        'Fajr': timings['Fajr'][:5],
                        'Dhuhr': timings['Dhuhr'][:5],
                        'Asr': timings['Asr'][:5],
                        'Maghrib': timings['Maghrib'][:5],
                        'Isha': timings['Isha'][:5]
                    }
            return None
        except Exception as e:
            print(f"Error fetching prayer times: {e}")
            return None
    
    def show_notification(self, title, message):
        """Show desktop notification"""
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=10
            )
        except:
            # Fallback to print if plyer fails
            print(f"NOTIFICATION: {title} - {message}")
    
    def lock_computer(self):
        """Lock Windows computer using ctypes"""
        ctypes.windll.user32.LockWorkStation()
    
    def show_lock_screen(self):
        """Show a beautiful lock screen with countdown"""
        if self.lock_window:
            return
            
        self.lock_window = tk.Toplevel()
        self.lock_window.attributes('-fullscreen', True)
        self.lock_window.configure(bg='black')
        self.lock_window.attributes('-topmost', True)
        
        # Center frame
        center_frame = tk.Frame(self.lock_window, bg='black')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Prayer info
        prayer_label = tk.Label(
            center_frame, 
            text="Time for Prayer", 
            font=('Arial', 48, 'bold'), 
            fg='white', 
            bg='black'
        )
        prayer_label.pack(pady=20)
        
        # Countdown
        self.countdown_var = tk.StringVar()
        self.countdown_var.set(f"Computer will unlock in {self.settings['lock_duration']} minutes")
        countdown_label = tk.Label(
            center_frame, 
            textvariable=self.countdown_var,
            font=('Arial', 24), 
            fg='gray', 
            bg='black'
        )
        countdown_label.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(
            center_frame,
            text="Press and hold ESC to exit (for emergencies)",
            font=('Arial', 16),
            fg='red',
            bg='black'
        )
        instruction_label.pack(pady=20)
        
        # Bind ESC key for emergency exit
        self.lock_window.bind('<Escape>', self.emergency_exit)
        self.lock_window.focus_set()
        
        # Start countdown
        self.start_countdown()
    
    def start_countdown(self):
        """Start the countdown for unlock"""
        remaining = self.settings['lock_duration'] * 60  # Convert to seconds
        
        def update_countdown():
            nonlocal remaining
            if remaining <= 0:
                self.unlock_screen()
                return
            
            mins, secs = divmod(remaining, 60)
            self.countdown_var.set(f"Computer will unlock in {mins:02d}:{secs:02d}")
            remaining -= 1
            
            if self.lock_window:
                self.lock_window.after(1000, update_countdown)
        
        update_countdown()
    
    def unlock_screen(self):
        """Close the lock screen"""
        if self.lock_window:
            self.lock_window.destroy()
            self.lock_window = None
    
    def emergency_exit(self, event=None):
        """Emergency exit by holding ESC key"""
        # Create a simple dialog to confirm emergency exit
        if messagebox.askyesno("Emergency Exit", "Are you sure you want to exit the prayer lock? This should only be used in emergencies."):
            self.unlock_screen()
            self.lock_computer()  # Actually lock the computer to return to Windows lock screen
    
    def handle_prayer_time(self, prayer_name):
        """Handle when it's time for prayer"""
        self.show_notification(
            f"Time for {prayer_name}",
            f"It's now time for {prayer_name} prayer. Computer will lock shortly."
        )
        
        # Lock computer after a short delay
        time.sleep(5)  # Give user 5 seconds warning
        
        # Show beautiful lock screen
        self.show_lock_screen()
        
        # Actually lock Windows after showing our screen
        time.sleep(2)
        self.lock_computer()
        
        # Schedule unlock after specified duration
        threading.Timer(self.settings['lock_duration'] * 60, self.schedule_unlock).start()
    
    def schedule_unlock(self):
        """Schedule the unlock"""
        # Just close our lock screen, Windows will remain locked until user unlocks
        self.unlock_screen()
    
    def setup_schedules(self):
        """Setup prayer time schedules"""
        prayer_times = self.get_prayer_times()
        if not prayer_times:
            print("Could not fetch prayer times")
            return False
        
        # Clear existing schedules
        schedule.clear()
        
        # Schedule each prayer time
        for prayer, time_str in prayer_times.items():
            hour, minute = map(int, time_str.split(':'))
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
                self.handle_prayer_time, prayer
            )
            print(f"Scheduled {prayer} at {time_str}")
        
        return True
    
    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    
    def start(self):
        """Start the application"""
        if not self.setup_schedules():
            return False
        
        self.running = True
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        return True
    
    def stop(self):
        """Stop the application"""
        self.running = False
        schedule.clear()

class SettingsWindow:
    def __init__(self, parent, app):
        self.app = app
        self.window = tk.Toplevel(parent)
        self.window.title("Prayer App Settings")
        self.window.geometry("400x300")
        
        self.create_widgets()
        self.load_current_settings()
    
    def create_widgets(self):
        # City
        tk.Label(self.window, text="City:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.city_entry = tk.Entry(self.window, width=30)
        self.city_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Country
        tk.Label(self.window, text="Country:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.country_entry = tk.Entry(self.window, width=30)
        self.country_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Lock duration
        tk.Label(self.window, text="Lock Duration (minutes):").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.duration_var = tk.StringVar()
        duration_spin = tk.Spinbox(self.window, from_=5, to=30, textvariable=self.duration_var, width=10)
        duration_spin.grid(row=2, column=1, padx=10, pady=5)
        
        # Play Adhan
        self.adhan_var = tk.BooleanVar()
        tk.Checkbutton(self.window, text="Play Adhan", variable=self.adhan_var).grid(
            row=3, column=0, columnspan=2, sticky='w', padx=10, pady=5
        )
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", command=self.save_settings).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side='left', padx=5)
    
    def load_current_settings(self):
        """Load current settings into widgets"""
        self.city_entry.insert(0, self.app.settings['city'])
        self.country_entry.insert(0, self.app.settings['country'])
        self.duration_var.set(str(self.app.settings['lock_duration']))
        self.adhan_var.set(self.app.settings['play_adhan'])
    
    def save_settings(self):
        """Save settings from widgets"""
        self.app.settings['city'] = self.city_entry.get()
        self.app.settings['country'] = self.country_entry.get()
        self.app.settings['lock_duration'] = int(self.duration_var.get())
        self.app.settings['play_adhan'] = self.adhan_var.get()
        
        self.app.save_settings()
        messagebox.showinfo("Success", "Settings saved successfully!")
        self.window.destroy()

def main():
    root = tk.Tk()
    root.title("Prayer Time Reminder")
    root.geometry("300x200")
    
    app = PrayerApp()
    
    def start_app():
        if app.start():
            status_label.config(text="Status: Running", fg="green")
            start_btn.config(state="disabled")
            stop_btn.config(state="normal")
        else:
            messagebox.showerror("Error", "Failed to start. Check your internet connection and settings.")
    
    def stop_app():
        app.stop()
        status_label.config(text="Status: Stopped", fg="red")
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
    
    def show_settings():
        SettingsWindow(root, app)
    
    def exit_with_questions():
        # Ask 3 meaningful questions before exiting
        questions = [
            "If Allah is the One who gives you life, time, and every blessing you enjoy, what is holding you back from meeting Him for a few minutes in Ṣalāh?",
            "When you stand before Allah on the Day of Judgment and He asks about your prayers, what answer do you hope to give?",
            "If this prayer was the last chance Allah gave you to return to Him, would you still choose to ignore it?"
        ]

        # Show each question in sequence
        for i, question in enumerate(questions, 1):
            result = messagebox.askquestion(f"Question {i}", question)
            # Don't require specific answers, just show the questions for reflection
            if result is None:  # User cancelled
                return

        # After showing all questions, ask if they still want to exit
        final_confirmation = messagebox.askyesno("Exit Confirmation", "Do you still wish to exit the prayer reminder app?")
        if final_confirmation:
            root.quit()
    
    # GUI Elements
    tk.Label(root, text="Prayer Time Reminder", font=('Arial', 16, 'bold')).pack(pady=10)
    
    status_label = tk.Label(root, text="Status: Stopped", fg="red")
    status_label.pack(pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    start_btn = tk.Button(button_frame, text="Start", command=start_app, width=10)
    start_btn.pack(side='left', padx=5)
    
    stop_btn = tk.Button(button_frame, text="Stop", command=stop_app, width=10, state="disabled")
    stop_btn.pack(side='left', padx=5)
    
    tk.Button(button_frame, text="Settings", command=show_settings, width=10).pack(side='left', padx=5)
    
    tk.Button(root, text="Exit", command=exit_with_questions, width=20).pack(pady=10)
    
    # Handle window close
    def on_closing():
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            exit_with_questions()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    if sys.platform != 'win32':
        print("This application is designed for Windows only")
        sys.exit(1)
    
    main()