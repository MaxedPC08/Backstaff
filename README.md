# Astrolabe

Reinforcement-learning-powered motion control tools for FRC robots, with a PyQt desktop UI for managing controllers and tuning parameters.

## What’s here (current tree)
- PyQt desktop app: [main.py](main.py)
- Core control/optimization: [Reinforcement/controller.py](Reinforcement/controller.py), [Reinforcement/optimizer.py](Reinforcement/optimizer.py)
- Example RL demos: [Reinforcement/demos](Reinforcement/demos)
- Virtual env placeholder: [venv](venv/) (create/activate your own)
- Data folder (empty by default): [astrolabe_data](astrolabe_data)

> Note: There is no terminal TUI script or seed models JSON in this workspace snapshot. If you expected `tui.py` or `models.json`, add them before running.

## Quick start
1) Python env
- `python3 -m venv venv && source venv/bin/activate`
- `python -m pip install -r requirements.txt`

2) Run the desktop UI
- `python main.py`

3) Data locations
- Models/history: stored under [astrolabe_data](astrolabe_data) when created by the app

## Usage notes
- Model configs and history are created on demand in [astrolabe_data](astrolabe_data).
- The optimizer backend expects numeric bounds and learning rates per parameter.

## Repo layout (high level)
- [main.py](main.py): PyQt desktop app
- [Reinforcement/controller.py](Reinforcement/controller.py), [Reinforcement/optimizer.py](Reinforcement/optimizer.py): core RL control/optimization
- [Reinforcement/demos](Reinforcement/demos): minimal demo scripts
- [requirements.txt](requirements.txt): Python deps (includes PyQt5 and numpy)

## Development
- Tests are not included in this snapshot; add your own as needed.
- If you adjust dependencies, keep [requirements.txt](requirements.txt) in sync.

## Troubleshooting
- UI will not start: ensure PyQt5 is installed from [requirements.txt](requirements.txt) and that you are using the virtual environment.
- Missing expected files (e.g., `tui.py`, `models.json`): they are not present in this repo snapshot; add or restore them before use.
