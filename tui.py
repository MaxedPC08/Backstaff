"""
Terminal User Interface for Astrolabe Reinforcement Learning Controller
"""

import os
import json
import sys
from typing import List, Dict, Any
from pathlib import Path
import numpy as np

from Reinforcement.controller import Controller
from Reinforcement.optimizer import Optimizer


class ModelManager:
    
    def __init__(self):
        self.controllers = {}
        self.models_file = "models.json"
        self._load_controllers()
    
    def _load_controllers(self):
        if os.path.exists(self.models_file):
            try:
                with open(self.models_file, 'r') as f:
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
                                stoc_rates=config.get('stoc_rates', [1.0] * config['num_params']),
                                learning_rate=config['learning_rates'][0] if config['learning_rates'] else 0.01
                            )
                        except Exception as e:
                            print(f"Warning: Could not load controller {name}: {e}")
            except Exception as e:
                print(f"Warning: Could not load models file: {e}")
    
    def _save_models(self):
        models = {}
        for name, controller in self.controllers.items():
            current_weights = controller.get_weights()
            if hasattr(current_weights, "tolist"):
                current_weights = current_weights.tolist()
            models[name] = {
                "name": name,
                "optimizer_type": "Standard Optimizer",
                "num_params": len(controller.opt.mins),
                "mins": controller.opt.mins.tolist(),
                "maxs": controller.opt.maxs.tolist(),
                "learning_rates": [controller.opt.learning_rate] * len(controller.opt.mins),
                "initial_weights": controller.opt.current.tolist(),
                "current_weights": current_weights,
                "stoc_rates": controller.opt.stoc_rates.tolist()
            }
        
        with open(self.models_file, 'w') as f:
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
            stoc_rates=config.get('stoc_rates', [1.0] * config['num_params']),
            learning_rate=config['learning_rates'][0] if config['learning_rates'] else 0.01
        )
        
        self._save_models()
    
    def remove_model(self, name: str) -> bool:
        if name in self.controllers:
            del self.controllers[name]
            self._save_models()
            return True
        return False
    
    def get_model(self, name: str) -> Dict[str, Any]:
        if name not in self.controllers:
            return None
        
        controller = self.controllers[name]
        current_weights = controller.get_weights()
        if hasattr(current_weights, "tolist"):
            current_weights = current_weights.tolist()
        return {
            "name": name,
            "optimizer_type": "Standard Optimizer",
            "num_params": len(controller.opt.mins),
            "mins": controller.opt.mins.tolist(),
            "maxs": controller.opt.maxs.tolist(),
            "learning_rates": [controller.opt.learning_rate] * len(controller.opt.mins),
            "initial_weights": controller.opt.current.tolist(),
            "current_weights": current_weights
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
            
            self._save_models()
            return True
        return False
    
    def model_exists(self, name: str) -> bool:
        return name in self.controllers
    
    def get_controller(self, name: str) -> Controller:
        return self.controllers.get(name)


class TUI:
    """Terminal User Interface for model management"""
    
    def __init__(self):
        self.manager = ModelManager()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60 + "\n")
    
    def main_menu(self):
        """Display main menu"""
        while self.running:
            self.clear_screen()
            self.print_header("Astrolabe RL Model Manager")
            
            print("1. Add Model")
            print("2. Remove Model")
            print("3. Tune Model")
            print("4. Edit Model Configuration")
            print("5. View All Models")
            print("6. Exit")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_model_menu()
            elif choice == '2':
                self.remove_model_menu()
            elif choice == '3':
                self.tune_model_menu()
            elif choice == '4':
                self.edit_config_menu()
            elif choice == '5':
                self.view_models_menu()
            elif choice == '6':
                self.running = False
                print("\nGoodbye!")
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    def add_model_menu(self):
        """Menu to add a new model"""
        self.clear_screen()
        self.print_header("Add New Model")
        
        # Get model name
        name = input("Enter model name: ").strip()
        
        if not name:
            print("Model name cannot be empty!")
            input("Press Enter to continue...")
            return
        
        if self.manager.model_exists(name):
            print(f"Model '{name}' already exists!")
            input("Press Enter to continue...")
            return
        
        # Get optimizer type
        print("\nAvailable optimizers:")
        print("1. Standard Optimizer")
        optimizers = ["Standard Optimizer"]
        optimizer_choice = input("Choose optimizer (1): ").strip()
        optimizer_type = optimizers[int(optimizer_choice) - 1] if optimizer_choice in ['1'] else "Standard Optimizer"
        
        # Get number of parameters
        while True:
            try:
                num_params = int(input("Enter number of parameters: ").strip())
                if num_params <= 0:
                    print("Number of parameters must be positive!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")
        
        # Get parameter bounds and learning rates
        mins = []
        maxs = []
        learning_rates = []
        
        print(f"\nEnter bounds and learning rate for each parameter:")
        for i in range(num_params):
            print(f"\nParameter {i + 1}:")
            
            while True:
                try:
                    min_val = float(input(f"  Minimum value: ").strip())
                    max_val = float(input(f"  Maximum value: ").strip())
                    
                    if min_val >= max_val:
                        print("  Minimum must be less than maximum!")
                        continue
                    break
                except ValueError:
                    print("  Please enter valid numbers!")
            
            while True:
                try:
                    lr = float(input(f"  Learning rate: ").strip())
                    if lr <= 0:
                        print("  Learning rate must be positive!")
                        continue
                    break
                except ValueError:
                    print("  Please enter a valid number!")
            
            mins.append(min_val)
            maxs.append(max_val)
            learning_rates.append(lr)
        
        # Create initial weights (midpoint between min and max)
        initial_weights = [(min_val + max_val) / 2 for min_val, max_val in zip(mins, maxs)]
        
        # Save model configuration
        config = {
            "name": name,
            "optimizer_type": optimizer_type,
            "num_params": num_params,
            "mins": mins,
            "maxs": maxs,
            "learning_rates": learning_rates,
            "initial_weights": initial_weights,
            "current_weights": initial_weights.copy(),
            "stoc_rates": [1.0] * num_params
        }
        
        self.manager.add_model(name, config)
        print(f"\nModel '{name}' created successfully!")
        input("Press Enter to continue...")
    
    def remove_model_menu(self):
        """Menu to remove a model"""
        self.clear_screen()
        self.print_header("Remove Model")
        
        models = self.manager.get_all_models()
        
        if not models:
            print("No models available!")
            input("Press Enter to continue...")
            return
        
        print("Available models:")
        for i, model_name in enumerate(models, 1):
            print(f"{i}. {model_name}")
        print(f"{len(models) + 1}. Cancel")
        
        while True:
            try:
                choice = int(input("\nSelect model to remove: ").strip())
                if 1 <= choice <= len(models):
                    model_to_remove = models[choice - 1]
                    confirm = input(f"Are you sure you want to remove '{model_to_remove}'? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        self.manager.remove_model(model_to_remove)
                        print(f"Model '{model_to_remove}' removed successfully!")
                    else:
                        print("Removal cancelled.")
                    break
                elif choice == len(models) + 1:
                    print("Removal cancelled.")
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")
        
        input("Press Enter to continue...")
    
    def tune_model_menu(self):
        """Menu to tune a model"""
        self.clear_screen()
        self.print_header("Tune Model")
        
        models = self.manager.get_all_models()
        
        if not models:
            print("No models available!")
            input("Press Enter to continue...")
            return
        
        print("Available models:")
        for i, model_name in enumerate(models, 1):
            print(f"{i}. {model_name}")
        print(f"{len(models) + 1}. Cancel")
        
        while True:
            try:
                choice = int(input("\nSelect model to tune: ").strip())
                if 1 <= choice <= len(models):
                    model_name = models[choice - 1]
                    break
                elif choice == len(models) + 1:
                    print("Tuning cancelled.")
                    input("Press Enter to continue...")
                    return
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")
        
        config = self.manager.get_model(model_name)
        num_params = config["num_params"]
        mins = config["mins"]
        maxs = config["maxs"]
        controller = self.manager.get_controller(model_name)
        
        print(f"\nTuning model: {model_name}")
        print(f"Number of parameters: {num_params}\n")
        
        parameters = []
        for i in range(num_params):
            while True:
                try:
                    value = float(input(f"Enter value for parameter {i + 1} (range: {mins[i]} to {maxs[i]}): ").strip())
                    
                    if mins[i] <= value <= maxs[i]:
                        parameters.append(value)
                        break
                    else:
                        print(f"Value must be between {mins[i]} and {maxs[i]}!")
                except ValueError:
                    print("Please enter a valid number!")
        
        try:
            loss = float(np.sum(np.array(parameters) ** 2))
            if controller is not None:
                controller.tell(loss, parameters)
                controller.opt.current = np.array(parameters)
                controller.current = np.array(parameters)
            
            config["current_weights"] = parameters
            self.manager.update_model(model_name, config)
            
            print(f"\nParameters: {parameters}")
            print(f"Output (Sum of Squares): {loss:.6f}")
            print(f"Model weights updated!")
            
        except Exception as e:
            print(f"Error during tuning: {e}")
        
        input("Press Enter to continue...")
    
    def edit_config_menu(self):
        """Menu to edit model configuration"""
        self.clear_screen()
        self.print_header("Edit Model Configuration")
        
        models = self.manager.get_all_models()
        
        if not models:
            print("No models available!")
            input("Press Enter to continue...")
            return
        
        print("Available models:")
        for i, model_name in enumerate(models, 1):
            print(f"{i}. {model_name}")
        print(f"{len(models) + 1}. Cancel")
        
        while True:
            try:
                choice = int(input("\nSelect model to edit: ").strip())
                if 1 <= choice <= len(models):
                    model_name = models[choice - 1]
                    break
                elif choice == len(models) + 1:
                    print("Edit cancelled.")
                    input("Press Enter to continue...")
                    return
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number!")
        
        config = self.manager.get_model(model_name)
        
        while True:
            self.clear_screen()
            self.print_header(f"Edit Configuration: {model_name}")
            
            print(f"1. Edit Minimum bounds")
            print(f"2. Edit Maximum bounds")
            print(f"3. Edit Learning rates")
            print(f"4. View Current Configuration")
            print(f"5. Back to Main Menu")
            
            edit_choice = input("\nSelect what to edit (1-5): ").strip()
            
            if edit_choice == '1':
                self.edit_parameter_bounds(config, "mins", "Minimum")
            elif edit_choice == '2':
                self.edit_parameter_bounds(config, "maxs", "Maximum")
            elif edit_choice == '3':
                self.edit_learning_rates(config)
            elif edit_choice == '4':
                self.view_configuration(config)
            elif edit_choice == '5':
                break
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
        
        self.manager.update_model(model_name, config)
    
    def edit_parameter_bounds(self, config: Dict, key: str, label: str):
        """Edit parameter bounds (mins or maxs)"""
        self.clear_screen()
        self.print_header(f"Edit {label} Bounds")
        
        num_params = config["num_params"]
        bounds = config[key]
        
        print(f"Current {label} values:")
        for i, val in enumerate(bounds):
            print(f"  Parameter {i + 1}: {val}")
        
        print(f"\nEnter new values (or press Enter to skip):")
        for i in range(num_params):
            while True:
                user_input = input(f"Parameter {i + 1} ({label}): ").strip()
                if user_input == "":
                    break
                try:
                    new_val = float(user_input)
                    bounds[i] = new_val
                    break
                except ValueError:
                    print("Please enter a valid number!")
        
        print(f"{label} bounds updated!")
        input("Press Enter to continue...")
    
    def edit_learning_rates(self, config: Dict):
        """Edit learning rates"""
        self.clear_screen()
        self.print_header("Edit Learning Rates")
        
        num_params = config["num_params"]
        learning_rates = config["learning_rates"]
        
        print(f"Current learning rates:")
        for i, lr in enumerate(learning_rates):
            print(f"  Parameter {i + 1}: {lr}")
        
        print(f"\nEnter new values (or press Enter to skip):")
        for i in range(num_params):
            while True:
                user_input = input(f"Parameter {i + 1}: ").strip()
                if user_input == "":
                    break
                try:
                    new_lr = float(user_input)
                    if new_lr <= 0:
                        print("Learning rate must be positive!")
                        continue
                    learning_rates[i] = new_lr
                    break
                except ValueError:
                    print("Please enter a valid number!")
        
        print(f"Learning rates updated!")
        input("Press Enter to continue...")
    
    def view_configuration(self, config: Dict):
        """View current model configuration"""
        self.clear_screen()
        self.print_header(f"Configuration: {config['name']}")
        
        print(f"Optimizer Type: {config['optimizer_type']}")
        print(f"Number of Parameters: {config['num_params']}\n")
        
        print("Parameter Bounds:")
        for i in range(config['num_params']):
            print(f"  Parameter {i + 1}: [{config['mins'][i]}, {config['maxs'][i]}]")
        
        print("\nLearning Rates:")
        for i, lr in enumerate(config['learning_rates']):
            print(f"  Parameter {i + 1}: {lr}")
        
        print("\nCurrent Weights:")
        for i, w in enumerate(config['current_weights']):
            print(f"  Parameter {i + 1}: {w}")
        
        input("Press Enter to continue...")
    
    def view_models_menu(self):
        """View all models"""
        self.clear_screen()
        self.print_header("All Models")
        
        models = self.manager.get_all_models()
        
        if not models:
            print("No models available!")
        else:
            for i, model_name in enumerate(models, 1):
                config = self.manager.get_model(model_name)
                print(f"{i}. {model_name}")
                print(f"   Parameters: {config['num_params']}")
                print(f"   Optimizer: {config['optimizer_type']}\n")
        
        input("Press Enter to continue...")
    
    def run(self):
        """Run the TUI"""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            self.running = False


if __name__ == "__main__":
    tui = TUI()
    tui.run()
