"""Model manager backend for the application"""

import os
import json
import numpy as np
from typing import List, Dict, Any

from Reinforcement.controller import Controller


class ModelManager:
    """Model management backend"""
    
    def __init__(self, settings):
        self.controllers = {}
        self.model_configs = {}  # Store full config including metadata
        self.settings = settings
        os.makedirs(self.settings.get("data_folder", "./backstaff_data"), exist_ok=True)
        self._load_controllers()

    def _models_path(self) -> str:
        data_folder = self.settings.get("data_folder", "./backstaff_data")
        os.makedirs(data_folder, exist_ok=True)
        return os.path.join(data_folder, "models.json")
    
    def _load_controllers(self):
        models_file = self._models_path()
        legacy_models_file = "models.json"
        source_file = models_file if os.path.exists(models_file) else None
        if not source_file and os.path.exists(legacy_models_file):
            source_file = legacy_models_file
        if source_file:
            try:
                with open(source_file, 'r') as f:
                    models = json.load(f)
                    for name, config in models.items():
                        try:
                            self.controllers[name] = Controller(
                                weights=config.get('current_weights', config['initial_weights']),
                                mins=config['mins'],
                                maxs=config['maxs'],
                                not_reached_error=100,
                                filename=name + ".json",
                                load=False,
                                stoc_rates=config.get('stoc_rates', [0.1] * config['num_params']),
                                learning_rate=config['learning_rates'][0] if config['learning_rates'] else 0.01
                            )
                            # Store full config
                            self.model_configs[name] = config
                        except Exception as e:
                            print(f"Warning: Could not load controller {name}: {e}")
                # If we loaded from legacy location, persist to the new data folder
                if source_file == legacy_models_file and not os.path.exists(models_file):
                    self._save_models()
            except Exception as e:
                print(f"Warning: Could not load models file: {e}")
    
    def _save_models(self):
        models = {}
        for name, controller in self.controllers.items():
            current_weights = controller.get_weights()
            if hasattr(current_weights, "tolist"):
                current_weights = current_weights.tolist()
            
            # Start with existing config if available
            base_config = self.model_configs.get(name, {})
            
            models[name] = {
                "name": name,
                "optimizer_type": "Standard Optimizer",
                "num_params": len(controller.opt.mins),
                "param_names": base_config.get('param_names', []),
                "mins": controller.opt.mins.tolist(),
                "maxs": controller.opt.maxs.tolist(),
                "learning_rates": [controller.opt.learning_rate] * len(controller.opt.mins),
                "initial_weights": controller.opt.current.tolist(),
                "current_weights": current_weights,
                "stoc_rates": controller.opt.stoc_rates.tolist(),
                "stochasticity_rate": base_config.get('stochasticity_rate', 1.0),
                "loss_function": base_config.get('loss_function', ''),
                "custom_param_names": base_config.get('custom_param_names', []),
                "custom_param_values": base_config.get('custom_param_values', [])
            }
        
        models_file = self._models_path()
        with open(models_file, 'w') as f:
            json.dump(models, f, indent=2)
    
    def add_model(self, name: str, config: Dict[str, Any]):
        if name in self.controllers:
            raise ValueError(f"Model '{name}' already exists.")

        self.controllers[name] = Controller(
            weights=config['initial_weights'],
            mins=config['mins'],
            maxs=config['maxs'],
            not_reached_error=100,
            filename=name + ".json",
            load=False,
            stoc_rates=config.get('stoc_rates', [0.1] * config['num_params']),
            learning_rate=config['learning_rates'][0] if config['learning_rates'] else 0.01
        )

        # Persist the full config so model-specific metadata (including loss) is saved
        self.model_configs[name] = config
        
        self._save_models()
    
    def remove_model(self, name: str) -> bool:
        if name in self.controllers:
            del self.controllers[name]
            if name in self.model_configs:
                del self.model_configs[name]
            self._save_models()
            return True
        return False
    
    def get_model(self, name: str) -> Dict[str, Any]:
        if name not in self.controllers:
            return None
        
        # Get the stored config
        config = self.model_configs.get(name, {})
        
        controller = self.controllers[name]
        current_weights = controller.get_weights()
        if hasattr(current_weights, "tolist"):
            current_weights = current_weights.tolist()
        
        # Merge controller state with stored config
        return {
            "name": name,
            "optimizer_type": config.get("optimizer_type", "Standard Optimizer"),
            "num_params": len(controller.opt.mins),
            "param_names": config.get('param_names', []),
            "mins": controller.opt.mins.tolist(),
            "maxs": controller.opt.maxs.tolist(),
            "learning_rates": [controller.opt.learning_rate] * len(controller.opt.mins),
            "initial_weights": controller.opt.current.tolist(),
            "current_weights": current_weights,
            "stoc_rates": controller.opt.stoc_rates.tolist(),
            "loss_function": config.get('loss_function', ''),
            "custom_param_names": config.get('custom_param_names', []),
            "custom_param_values": config.get('custom_param_values', [])
        }
    
    def get_all_models(self) -> List[str]:
        return list(self.controllers.keys())
    
    def update_model(self, name: str, config: Dict[str, Any]):
        if name in self.controllers:
            controller = self.controllers[name]
            
            if 'mins' in config:
                controller.opt.mins = np.array(config['mins'])
            if 'maxs' in config:
                controller.opt.maxs = np.array(config['maxs'])
            if 'learning_rates' in config:
                controller.opt.learning_rate = config['learning_rates'][0] if config['learning_rates'] else 0.01
            if 'stoc_rates' in config:
                controller.opt.stoc_rates = np.array(config['stoc_rates'])
            if 'current_weights' in config:
                controller.opt.current = np.array(config['current_weights'])
                controller.current = np.array(config['current_weights'])
            
            # Store the full config
            self.model_configs[name] = config
            
            self._save_models()
            return True
        return False
    
    def model_exists(self, name: str) -> bool:
        return name in self.controllers
    
    def get_controller(self, name: str) -> Controller:
        return self.controllers.get(name)
