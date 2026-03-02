from Reinforcement.controller import Controller
import numpy as np
import os
import json


class ControllerFunctionalObject:
    
    def __init__(self, *args, **kwargs):
        self.controllers = {}
        self._load_controllers()

    def _load_controllers(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "Data", "controllers.json")
        
        if os.path.exists(data_path):
            try:
                with open(data_path, "r") as f:
                    controller_names = json.load(f)
                    for name in controller_names:
                        try:
                            self.controllers[name] = Controller(
                                weights=[0.5],
                                mins=[0.0],
                                maxs=[1.0],
                                filename=name + ".json",
                                load=True
                            )
                        except Exception as e:
                            print(f"Warning: Could not load controller {name}: {e}")
            except Exception as e:
                print(f"Warning: Could not load controllers file: {e}")

    def _save_controller_list(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "Data", "controllers.json")
        
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        with open(data_path, "w") as f:
            json.dump(list(self.controllers.keys()), f)

    def add_controller(self, name, weights, mins, maxs, stoc_rate, learning_rate=0.01, not_reached_error=100):
        if name in self.controllers:
            raise ValueError(f"Controller with name '{name}' already exists.")
        
        if not isinstance(weights, (list, np.ndarray)):
            raise TypeError("Weights must be a list or numpy array.")
        if not isinstance(mins, (list, np.ndarray)):
            raise TypeError("Mins must be a list or numpy array.")
        if not isinstance(maxs, (list, np.ndarray)):
            raise TypeError("Maxs must be a list or numpy array.")
        
        self.controllers[name] = Controller(
            weights, mins, maxs,
            not_reached_error=not_reached_error,
            filename=name + ".json",
            load=True,
            stoc_rate=stoc_rate,
            learning_rate=learning_rate
        )
        
        self._save_controller_list()
        return True

    def edit_controller(self, name, **kwargs):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        self.controllers[name].edit_controller(**kwargs)
        return True

    def remove_controller(self, name):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        del self.controllers[name]
        self._save_controller_list()
        return True

    def add_frame(self, name, frame):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        self.controllers[name].add_frame(frame)
        return True

    def update(self, name, target_reached):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        self.controllers[name].set_reached(target_reached)
        return True

    def get_weights(self, name):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        return self.controllers[name].get_weights().tolist()

    def tell(self, name, loss, weights=None):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        self.controllers[name].tell(loss, weights)
        return True

    def get_all_controllers(self):
        return list(self.controllers.keys())

    def get_controller_info(self, name):
        if name not in self.controllers:
            raise ValueError(f"Controller '{name}' does not exist.")
        
        controller = self.controllers[name]
        return {
            "name": name,
            "weights": controller.get_weights().tolist(),
            "mins": controller.opt.mins.tolist(),
            "maxs": controller.opt.maxs.tolist(),
            "learning_rate": controller.opt.learning_rate
        }