# Backstaff

**Reinforcement learning-powered motion control tuning for FRC robots.**

Backstaff is a desktop application that helps robotics teams optimize PID controllers and motion parameters using reinforcement learning. Instead of manually tweaking parameters through trial and error, Backstaff learns optimal settings by analyzing your robot's performance data. Built with PyQt5 for a clean, responsive interface with dark mode support.

---

## Features

- **RL-Based Optimization**: Automatically tune PID gains (P, I, D, FF) using reinforcement learning algorithms
- **Visual Model Management**: Create, edit, and manage multiple controller configurations through an intuitive GUI
- **Performance Tracking**: Track optimization history and visualize parameter evolution over time
- **Flexible Configuration**: Set custom bounds, learning rates, and stochastic rates per parameter
- **Dark Mode**: Professional dark/light theme support for extended tuning sessions
- **Data Persistence**: All models and training history automatically saved to disk

---

## Quick Start

### (Recommended) Download a released version at https://github.com/MaxedPC08/Backstaff/releases/tag/V0.1

### To run the python code:
#### 1. Setup Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Launch Application
```bash
python main.py
```

#### 3. Create Your First Model
1. Click "Add Model" in the sidebar
2. Configure parameter names (e.g., P, I, D, FF)
3. Set bounds and learning rates
4. Start tuning!

---

## Architecture

### Backend (Reinforcement Learning)
- **[Reinforcement/optimizer.py](Reinforcement/optimizer.py)**: Core gradient-free optimizer with configurable learning rates and parameter constraints
- **[Reinforcement/controller.py](Reinforcement/controller.py)**: Controller wrapper that evaluates robot motion by analyzing position, velocity, and acceleration data
- **[Reinforcement/controller_manager.py](Reinforcement/controller_manager.py)**: Manages multiple controller instances
- **[Reinforcement/demos/](Reinforcement/demos)**: Example implementations
  - `pid.py`: Standard PID controller
  - `rl_pid.py`: RL-enhanced PID tuner
  - `1d_momentum_sim.py`: Motion simulation framework

### Frontend (PyQt5 UI)
- **[ui/main_window.py](ui/main_window.py)**: Main application window with split-pane layout
- **[ui/main_content.py](ui/main_content.py)**: Central content area for parameter visualization and control
- **[ui/model_manager.py](ui/model_manager.py)**: Backend logic for model CRUD operations and controller instantiation
- **[ui/widgets.py](ui/widgets.py)**: Custom widgets including controller list and parameter displays
- **[ui/dialogs.py](ui/dialogs.py)**: Modal dialogs for adding/editing models and application settings
- **[ui/settings_manager.py](ui/settings_manager.py)**: Persistent settings management
- **[ui/styles.py](ui/styles.py)**: Theme and stylesheet management

### Data Management
- **Models**: [backstaff_data/models.json](backstaff_data/models.json) stores all model configurations
- **History**: Individual `*_history.json` files track optimization progress per model
- **Notes**: User annotations saved in `*_notes.json` files
- **Settings**: [backstaff_settings.json](backstaff_settings.json) stores UI preferences

---

## How It Works

### The Optimization Loop

1. **Define Model**: Create a model with N parameters (e.g., P, I, D, FF gains) and set bounds
2. **Collect Data**: Run your robot and collect frame data (position, velocity, time)
3. **Evaluate Performance**: Backstaff computes error metrics based on:
   - Distance traveled vs. optimal path
   - Speed consistency (penalizes jerky motion)
   - Target achievement
4. **Update Weights**: RL optimizer adjusts parameters to minimize error
5. **Iterate**: Repeat until performance converges

---

## Configuration

### Model Structure
Each model in [backstaff_data/models.json](backstaff_data/models.json) contains:
```json
{
  "name": "shooterpid",
  "optimizer_type": "Standard Optimizer",
  "num_params": 4,
  "param_names": ["P", "I", "D", "FF"],
  "mins": [0.0, 0.0, 0.0, 0.0],
  "maxs": [1.0, 1.0, 1.0, 1.0],
  "learning_rates": [0.0001, 0.0001, 0.0001, 0.0001],
  "initial_weights": [0.5, 0.0, 0.1, 0.2]
}
```

### Application Settings
Configure in [backstaff_settings.json](backstaff_settings.json):
```json
{
  "data_folder": "/path/to/backstaff_data",
  "dark_mode": true
}
```

---

## Building Executable

A build script and spec file are included for creating standalone executables:

```bash
./build.sh
```

Output will be in `dist/Backstaff/`

---

## Development

### Project Structure
```
Backstaff/
├── main.py                      # Application entry point
├── Reinforcement/               # RL backend
│   ├── optimizer.py            # Core optimization engine
│   ├── controller.py           # Controller logic
│   ├── controller_manager.py   # Multi-controller management
│   └── demos/                  # Example implementations
├── ui/                         # PyQt5 frontend
│   ├── main_window.py         # Main application window
│   ├── model_manager.py       # Model CRUD backend
│   ├── dialogs.py             # UI dialogs
│   └── widgets.py             # Custom components
├── backstaff_data/            # Persistent storage
│   ├── models.json           # Model configurations
│   └── *_history.json        # Training history
└── requirements.txt          # Python dependencies
```

### Dependencies
- **PyQt5** (≥5.15.0): Cross-platform GUI framework
- **NumPy** (≥1.21.0): Numerical computing and optimization

### Testing
Add your own test suite as needed. Consider testing:
- Optimizer convergence on known functions
- Model save/load integrity
- UI state management

---

## Troubleshooting

**Application won't start**
- Ensure virtual environment is activated
- Verify PyQt5 installation: `pip list | grep PyQt5`
- Check Python version (3.8+ recommended)

**Models not saving**
- Check write permissions on `backstaff_data/` directory
- Verify `data_folder` path in settings file

**Dark mode not applying**
- Toggle in Settings dialog (gear icon)
- Check [backstaff_settings.json](backstaff_settings.json) for `"dark_mode": true`

---

## License

See [LICENSE](LICENSE) for details.

---

## Contributing

This is a robotics team tool designed for FRC competition preparation. Contributions welcome - especially around:
- Additional optimizer algorithms
- Real-time robot integration examples
- Performance visualization improvements
- Multi-objective optimization support
