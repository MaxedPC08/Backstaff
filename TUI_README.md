# Astrolabe RL TUI - Terminal User Interface

A comprehensive terminal user interface for managing and tuning Astrolabe Reinforcement Learning models.

## Features

- **Add Model**: Create new models with custom optimizers, parameters, bounds, and learning rates
- **Remove Model**: Delete models from your collection with confirmation
- **Tune Model**: Input parameter values and get optimization output
- **Edit Configuration**: Modify existing model configurations (bounds, learning rates)
- **View Models**: Display all created models and their specifications

## Usage

Run the TUI with:
```bash
python3 tui.py
```

## Main Menu Options

1. **Add Model** - Create a new model by specifying:
   - Model name
   - Optimizer type
   - Number of parameters
   - Minimum/maximum bounds for each parameter
   - Learning rate for each parameter

2. **Remove Model** - Select and delete a model from a dropdown menu

3. **Tune Model** - Choose a model and input parameter values to get an output number

4. **Edit Model Configuration** - Modify:
   - Minimum bounds
   - Maximum bounds
   - Learning rates

5. **View All Models** - Display a list of all created models with basic info

6. **Exit** - Close the application

## Model Storage

All models are stored in `models.json` in the project root directory. Each model contains:
- Model name
- Optimizer type
- Number of parameters
- Min/max bounds for each parameter
- Learning rates for each parameter
- Initial and current weights

## Data Persistence

Models are automatically saved to `models.json` when created or modified. They will be loaded automatically when you run the TUI again.
