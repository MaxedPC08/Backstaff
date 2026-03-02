# Astrolabe RL - Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set up demo models:
```bash
python3 setup_demo.py
```

## Running the Terminal UI

Start the TUI application:
```bash
python3 tui.py
```

## Main Menu

The TUI presents you with these options:

### 1. Add Model
Create a new reinforcement learning model by specifying:
- **Model Name**: A unique identifier for your model
- **Optimizer**: Type of optimizer to use (Standard Optimizer)
- **Number of Parameters**: How many tunable parameters your model has (e.g., 3 for PID controller)
- **Parameter Bounds**: For each parameter, specify minimum and maximum values
- **Learning Rate**: For each parameter, specify how quickly it should be optimized

Example PID Controller:
```
Model name: my_pid_controller
Optimizer: Standard Optimizer
Parameters: 3
Parameter 1: Min=0.0, Max=1.0, LR=0.0001 (Proportional)
Parameter 2: Min=0.0, Max=1.0, LR=0.0001 (Integral)
Parameter 3: Min=0.0, Max=1.0, LR=0.0001 (Derivative)
```

### 2. Remove Model
Delete a model from your collection. You'll be shown a list of available models to choose from.

### 3. Tune Model
Test and optimize a model by:
1. Selecting the model from a list
2. Entering trial values for each parameter
3. Seeing the optimization output

### 4. Edit Model Configuration
Modify an existing model's:
- Minimum parameter bounds
- Maximum parameter bounds
- Learning rates for each parameter

### 5. View All Models
Display a summary of all created models including their parameter counts and optimizer types.

### 6. Exit
Close the application.

## Data Persistence

All models are automatically saved to `models.json` in the project directory. This file persists between sessions, so your models will be available each time you run the TUI.

## Model Structure

Each model is stored with the following information:
```json
{
  "model_name": {
    "name": "model_name",
    "optimizer_type": "Standard Optimizer",
    "num_params": 3,
    "mins": [0.0, 0.0, 0.0],
    "maxs": [1.0, 1.0, 1.0],
    "learning_rates": [0.0001, 0.0001, 0.0001],
    "initial_weights": [0.5, 0.5, 0.5],
    "current_weights": [0.5, 0.5, 0.5]
  }
}
```

## Tips

- Use descriptive model names that reflect their purpose (e.g., `ball_tracking_pid`)
- Start with conservative learning rates and adjust based on results
- Keep parameter bounds realistic to your use case
- Use the Tune Model feature to test your model with different parameters

## Troubleshooting

**No models showing up in menus:**
- Check that `models.json` exists and is valid JSON
- Try running `setup_demo.py` to create sample models

**Getting an error when adding a model:**
- Ensure all numeric inputs are valid numbers
- Minimum value must be less than maximum value
- Learning rates must be positive numbers

## Integration with Astrolabe Core

The TUI manages model configurations which can be used with the Astrolabe reinforcement learning controller in the `Reinforcement/` directory. The model data is stored in a portable JSON format that can be easily integrated with your training pipelines.
