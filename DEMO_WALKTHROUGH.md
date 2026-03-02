# Astrolabe TUI - Walkthrough Demo

This document provides a step-by-step guide to using the Astrolabe Terminal User Interface.

## Starting the TUI

```bash
python3 tui.py
```

You'll see the main menu:

```
============================================================
  Astrolabe RL Model Manager
============================================================

1. Add Model
2. Remove Model
3. Tune Model
4. Edit Model Configuration
5. View All Models
6. Exit

Enter your choice (1-6):
```

## Example 1: Viewing Demo Models

### Step 1: View All Models
```
Enter your choice (1-6): 5
```

Output:
```
============================================================
  All Models
============================================================

1. demo_pid_controller
   Parameters: 3
   Optimizer: Standard Optimizer

2. demo_momentum_controller
   Parameters: 2
   Optimizer: Standard Optimizer
```

## Example 2: Adding a New Model

### Step 1: Choose "Add Model"
```
Enter your choice (1-6): 1
```

### Step 2: Enter Model Name
```
============================================================
  Add New Model
============================================================

Enter model name: my_controller
```

### Step 3: Choose Optimizer
```
Available optimizers:
1. Standard Optimizer
Choose optimizer (1): 1
```

### Step 4: Specify Number of Parameters
```
Enter number of parameters: 3
```

### Step 5: Enter Parameter Bounds and Learning Rates
```
Enter bounds and learning rate for each parameter:

Parameter 1:
  Minimum value: 0.0
  Maximum value: 1.0
  Learning rate: 0.0001

Parameter 2:
  Minimum value: 0.0
  Maximum value: 1.0
  Learning rate: 0.0001

Parameter 3:
  Minimum value: 0.0
  Maximum value: 1.0
  Learning rate: 0.0001

Model 'my_controller' created successfully!
```

## Example 3: Tuning a Model

### Step 1: Choose "Tune Model"
```
Enter your choice (1-6): 3
```

### Step 2: Select Model
```
Available models:
1. demo_pid_controller
2. demo_momentum_controller
3. my_controller
4. Cancel

Select model to tune: 1
```

### Step 3: Enter Parameter Values
```
Tuning model: demo_pid_controller
Number of parameters: 3

Enter value for parameter 1 (range: 0.0 to 1.0): 0.5
Enter value for parameter 2 (range: 0.0 to 1.0): 0.3
Enter value for parameter 3 (range: 0.0 to 1.0): 0.7

Parameters: [0.5, 0.3, 0.7]
Output (Sum of Squares): 0.830000
Model weights updated!
```

## Example 4: Editing Model Configuration

### Step 1: Choose "Edit Model Configuration"
```
Enter your choice (1-6): 4
```

### Step 2: Select Model
```
Available models:
1. demo_pid_controller
2. demo_momentum_controller
3. my_controller
4. Cancel

Select model to edit: 1
```

### Step 3: Choose What to Edit
```
============================================================
  Edit Configuration: demo_pid_controller
============================================================

1. Edit Minimum bounds
2. Edit Maximum bounds
3. Edit Learning rates
4. View Current Configuration
5. Back to Main Menu

Select what to edit (1-5): 1
```

### Step 4: Edit Minimum Bounds
```
Current Minimum values:
  Parameter 1: 0.0
  Parameter 2: 0.0
  Parameter 3: 0.0

Enter new values (or press Enter to skip):
Parameter 1 (Minimum): 
Parameter 2 (Minimum): 0.1
Parameter 3 (Minimum): 

Minimum bounds updated!
```

## Example 5: Removing a Model

### Step 1: Choose "Remove Model"
```
Enter your choice (1-6): 2
```

### Step 2: Select Model to Remove
```
Available models:
1. demo_pid_controller
2. demo_momentum_controller
3. my_controller
4. Cancel

Select model to remove: 3
```

### Step 3: Confirm Deletion
```
Are you sure you want to remove 'my_controller'? (y/n): y
Model 'my_controller' removed successfully!
```

## Tips and Tricks

### Input Validation
- All numeric inputs are validated for correctness
- Parameter values must be within specified bounds
- Learning rates must be positive numbers
- Minimum value must be less than maximum value

### Skipping Fields
When editing bounds or learning rates, press Enter with no input to skip that field:
```
Parameter 1 (Minimum): 
```

### Viewing Configuration
Before editing, you can view the current configuration:
```
Select what to edit (1-5): 4
```

This shows:
- Optimizer type
- Number of parameters
- Parameter bounds for each parameter
- Learning rates for each parameter
- Current weights

### Models Persistence
All models are automatically saved to `models.json`:
- After adding a new model
- After editing a model
- After tuning (weights are updated)
- After removing a model

You can close and reopen the TUI without losing any data!

## Navigation

- Use numbers (1-6 or 1-5) to select menu options
- Press Enter to confirm selections
- Type 'y' or 'n' for yes/no prompts
- Press Ctrl+C to exit at any time

## Common Workflows

### Create and Configure a PID Controller
1. Choose "Add Model"
2. Enter name: "pid_controller"
3. Choose: 1 (Standard Optimizer)
4. Parameters: 3
5. Configure bounds for P, I, D terms
6. Edit learning rates if needed
7. Tune with test values

### Batch Modify Multiple Models
1. Choose "View All Models" to see what you have
2. Choose "Edit Model Configuration"
3. Select first model and modify
4. Repeat for each model

### Test Different Parameter Values
1. Choose "Tune Model"
2. Select your model
3. Try different parameter combinations
4. View the output score
5. The current weights are updated each time

## Troubleshooting

**Issue:** "Model name cannot be empty!"
- Solution: Enter a valid model name (letters, numbers, underscores)

**Issue:** "Value must be between X and Y!"
- Solution: Enter a value within the specified range

**Issue:** "Minimum must be less than maximum!"
- Solution: When editing bounds, ensure min < max

**Issue:** Models not appearing in the list
- Solution: Check that models.json is valid JSON and readable

**Issue:** "Press Enter to continue..." prompts after every action
- Solution: This is normal - it allows you to review the output before returning to the menu
