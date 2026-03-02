#!/usr/bin/env python3
"""
Demo script for the Astrolabe TUI
This creates a sample model and demonstrates the functionality
"""

import json
import os

def create_demo_model():
    """Create a demo model in models.json"""
    models = {}
    
    # Create a demo PID controller model
    models["demo_pid_controller"] = {
        "name": "demo_pid_controller",
        "optimizer_type": "Standard Optimizer",
        "num_params": 3,
        "mins": [0.0, 0.0, 0.0],
        "maxs": [1.0, 1.0, 1.0],
        "learning_rates": [0.0001, 0.0001, 0.0001],
        "initial_weights": [0.5, 0.5, 0.5],
        "current_weights": [0.5, 0.5, 0.5]
    }
    
    # Create a demo momentum controller model
    models["demo_momentum_controller"] = {
        "name": "demo_momentum_controller",
        "optimizer_type": "Standard Optimizer",
        "num_params": 2,
        "mins": [-1.0, 0.0],
        "maxs": [1.0, 2.0],
        "learning_rates": [0.00001, 0.00001],
        "initial_weights": [0.0, 1.0],
        "current_weights": [0.0, 1.0]
    }
    
    with open("models.json", 'w') as f:
        json.dump(models, f, indent=2)
    
    print("✓ Demo models created in models.json")
    print("  - demo_pid_controller (3 parameters)")
    print("  - demo_momentum_controller (2 parameters)")
    print("\nRun 'python3 tui.py' to start the TUI and try these models!")

if __name__ == "__main__":
    if os.path.exists("models.json"):
        response = input("models.json already exists. Overwrite with demo models? (y/n): ").strip().lower()
        if response != 'y':
            print("Demo setup cancelled.")
            exit(0)
    
    create_demo_model()
