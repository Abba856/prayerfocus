import math
import json
import requests
import datetime
from datetime import date
import re

class PrayerCalculator:
    """
    Prayer time calculator with both online API and offline calculation capabilities
    """
    
    # Calculation Methods
    METHODS = {
        'MWL': {
            'name': 'Muslim World League',
            'params': {'fajr': 18, 'isha': 17}
        },
        'ISNA': {
            'name': 'Islamic Society of North America',
            'params': {'fajr': 15, 'isha': 15}
        },
        'Egypt': {
            'name': 'Egyptian General Authority of Survey',
            'params': {'fajr': 19.5, 'isha': 17.5}
        },
        'Makkah': {
            'name': 'Umm Al-Qura University, Makkah',
            'params': {'fajr': 18.5, 'isha': '90 min'}
        },
        'Karachi': {
            'name': 'University of Islamic Sciences, Karachi',
            'params': {'fajr': 18, 'isha': 18}
        },
        'Tehran': {
            'name': 'Institute of Geophysics, University of Tehran',
            'params': {'fajr': 17.7, 'isha': 14, 'maghrib': 4.5, 'midnight': 'Jafari'}
        },
        'Jafari': {
            'name': 'Shia Ithna-Ashari, Leva Institute, Qum',
            'params': {'fajr': 16, 'isha': 14, 'maghrib': 4, 'midnight': 'Jafari'}
        }
    }
    
    # Default Parameters
    DEFAULT_PARAMS = {
        'maghrib': '0 min',
        'midnight': 'Standard'
    }
    
    def __init__(self, method='MWL', coordinates=None, timezone=None):
        self.method = method
        self.coordinates = coordinates or (0, 0)  # (latitude, longitude)
        self.timezone = timezone or 0
        self.lat = coordinates[0] if coordinates else 0
        self.lng = coordinates[1] if coordinates else 0
        self.elv = 0  # Elevation
        self.settings = self._init_settings()
        self.time_format = '24h'
        self.num_iterations = 1
        self.offset = {name: 0 for name in self.get_time_names()}
        
    def _init_settings(self):
        """Initialize settings based on the selected method"""
        settings = {
            "imsak": '10 min',
            "dhuhr": '0 min',
            "asr": 'Standard',
            "highLats": 'NightMiddle',
            "midnight": "Standard"  # Add default midnight setting
        }

        # Add default values for all prayer times
        for param_name in ['fajr', 'isha', 'maghrib']:
            settings[param_name] = self.DEFAULT_PARAMS.get(param_name, 0)

        # Override with method-specific values
        if self.method in self.METHODS:
            params = self.METHODS[self.method]['params']
            for name, value in params.items():
                settings[name] = value

        return settings
    
    def get_time_names(self):
        """Return the prayer time names"""
        return {
            'imsak': 'Imsak',
            'fajr': 'Fajr', 
            'sunrise': 'Sunrise',
            'dhuhr': 'Dhuhr',
            'asr': 'Asr',
            'sunset': 'Sunset',
            'maghrib': 'Maghrib',
            'isha': 'Isha',
            'midnight': 'Midnight'
        }
    
    def set_location(self, coordinates, timezone):
        """Set the location and timezone"""
        self.coordinates = coordinates
        self.lat = coordinates[0]
        self.lng = coordinates[1]
        self.timezone = timezone
    
    def get_times_online(self, date_obj=None):
        """
        Get prayer times using online API (Aladhan)
        """
        if date_obj is None:
            date_obj = datetime.date.today()
            
        try:
            # Using Aladhan API
            url = f"http://api.aladhan.com/v1/calendar/{date_obj.day}/{date_obj.month}/{date_obj.year}"
            params = {
                'latitude': self.lat,
                'longitude': self.lng,
                'method': self._get_api_method()
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    # Extract today's prayer times
                    for item in data['data']:
                        if item['date']['gregorian']['day'] == str(date_obj.day):
                            times = item['timings']
                            # Format to our standard
                            result = {
                                'fajr': self._parse_time(times['Fajr']),
                                'sunrise': self._parse_time(times['Sunrise']),
                                'dhuhr': self._parse_time(times['Dhuhr']),
                                'asr': self._parse_time(times['Asr']),
                                'maghrib': self._parse_time(times['Maghrib']),
                                'isha': self._parse_time(times['Isha']),
                            }
                            return result
        except Exception as e:
            print(f"Online API failed: {e}")
            # Fall back to offline calculation
            return self.get_times_offline(date_obj)
        
        # If online fails, fall back to offline calculation
        return self.get_times_offline(date_obj)
    
    def _get_api_method(self):
        """Map our method to Aladhan API method numbers"""
        method_map = {
            'MWL': 3,      # Muslim World League
            'ISNA': 2,     # ISNA
            'Egypt': 5,    # Egyptian
            'Makkah': 4,   # Umm Al-Qura
            'Karachi': 6,  # University of Islamic Sciences, Karachi
            'Tehran': 7,   # Institute of Geophysics, University of Tehran
            'Jafari': 0    # Shia Ithna-Ashari
        }
        return method_map.get(self.method, 3)  # Default to MWL
    
    def _parse_time(self, time_str):
        """Parse time string from API to float hour"""
        try:
            # Format is "HH:MM" or "HH:MM:SS"
            parts = time_str.split(':')
            hour = int(parts[0])
            minute = int(parts[1])
            return hour + minute/60.0
        except:
            return 0.0
    
    def get_times_offline(self, date_obj=None):
        """
        Get prayer times using offline astronomical calculations
        Based on the praytimes.js algorithm
        """
        if date_obj is None:
            date_obj = datetime.date.today()
            
        year, month, day = date_obj.year, date_obj.month, date_obj.day
        
        # Calculate Julian date
        self.j_date = self.julian(year, month, day) - self.lng / (15 * 24.0)
        
        # Initial prayer times
        times = {
            'imsak': 5,
            'fajr': 5,
            'sunrise': 6,
            'dhuhr': 12,
            'asr': 13,
            'sunset': 18,
            'maghrib': 18,
            'isha': 18
        }
        
        # Main iterations
        for i in range(self.num_iterations):
            times = self._compute_prayer_times(times)
        
        times = self._adjust_times(times)
        
        # Add midnight time
        if self.settings['midnight'] == 'Jafari':
            times['midnight'] = times['sunset'] + self._time_diff(times['sunset'], times['fajr']) / 2
        else:
            times['midnight'] = times['sunset'] + self._time_diff(times['sunset'], times['sunrise']) / 2
        
        times = self._tune_times(times)
        
        # Convert to formatted time strings
        formatted_times = {}
        for name, value in times.items():
            formatted_times[name] = self._get_formatted_time(value, self.time_format)
        
        return formatted_times
    
    def _compute_prayer_times(self, times):
        """Compute prayer times at given julian date"""
        params = self.settings
        imsak = self._sun_angle_time(self._eval(params.get('imsak', '10 min')), times['imsak'], 'ccw')
        fajr = self._sun_angle_time(self._eval(params.get('fajr', 18)), times['fajr'], 'ccw')
        sunrise = self._sun_angle_time(self._rise_set_angle(self.elv), times['sunrise'], 'ccw')
        dhuhr = self._mid_day(times['dhuhr'])
        asr = self._asr_time(self._asr_factor(params.get('asr', 'Standard')), times['asr'])
        sunset = self._sun_angle_time(self._rise_set_angle(self.elv), times['sunset'])
        maghrib = self._sun_angle_time(self._eval(params.get('maghrib', '0 min')), times['maghrib'])
        isha = self._sun_angle_time(self._eval(params.get('isha', 17)), times['isha'])

        return {
            'imsak': imsak,
            'fajr': fajr,
            'sunrise': sunrise,
            'dhuhr': dhuhr,
            'asr': asr,
            'sunset': sunset,
            'maghrib': maghrib,
            'isha': isha
        }
    
    def _adjust_times(self, times):
        """Adjust times in a prayer time array"""
        params = self.settings
        tz_adjust = self.timezone - self.lng / 15.0
        
        for t, v in times.items():
            times[t] += tz_adjust
        
        if params['highLats'] != 'None':
            times = self._adjust_high_lats(times)
        
        if self._is_min(params['imsak']):
            times['imsak'] = times['fajr'] - self._eval(params['imsak']) / 60.0
        
        if self._is_min(params['maghrib']):
            times['maghrib'] = times['sunset'] - self._eval(params['maghrib']) / 60.0
        
        if self._is_min(params['isha']):
            times['isha'] = times['maghrib'] - self._eval(params['isha']) / 60.0
        
        times['dhuhr'] += self._eval(params['dhuhr']) / 60.0
        return times
    
    def _adjust_high_lats(self, times):
        """Adjust times for locations in higher latitudes"""
        params = self.settings
        night_time = self._time_diff(times['sunset'], times['sunrise'])
        
        times['imsak'] = self._adjust_hl_time(times['imsak'], times['sunrise'], 
                                             self._eval(params['imsak']), night_time, 'ccw')
        times['fajr'] = self._adjust_hl_time(times['fajr'], times['sunrise'], 
                                            self._eval(params['fajr']), night_time, 'ccw')
        times['isha'] = self._adjust_hl_time(times['isha'], times['sunset'], 
                                            self._eval(params['isha']), night_time)
        times['maghrib'] = self._adjust_hl_time(times['maghrib'], times['sunset'], 
                                               self._eval(params['maghrib']), night_time)
        return times
    
    def _adjust_hl_time(self, time, base, angle, night, direction=None):
        """Adjust a time for higher latitudes"""
        portion = self._night_portion(angle, night)
        diff = self._time_diff(time, base) if direction == 'ccw' else self._time_diff(base, time)
        
        if math.isnan(time) or diff > portion:
            time = base + (-portion if direction == 'ccw' else portion)
        return time
    
    def _night_portion(self, angle, night):
        """The night portion used for adjusting times in higher latitudes"""
        method = self.settings['highLats']
        portion = 1/2.0  # midnight
        
        if method == 'AngleBased':
            portion = 1/60.0 * angle
        elif method == 'OneSeventh':
            portion = 1/7.0
        
        return portion * night
    
    def _tune_times(self, times):
        """Apply offsets to the times"""
        for name, value in times.items():
            times[name] += self.offset[name] / 60.0
        return times
    
    def _get_formatted_time(self, time, format_type):
        """Convert float time to the given format"""
        if math.isnan(time):
            return '-----'
        
        time = self._fixhour(time + 0.5/60)  # Add 0.5 minutes to round
        hours = int(time)
        minutes = int((time - hours) * 60)
        
        if format_type == "24h":
            return f"{hours:02d}:{minutes:02d}"
        else:  # 12h format
            suffix = 'AM' if hours < 12 else 'PM'
            display_hour = hours % 12
            if display_hour == 0:
                display_hour = 12
            return f"{display_hour}:{minutes:02d} {suffix}"
    
    def _mid_day(self, time):
        """Compute mid-day time"""
        eqt = self._sun_position(self.j_date + time)[1]
        return self._fixhour(12 - eqt)
    
    def _sun_angle_time(self, angle, time, direction=None):
        """Compute the time at which sun reaches a specific angle below horizon"""
        try:
            decl = self._sun_position(self.j_date + time)[0]
            noon = self._mid_day(time)
            t = 1/15.0 * self._arccos((-self._sin(angle) - self._sin(decl) * self._sin(self.lat)) / 
                                     (self._cos(decl) * self._cos(self.lat)))
            return noon + (-t if direction == 'ccw' else t)
        except ValueError:
            return float('nan')
    
    def _asr_time(self, factor, time):
        """Compute asr time"""
        decl = self._sun_position(self.j_date + time)[0]
        angle = -self._arccot(factor + self._tan(abs(self.lat - decl)))
        return self._sun_angle_time(angle, time)
    
    def _sun_position(self, jd):
        """Compute declination angle of sun and equation of time"""
        D = jd - 2451545.0
        g = self._fixangle(357.529 + 0.98560028 * D)
        q = self._fixangle(280.459 + 0.98564736 * D)
        L = self._fixangle(q + 1.915 * self._sin(g) + 0.020 * self._sin(2*g))
        e = 23.439 - 0.00000036 * D
        RA = self._arctan2(self._cos(e) * self._sin(L), self._cos(L)) / 15.0
        eqt = q/15.0 - self._fixhour(RA)
        decl = self._arcsin(self._sin(e) * self._sin(L))
        return (decl, eqt)
    
    def julian(self, year, month, day):
        """Convert Gregorian date to Julian day"""
        if month <= 2:
            year -= 1
            month += 12
        A = int(year / 100)
        B = 2 - A + int(A / 4)
        return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    
    def _asr_factor(self, asr_param):
        """Get asr shadow factor"""
        methods = {'Standard': 1, 'Hanafi': 2}
        if asr_param in methods:
            return methods[asr_param]
        return self._eval(asr_param)
    
    def _rise_set_angle(self, elevation=0):
        """Return sun angle for sunset/sunrise"""
        elevation = 0 if elevation is None else elevation
        return 0.833 + 0.0347 * math.sqrt(elevation)
    
    def _time_diff(self, time1, time2):
        """Compute the difference between two times"""
        return self._fixhour(time2 - time1)
    
    def _eval(self, st):
        """Convert given string into a number"""
        if isinstance(st, (int, float)):
            return float(st)
        
        val = re.split('[^0-9.+-]', str(st), 1)[0]
        return float(val) if val else 0
    
    def _is_min(self, arg):
        """Detect if input contains 'min'"""
        return isinstance(arg, str) and 'min' in arg
    
    #----------------- Degree-Based Math Functions -------------------
    def _sin(self, d):
        return math.sin(math.radians(d))
    
    def _cos(self, d):
        return math.cos(math.radians(d))
    
    def _tan(self, d):
        return math.tan(math.radians(d))
    
    def _arcsin(self, x):
        return math.degrees(math.asin(x))
    
    def _arccos(self, x):
        return math.degrees(math.acos(x))
    
    def _arctan(self, x):
        return math.degrees(math.atan(x))
    
    def _arccot(self, x):
        return math.degrees(math.atan(1.0/x))
    
    def _arctan2(self, y, x):
        return math.degrees(math.atan2(y, x))
    
    def _fixangle(self, angle):
        return self._fix(angle, 360.0)
    
    def _fixhour(self, hour):
        return self._fix(hour, 24.0)
    
    def _fix(self, a, mode):
        if math.isnan(a):
            return a
        a = a - mode * (math.floor(a / mode))
        return a + mode if a < 0 else a


# Example usage and testing
if __name__ == "__main__":
    # Example: Calculate prayer times for New York
    calculator = PrayerCalculator(method='MWL', coordinates=(40.7128, -74.0060), timezone=-5)
    times = calculator.get_times_online()
    print("Prayer times:", times)
    
    # Test offline calculation
    offline_times = calculator.get_times_offline()
    print("Offline calculation:", offline_times)