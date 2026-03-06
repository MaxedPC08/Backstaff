"""Settings management for the application"""

import os
import json


class Settings:
    """Settings management backend"""
    
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.default_data_folder = os.path.join(base_dir, "backstaff_data")
        self.settings_file = os.path.join(base_dir, "backstaff_settings.json")
        self.default_settings = {
            "data_folder": self.default_data_folder,
            "dark_mode": False
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        os.makedirs(os.path.dirname(self.settings_file) or ".", exist_ok=True)
        legacy_data_path = os.path.join(self.default_data_folder, "backstaff_settings.json")
        legacy_root_path = "backstaff_settings.json"
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                return self.default_settings.copy()
        for legacy_path in [legacy_data_path, legacy_root_path]:
            if os.path.exists(legacy_path):
                try:
                    with open(legacy_path, 'r') as f:
                        data = json.load(f)
                    self.settings = data
                    self.save_settings()
                    return data
                except:
                    return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to file"""
        os.makedirs(os.path.dirname(self.settings_file) or ".", exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
