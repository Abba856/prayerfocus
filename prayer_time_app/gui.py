import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from datetime import datetime
from service import PrayerTimeService
from config_manager import ConfigManager

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False
    print("pystray not available. System tray functionality will be limited.")


class PrayerTimeGUI:
    """
    Graphical user interface for the Prayer Time Reminder application
    """
    
    def __init__(self):
        self.service = PrayerTimeService()
        self.config_manager = self.service.config_manager
        self.root = None
        self.system_tray_icon = None
        self.status_label = None
        self.prayer_times_text = None
        self.setup_gui()
    
    def setup_gui(self):
        """Initialize the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Prayer Time Reminder and Auto Lock System")
        self.root.geometry("600x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main tab
        self.create_main_tab(notebook)
        
        # Settings tab
        self.create_settings_tab(notebook)
        
        # About tab
        self.create_about_tab(notebook)
        
        # Start the service
        self.service.start_service()
        
        # Update prayer times display
        self.update_prayer_times_display()
        
        # Schedule periodic updates
        self.root.after(1000, self.periodic_update)
    
    def create_main_tab(self, notebook):
        """Create the main tab with prayer times and controls"""
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="Main")
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Service Status: Starting...", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        # Prayer times display
        ttk.Label(main_frame, text="Today's Prayer Times:", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        # Create a text widget with scrollbar for prayer times
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.prayer_times_text = tk.Text(text_frame, height=10, width=50)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.prayer_times_text.yview)
        self.prayer_times_text.configure(yscrollcommand=scrollbar.set)
        
        self.prayer_times_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Refresh Prayer Times", command=self.update_prayer_times_display).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Emergency Unlock", command=self.emergency_unlock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Settings", command=self.show_settings).pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self, notebook):
        """Create the settings tab"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Settings")
        
        # Location settings
        location_frame = ttk.LabelFrame(settings_frame, text="Location Settings")
        location_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(location_frame, text="Latitude:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.lat_entry = ttk.Entry(location_frame, width=15)
        self.lat_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(location_frame, text="Longitude:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.lng_entry = ttk.Entry(location_frame, width=15)
        self.lng_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(location_frame, text="Update Location", command=self.update_location).grid(row=0, column=4, padx=5, pady=5)
        
        # Calculation method
        calc_frame = ttk.LabelFrame(settings_frame, text="Calculation Settings")
        calc_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(calc_frame, text="Calculation Method:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.method_var = tk.StringVar()
        method_combo = ttk.Combobox(calc_frame, textvariable=self.method_var, 
                                   values=["MWL", "ISNA", "Egypt", "Makkah", "Karachi", "Tehran", "Jafari"],
                                   state="readonly", width=15)
        method_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(calc_frame, text="Update Method", command=self.update_calculation_method).grid(row=0, column=2, padx=5, pady=5)
        
        # Lock settings
        lock_frame = ttk.LabelFrame(settings_frame, text="Lock Settings")
        lock_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.lock_enabled_var = tk.BooleanVar()
        lock_enabled_check = ttk.Checkbutton(lock_frame, text="Enable Auto-Lock", 
                                           variable=self.lock_enabled_var)
        lock_enabled_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(lock_frame, text="Lock Duration (minutes):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.duration_var = tk.StringVar()
        duration_spin = ttk.Spinbox(lock_frame, from_=5, to=30, textvariable=self.duration_var, width=10)
        duration_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # Notification settings
        notif_frame = ttk.LabelFrame(settings_frame, text="Notification Settings")
        notif_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.play_adhan_var = tk.BooleanVar()
        adhan_check = ttk.Checkbutton(notif_frame, text="Play Adhan", variable=self.play_adhan_var)
        adhan_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(notif_frame, text="Adhan Volume:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.volume_var = tk.DoubleVar()
        volume_scale = ttk.Scale(notif_frame, from_=0.0, to=1.0, variable=self.volume_var, 
                                orient=tk.HORIZONTAL, length=200)
        volume_scale.grid(row=1, column=1, padx=5, pady=5)
        
        # Load current settings
        self.load_settings()
    
    def create_about_tab(self, notebook):
        """Create the about tab"""
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="About")
        
        about_text = """
Prayer Time Reminder and Auto Computer Lock System

This application helps Muslims maintain their prayer schedule by:
- Calculating accurate prayer times based on your location
- Providing Adhan notifications at prayer times
- Automatically locking your computer during prayer times
- Allowing emergency unlock when needed

Features:
- Multiple calculation methods
- Configurable lock duration
- Adhan audio playback
- System tray integration
- Location-based calculations

Version: 1.0
        """
        
        text_widget = tk.Text(about_frame, wrap=tk.WORD, state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, about_text)
        text_widget.config(state=tk.DISABLED)
    
    def load_settings(self):
        """Load current settings into GUI elements"""
        location = self.config_manager.get_location()
        self.lat_entry.delete(0, tk.END)
        self.lat_entry.insert(0, str(location['latitude']))
        self.lng_entry.delete(0, tk.END)
        self.lng_entry.insert(0, str(location['longitude']))
        
        self.method_var.set(self.config_manager.get_calculation_method())
        
        lock_settings = self.config_manager.get_lock_settings()
        self.lock_enabled_var.set(lock_settings.get('enabled', True))
        self.duration_var.set(str(lock_settings.get('duration_minutes', 10)))
        
        notif_settings = self.config_manager.get_notification_settings()
        self.play_adhan_var.set(notif_settings.get('play_adhan', True))
        self.volume_var.set(notif_settings.get('adhan_volume', 0.7))
    
    def update_location(self):
        """Update location from GUI inputs"""
        try:
            lat = float(self.lat_entry.get())
            lng = float(self.lng_entry.get())
            
            # Validate latitude and longitude ranges
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                messagebox.showerror("Invalid Location", "Please enter valid coordinates:\nLatitude: -90 to 90\nLongitude: -180 to 180")
                return
            
            self.config_manager.set_location(lat, lng)
            self.service.update_location()
            self.config_manager.save_config()
            
            messagebox.showinfo("Success", "Location updated successfully!")
            self.update_prayer_times_display()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for latitude and longitude")
    
    def update_calculation_method(self):
        """Update calculation method from GUI"""
        method = self.method_var.get()
        if method:
            self.config_manager.set_calculation_method(method)
            self.config_manager.save_config()
            messagebox.showinfo("Success", f"Calculation method updated to {method}")
            self.update_prayer_times_display()
    
    def update_prayer_times_display(self):
        """Update the prayer times display"""
        try:
            times = self.service.get_today_prayer_times()
            self.prayer_times_text.config(state=tk.NORMAL)
            self.prayer_times_text.delete(1.0, tk.END)
            
            if times:
                text_content = "Prayer Times for Today:\n"
                text_content += "=" * 30 + "\n"
                for prayer, time_str in times.items():
                    text_content += f"{prayer.capitalize()}: {time_str}\n"
                
                self.prayer_times_text.insert(tk.END, text_content)
            else:
                self.prayer_times_text.insert(tk.END, "Could not retrieve prayer times. Please check your internet connection and location settings.")
            
            self.prayer_times_text.config(state=tk.DISABLED)
        except Exception as e:
            self.prayer_times_text.config(state=tk.NORMAL)
            self.prayer_times_text.delete(1.0, tk.END)
            self.prayer_times_text.insert(tk.END, f"Error loading prayer times: {e}")
            self.prayer_times_text.config(state=tk.DISABLED)
    
    def emergency_unlock(self):
        """Handle emergency unlock"""
        if self.service.emergency_unlock():
            messagebox.showinfo("Emergency Unlock", "System unlocked successfully!")
        else:
            messagebox.showwarning("Emergency Unlock", "System was not locked or unlock failed.")
    
    def show_settings(self):
        """Show settings dialog"""
        self.root.focus_set()
    
    def periodic_update(self):
        """Periodically update the GUI with service status"""
        try:
            status = self.service.get_current_status()
            lock_status = "LOCKED" if status["is_system_locked"] else "UNLOCKED"
            service_status = "RUNNING" if status["is_running"] else "STOPPED"
            
            self.status_label.config(text=f"Service: {service_status} | System: {lock_status}")
        except Exception as e:
            self.status_label.config(text=f"Error updating status: {e}")
        
        # Schedule next update
        self.root.after(1000, self.periodic_update)
    
    def on_closing(self):
        """Handle application closing"""
        # Minimize to system tray instead of closing if supported
        if PYSTRAY_AVAILABLE:
            self.root.withdraw()  # Hide the window
            self.create_system_tray_icon()
        else:
            # If system tray is not available, ask user if they want to quit
            if messagebox.askokcancel("Quit", "Do you want to quit the application?\nThe service will stop."):
                self.service.stop_service()
                self.root.destroy()
    
    def create_system_tray_icon(self):
        """Create system tray icon"""
        if not PYSTRAY_AVAILABLE:
            return
        
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='blue')
        dc = ImageDraw.Draw(image)
        dc.text((10, 20), 'PT', fill=(255, 255, 255))
        
        menu = (item('Show', self.show_from_tray), 
                item('Emergency Unlock', self.emergency_unlock_from_tray),
                item('Exit', self.exit_from_tray))
        
        self.system_tray_icon = pystray.Icon("Prayer Time", image, "Prayer Time Reminder", menu)
        self.system_tray_icon.run_detached()
    
    def show_from_tray(self, icon, item):
        """Show the main window from system tray"""
        self.root.deiconify()
        self.root.lift()
    
    def emergency_unlock_from_tray(self, icon, item):
        """Perform emergency unlock from system tray"""
        self.service.emergency_unlock()
    
    def exit_from_tray(self, icon, item):
        """Exit the application from system tray"""
        if self.system_tray_icon:
            self.system_tray_icon.stop()
        self.service.stop_service()
        self.root.quit()
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    if sys.platform != 'win32':
        print("This application is designed for Windows systems only")
        sys.exit(1)
    
    app = PrayerTimeGUI()
    app.run()