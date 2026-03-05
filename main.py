"""
Qt GUI Application for Astrolabe Reinforcement Learning Controller
"""

import os
import json
import sys
from typing import List, Dict, Any
from pathlib import Path
import numpy as np
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem, QDialog, QMessageBox,
    QListWidget, QListWidgetItem, QTabWidget, QInputDialog, QScrollArea,
    QFormLayout, QGroupBox, QHeaderView, QProgressBar, QStatusBar,
    QFileDialog, QCheckBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QBrush

from Reinforcement.controller import Controller
from Reinforcement.optimizer import Optimizer


# Settings management
class Settings:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.default_data_folder = os.path.join(base_dir, "astrolabe_data")
        self.settings_file = os.path.join(base_dir, "astrolabe_settings.json")
        self.default_settings = {
            "data_folder": self.default_data_folder,
            "dark_mode": False
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        os.makedirs(os.path.dirname(self.settings_file) or ".", exist_ok=True)
        legacy_data_path = os.path.join(self.default_data_folder, "astrolabe_settings.json")
        legacy_root_path = "astrolabe_settings.json"
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
        os.makedirs(os.path.dirname(self.settings_file) or ".", exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()


def get_stylesheet(dark_mode=False):
    """Return modern stylesheet for the application"""
    if dark_mode:
        return """
        QMainWindow {
            background-color: #1e1e1e;
        }
        
        QWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        
        QLabel {
            color: #e0e0e0;
        }
        
        QLineEdit, QSpinBox, QDoubleSpinBox {
            background-color: #2d2d2d;
            border: 1px solid #444444;
            border-radius: 4px;
            padding: 5px;
            color: #e0e0e0;
            selection-background-color: #4CAF50;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #4CAF50;
            outline: none;
        }
        
        QPushButton {
            background-color: #4a4a4a;
            color: white;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 11px;
        }
        
        QPushButton:hover {
            background-color: #555555;
            border: 1px solid #666666;
        }
        
        QPushButton:pressed {
            background-color: #3a3a3a;
        }
        
        QPushButton#deleteBtn {
            background-color: #6b3b3b;
        }
        
        QPushButton#deleteBtn:hover {
            background-color: #7a4a4a;
        }
        
        QPushButton#deleteBtn:pressed {
            background-color: #5a2a2a;
        }
        
        QPushButton#cancelBtn {
            background-color: #555555;
        }
        
        QPushButton#cancelBtn:hover {
            background-color: #666666;
        }
        
        QTableWidget {
            background-color: #2d2d2d;
            alternate-background-color: #252525;
            gridline-color: #444444;
            border: 1px solid #444444;
            border-radius: 4px;
            color: #e0e0e0;
        }
        
        QTableWidget::item {
            padding: 5px;
            color: #e0e0e0;
        }
        
        QTableWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #1a1a1a;
            color: #e0e0e0;
            padding: 5px;
            border: none;
            font-weight: bold;
        }
        
        QGroupBox {
            color: #e0e0e0;
            border: 2px solid #444444;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        
        QTabWidget::pane {
            border: 1px solid #444444;
            background-color: #1e1e1e;
        }
        
        QTabBar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #e0e0e0;
            padding: 10px 30px;
            margin-right: 2px;
            border-radius: 4px 4px 0 0;
            font-weight: bold;
            min-width: 120px;
        }
        
        QTabBar::tab:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QScrollArea {
            background-color: #2d2d2d;
            border: 1px solid #444444;
            border-radius: 4px;
        }
        
        QStatusBar {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        
        QListWidget {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: 1px solid #444444;
            border-radius: 4px;
        }
        
        QCheckBox {
            color: #e0e0e0;
        }
    """
    else:
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QWidget {
            background-color: #f5f5f5;
            color: #333333;
        }
        
        QLabel {
            color: #333333;
        }
        
        QLineEdit, QSpinBox, QDoubleSpinBox {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            color: #333333;
            selection-background-color: #4CAF50;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #4CAF50;
            outline: none;
        }
        
        QPushButton {
            background-color: #cccccc;
            color: #333333;
            border: 1px solid #999999;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 11px;
        }
        
        QPushButton:hover {
            background-color: #dddddd;
            border: 1px solid #888888;
        }
        
        QPushButton:pressed {
            background-color: #bbbbbb;
        }
        
        QPushButton#deleteBtn {
            background-color: #d9b3b3;
        }
        
        QPushButton#deleteBtn:hover {
            background-color: #e6cccc;
        }
        
        QPushButton#deleteBtn:pressed {
            background-color: #cc9999;
        }
        
        QPushButton#cancelBtn {
            background-color: #cccccc;
        }
        
        QPushButton#cancelBtn:hover {
            background-color: #616161;
        }
        
        QTableWidget {
            background-color: white;
            alternate-background-color: #f9f9f9;
            gridline-color: #e0e0e0;
            border: 1px solid #cccccc;
            border-radius: 4px;
            color: #333333;
        }
        
        QTableWidget::item {
            padding: 5px;
            color: #333333;
        }
        
        QTableWidget::item:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #424242;
            color: white;
            padding: 5px;
            border: none;
            font-weight: bold;
        }
        
        QGroupBox {
            color: #333333;
            border: 2px solid #cccccc;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        
        QTabWidget::pane {
            border: 1px solid #cccccc;
            background-color: #f5f5f5;
        }
        
        QTabBar {
            alignment: left;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            color: #333333;
            padding: 10px 30px;
            margin-right: 2px;
            border-radius: 4px 4px 0 0;
            font-weight: bold;
            min-width: 120px;
        }
        
        QTabBar::tab:selected {
            background-color: #4CAF50;
            color: white;
        }
        
        QScrollArea {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        
        QStatusBar {
            background-color: #424242;
            color: white;
        }
        
        QListWidget {
            background-color: white;
            color: #333333;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        
        QCheckBox {
            color: #333333;
        }
    """


class ModelManager:
    """Model management backend (same as TUI)"""
    
    def __init__(self, settings: Settings):
        self.controllers = {}
        self.model_configs = {}  # Store full config including metadata
        self.settings = settings
        os.makedirs(self.settings.get("data_folder", "./astrolabe_data"), exist_ok=True)
        self._load_controllers()

    def _models_path(self) -> str:
        data_folder = self.settings.get("data_folder", "./astrolabe_data")
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
                                stoc_rates=config.get('stoc_rates', [1.0] * config['num_params']),
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
            stoc_rates=config.get('stoc_rates', [1.0] * config['num_params']),
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


class AddModelDialog(QDialog):
    """Dialog for adding a new model"""
    
    def __init__(self, manager: ModelManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.config = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Add New Model")
        self.setGeometry(100, 100, 650, 750)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Create New Model")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Info text
        layout.addWidget(QLabel("Configure your model parameters below:"))
        layout.addWidget(QLabel(""))
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Model name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter a unique model name")
        self.name_input.setMinimumHeight(35)
        form_layout.addRow("Model Name:", self.name_input)
        
        # Number of parameters
        self.num_params_spin = QSpinBox()
        self.num_params_spin.setMinimum(1)
        self.num_params_spin.setMaximum(50)
        self.num_params_spin.setValue(3)
        self.num_params_spin.setMinimumHeight(35)
        self.num_params_spin.valueChanged.connect(self.update_parameter_fields)
        form_layout.addRow("Number of Parameters:", self.num_params_spin)
        
        layout.addLayout(form_layout)
        layout.addWidget(QLabel(""))
        
        # Scrollable parameter section
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.params_layout = QVBoxLayout()
        self.params_layout.setSpacing(15)
        
        self.param_fields = []
        self.update_parameter_fields()
        
        scroll_widget.setLayout(self.params_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(QLabel("Parameter Configuration:"))
        layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        create_btn = QPushButton("✓ Create Model")
        create_btn.setMinimumHeight(40)
        create_btn.setMinimumWidth(120)
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setMinimumWidth(120)
        
        create_btn.clicked.connect(self.create_model)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def update_parameter_fields(self):
        """Update parameter fields based on number of parameters"""
        # Clear existing fields
        while self.params_layout.count():
            self.params_layout.takeAt(0).widget().deleteLater()
        
        self.param_fields = []
        num_params = self.num_params_spin.value()
        
        for i in range(num_params):
            group = QGroupBox(f"Parameter {i + 1}")
            group_layout = QFormLayout()
            group_layout.setSpacing(8)
            
            name_input = QLineEdit()
            name_input.setPlaceholderText(f"e.g., param_{i+1}")
            name_input.setMinimumHeight(30)
            name_input.setToolTip("Name for this parameter (used in loss functions)")
            
            min_spin = QDoubleSpinBox()
            min_spin.setRange(-10000, 10000)
            min_spin.setValue(-1.0)
            min_spin.setMinimumHeight(30)
            min_spin.setToolTip("Minimum boundary value for this parameter")
            
            max_spin = QDoubleSpinBox()
            max_spin.setRange(-10000, 10000)
            max_spin.setValue(1.0)
            max_spin.setMinimumHeight(30)
            max_spin.setToolTip("Maximum boundary value for this parameter")
            
            lr_spin = QDoubleSpinBox()
            lr_spin.setRange(0.0001, 100)
            lr_spin.setValue(0.01)
            lr_spin.setSingleStep(0.01)
            lr_spin.setMinimumHeight(30)
            lr_spin.setToolTip("Learning rate for optimization")
            
            group_layout.addRow("Parameter Name:", name_input)
            group_layout.addRow("Min Value:", min_spin)
            group_layout.addRow("Max Value:", max_spin)
            group_layout.addRow("Learning Rate:", lr_spin)
            
            group.setLayout(group_layout)
            self.params_layout.addWidget(group)
            
            self.param_fields.append({
                'name': name_input,
                'min': min_spin,
                'max': max_spin,
                'lr': lr_spin
            })
    
    def create_model(self):
        """Create the model with current settings"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Validation Error", 
                "⚠ Model name cannot be empty!")
            return
        
        if self.manager.model_exists(name):
            QMessageBox.warning(self, "Duplicate Model", 
                f"⚠ Model '{name}' already exists!")
            return
        
        mins = []
        maxs = []
        learning_rates = []
        param_names = []
        
        for i, field in enumerate(self.param_fields):
            param_name = field['name'].text().strip()
            if not param_name:
                param_name = f"param_{i+1}"
            
            min_val = field['min'].value()
            max_val = field['max'].value()
            lr_val = field['lr'].value()
            
            if min_val >= max_val:
                QMessageBox.warning(self, "Validation Error", 
                    f"⚠ Parameter {i+1}: Minimum must be less than Maximum!")
                return
            
            if lr_val <= 0:
                QMessageBox.warning(self, "Validation Error", 
                    f"⚠ Parameter {i+1}: Learning rate must be positive!")
                return
            
            param_names.append(param_name)
            mins.append(min_val)
            maxs.append(max_val)
            learning_rates.append(lr_val)
        
        initial_weights = [(mn + mx) / 2 for mn, mx in zip(mins, maxs)]
        
        config = {
            "name": name,
            "optimizer_type": "Standard Optimizer",
            "num_params": len(mins),
            "param_names": param_names,
            "mins": mins,
            "maxs": maxs,
            "learning_rates": learning_rates,
            "initial_weights": initial_weights,
            "current_weights": initial_weights.copy(),
            "stoc_rates": [1.0] * len(mins),
            "loss_function": "",
            "custom_param_names": []
        }
        
        try:
            self.manager.add_model(name, config)
            QMessageBox.information(self, "Success", 
                f"✓ Model '{name}' created successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"✗ Failed to create model:\n{e}")


class TuneModelDialog(QDialog):
    """Dialog for tuning a model"""
    
    def __init__(self, manager: ModelManager, model_name: str, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.model_name = model_name
        self.config = manager.get_model(model_name)
        self.param_inputs = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Tune Model: {self.model_name}")
        self.setGeometry(100, 100, 600, 700)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Tune Model: {self.model_name}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addWidget(QLabel(f"Number of parameters: {self.config['num_params']}"))
        layout.addWidget(QLabel("Enter values for each parameter:"))
        layout.addWidget(QLabel(""))
        
        # Scrollable parameter section
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        params_layout = QVBoxLayout()
        params_layout.setSpacing(10)
        
        for i in range(self.config['num_params']):
            min_val = self.config['mins'][i]
            max_val = self.config['maxs'][i]
            current_val = self.config['current_weights'][i]
            
            group = QGroupBox(f"Parameter {i + 1}")
            group_layout = QFormLayout()
            
            range_label = QLabel(f"Range: {min_val:.4f} to {max_val:.4f}")
            range_label.setStyleSheet("color: #666666; font-size: 10px;")
            group_layout.addRow(range_label)
            
            spin = QDoubleSpinBox()
            spin.setRange(min_val, max_val)
            spin.setValue(current_val)
            spin.setSingleStep((max_val - min_val) / 100)
            spin.setMinimumHeight(35)
            spin.setToolTip(f"Enter value between {min_val:.4f} and {max_val:.4f}")
            
            group_layout.addRow("Value:", spin)
            group.setLayout(group_layout)
            params_layout.addWidget(group)
            self.param_inputs.append(spin)
        
        scroll_widget.setLayout(params_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Result section
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("background-color: #e8f5e9; padding: 10px; border-radius: 4px; color: #2e7d32;")
        self.result_label.setVisible(False)
        layout.addWidget(self.result_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        tune_btn = QPushButton("▶ Tune & Update")
        tune_btn.setMinimumHeight(40)
        tune_btn.setMinimumWidth(120)
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setMinimumWidth(120)
        
        tune_btn.clicked.connect(self.tune_model)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(tune_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def tune_model(self):
        """Tune the model with entered values"""
        parameters = [spin.value() for spin in self.param_inputs]
        
        try:
            loss = float(np.sum(np.array(parameters) ** 2))
            controller = self.manager.get_controller(self.model_name)
            
            if controller is not None:
                controller.tell(loss, parameters)
                controller.opt.current = np.array(parameters)
                controller.current = np.array(parameters)
            
            config = self.manager.get_model(self.model_name)
            config["current_weights"] = parameters
            self.manager.update_model(self.model_name, config)
            
            result_text = "✓ Model updated successfully!\n\n"
            result_text += "Parameters: " + ", ".join([f"{p:.6f}" for p in parameters]) + "\n"
            result_text += f"Output (Sum of Squares): {loss:.6f}"
            
            self.result_label.setText(result_text)
            self.result_label.setVisible(True)
            
            QMessageBox.information(self, "Success", 
                "✓ Model tuned and weights updated successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"✗ Error during tuning:\n{e}")


class EditConfigDialog(QDialog):
    """Dialog for editing model configuration"""
    
    def __init__(self, manager: ModelManager, model_name: str, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.model_name = model_name
        self.config = manager.get_model(model_name)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"Edit Configuration: {self.model_name}")
        self.setGeometry(100, 100, 700, 750)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Edit Model: {self.model_name}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addWidget(QLabel(""))
        
        # Create tabs for different edit options
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab { padding: 10px 20px; }
        """)
        
        # Tab 1: Edit minimums
        min_widget = self.create_bounds_tab("Minimum Bounds", "mins")
        tabs.addTab(min_widget, "🔽 Min Bounds")
        
        # Tab 2: Edit maximums
        max_widget = self.create_bounds_tab("Maximum Bounds", "maxs")
        tabs.addTab(max_widget, "🔼 Max Bounds")
        
        # Tab 3: Edit learning rates
        lr_widget = self.create_learning_rates_tab()
        tabs.addTab(lr_widget, "📈 Learning Rates")
        
        # Tab 4: View configuration
        view_widget = self.create_view_tab()
        tabs.addTab(view_widget, "👁 View Config")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        save_btn = QPushButton("✓ Save Changes")
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(120)
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.setMinimumWidth(120)
        
        save_btn.clicked.connect(self.save_changes)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_bounds_tab(self, title: str, key: str):
        """Create a tab for editing bounds"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel(f"Edit {title}:")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        layout.addWidget(QLabel(""))
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.bound_inputs = []
        bounds = self.config[key]
        
        for i, val in enumerate(bounds):
            spin = QDoubleSpinBox()
            spin.setRange(-100000, 100000)
            spin.setValue(val)
            spin.setMinimumHeight(35)
            spin.setToolTip(f"Set the {key.rstrip('s')} value for parameter {i+1}")
            form_layout.addRow(f"Parameter {i + 1}:", spin)
            self.bound_inputs.append((key, i, spin))
        
        layout.addLayout(form_layout)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_learning_rates_tab(self):
        """Create a tab for editing learning rates"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel("Edit Learning Rates:")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        layout.addWidget(QLabel("Higher values = faster learning, lower values = more stable"))
        layout.addWidget(QLabel(""))
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.lr_inputs = []
        learning_rates = self.config['learning_rates']
        
        for i, lr in enumerate(learning_rates):
            spin = QDoubleSpinBox()
            spin.setRange(0.0001, 100)
            spin.setValue(lr)
            spin.setSingleStep(0.01)
            spin.setMinimumHeight(35)
            spin.setToolTip(f"Learning rate for parameter {i+1}")
            form_layout.addRow(f"Parameter {i + 1}:", spin)
            self.lr_inputs.append(spin)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_view_tab(self):
        """Create a tab for viewing configuration"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Create a nice formatted view
        text = f"<b>Model:</b> {self.config['name']}<br>"
        text += f"<b>Optimizer:</b> {self.config['optimizer_type']}<br>"
        text += f"<b>Parameters:</b> {self.config['num_params']}<br><br>"
        
        text += "<b>Parameter Bounds:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i in range(self.config['num_params']):
            text += f"<tr><td>Parameter {i+1}:</td><td style='padding-left: 20px;'>"
            text += f"[{self.config['mins'][i]:.6f}, {self.config['maxs'][i]:.6f}]</td></tr>"
        text += "</table><br>"
        
        text += "<b>Learning Rates:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i, lr in enumerate(self.config['learning_rates']):
            text += f"<tr><td>Parameter {i+1}:</td><td style='padding-left: 20px;'>{lr:.8f}</td></tr>"
        text += "</table><br>"
        
        text += "<b>Current Weights:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i, w in enumerate(self.config['current_weights']):
            text += f"<tr><td>Parameter {i+1}:</td><td style='padding-left: 20px;'>{w:.8f}</td></tr>"
        text += "</table>"
        
        label = QLabel(text)
        label.setTextFormat(Qt.RichText)
        layout.addWidget(label)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def save_changes(self):
        """Save configuration changes"""
        try:
            # Update bounds
            for key, i, spin in self.bound_inputs:
                self.config[key][i] = spin.value()
            
            # Update learning rates
            for i, spin in enumerate(self.lr_inputs):
                self.config['learning_rates'][i] = spin.value()
            
            # Validate bounds
            for i in range(self.config['num_params']):
                if self.config['mins'][i] >= self.config['maxs'][i]:
                    QMessageBox.warning(self, "Validation Error", 
                        f"⚠ Parameter {i+1}: Min must be less than Max!")
                    return
            
            self.manager.update_model(self.model_name, self.config)
            QMessageBox.information(self, "Success", 
                "✓ Configuration updated successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"✗ Failed to save configuration:\n{e}")


class ControllerListWidget(QWidget):
    """Left sidebar widget for controller selection and management"""
    
    def __init__(self, manager: ModelManager, on_selection_changed=None, dark_mode=False, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.on_selection_changed = on_selection_changed
        self.dark_mode = dark_mode
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Controllers")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        if self.dark_mode:
            title.setStyleSheet("color: #e0e0e0;")
        else:
            title.setStyleSheet("color: #333333;")
        layout.addWidget(title)
        
        # Controller list
        self.list_widget = QListWidget()
        if self.dark_mode:
            self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #444444;
                    border-radius: 4px;
                    color: #e0e0e0;
                }
                QListWidget::item {
                    padding: 8px;
                    color: #e0e0e0;
                }
                QListWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
        else:
            self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    color: #333333;
                }
                QListWidget::item {
                    padding: 8px;
                    color: #333333;
                }
                QListWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
        self.list_widget.itemSelectionChanged.connect(self.on_item_selected)
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        
        add_btn = QPushButton("➕ Add")
        add_btn.setMinimumHeight(35)
        add_btn.setToolTip("Create a new controller")
        
        remove_btn = QPushButton("🗑 Remove")
        remove_btn.setObjectName("deleteBtn")
        remove_btn.setMinimumHeight(35)
        remove_btn.setToolTip("Delete selected controller")
        
        add_btn.clicked.connect(self.add_controller)
        remove_btn.clicked.connect(self.remove_controller)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(remove_btn)
        layout.addLayout(button_layout)
        
        self.add_btn = add_btn
        self.remove_btn = remove_btn
        
        self.setLayout(layout)
        self.refresh_list()
    
    def refresh_list(self):
        """Refresh the controller list"""
        self.list_widget.clear()
        models = self.manager.get_all_models()
        
        for model_name in models:
            config = self.manager.get_model(model_name)
            item_text = f"{model_name}\n({config['num_params']} params)"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, model_name)
            self.list_widget.addItem(item)
        
        if models:
            self.list_widget.setCurrentRow(0)
    
    def on_item_selected(self):
        """Handle controller selection"""
        current_item = self.list_widget.currentItem()
        if current_item and self.on_selection_changed:
            model_name = current_item.data(Qt.UserRole)
            self.on_selection_changed(model_name)
    
    def add_controller(self):
        """Emit signal to add controller"""
        # Will be handled by parent
        pass
    
    def remove_controller(self):
        """Emit signal to remove controller"""
        # Will be handled by parent
        pass
    
    def get_selected(self):
        """Get currently selected controller name"""
        current_item = self.list_widget.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
    
    def update_styling(self):
        """Update styling for dark/light mode"""
        # Find and update the title label
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.text() == "Controllers":
                if self.dark_mode:
                    widget.setStyleSheet("color: #e0e0e0;")
                else:
                    widget.setStyleSheet("color: #333333;")
        
        # Update list widget styling
        if self.dark_mode:
            self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #444444;
                    border-radius: 4px;
                    color: #e0e0e0;
                }
                QListWidget::item {
                    padding: 8px;
                    color: #e0e0e0;
                }
                QListWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
        else:
            self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    color: #333333;
                }
                QListWidget::item {
                    padding: 8px;
                    color: #333333;
                }
                QListWidget::item:selected {
                    background-color: #4CAF50;
                    color: white;
                }
            """)


class MainContentWidget(QWidget):
    """Main content panel for model details and tuning"""
    
    def __init__(self, manager: ModelManager, settings: Settings, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.settings = settings
        self.current_model = None
        self.history_data = []
        self.param_inputs = []
        self.init_ui()
    
    def get_history_file(self):
        """Get the history file path for the current model"""
        if not self.current_model:
            return None
        data_folder = self.settings.get("data_folder", "./astrolabe_data")
        os.makedirs(data_folder, exist_ok=True)
        return os.path.join(data_folder, f"{self.current_model}_history.json")
    
    def save_history(self):
        """Save history to file"""
        if not self.current_model:
            return
        
        history_file = self.get_history_file()
        if history_file:
            try:
                with open(history_file, 'w') as f:
                    json.dump(self.history_data, f, indent=2)
            except Exception as e:
                print(f"Error saving history: {e}")
    
    def load_history(self):
        """Load history from file"""
        if not self.current_model:
            return
        
        history_file = self.get_history_file()
        if history_file and os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.history_data = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                self.history_data = []
        else:
            self.history_data = []
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title area
        title_layout = QHBoxLayout()
        self.title_label = QLabel("Select a controller to begin")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Create tabs for different sections
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setUsesScrollButtons(True)
        
        # Tab 1: Tune Model
        self.tune_tab = self.create_tune_tab()
        self.tabs.addTab(self.tune_tab, "Tune Model")
        
        # Tab 2: History
        self.history_tab = self.create_history_tab()
        self.tabs.addTab(self.history_tab, "History")
        
        # Tab 3: Configuration
        self.config_tab = self.create_config_tab()
        self.tabs.addTab(self.config_tab, "Configuration")
        
        # Tab 4: Parameters & Loss
        self.params_loss_tab = self.create_params_loss_tab()
        self.tabs.addTab(self.params_loss_tab, "Parameters & Loss")
        
        # Tab 5: Notes
        self.notes_tab = self.create_notes_tab()
        self.tabs.addTab(self.notes_tab, "Notes")
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
        self.show_empty_state()
        # Apply initial styling based on current theme
        self.update_styling(self.settings.get("dark_mode", False))
    
    def create_tune_tab(self):
        """Create the tune model tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Loss/Custom parameters section (dynamic based on loss function)
        self.loss_group = QGroupBox("Loss Value")
        self.loss_group_layout = QVBoxLayout()
        
        # This will be swapped between loss input and custom parameters
        self.loss_input = QDoubleSpinBox()
        self.loss_input.setRange(-1000000, 1000000)
        self.loss_input.setValue(0.0)
        self.loss_input.setSingleStep(0.01)
        self.loss_input.setMinimumHeight(30)
        self.loss_input.setToolTip("Enter the loss/error value for this set of parameters")
        
        self.loss_form_layout = QFormLayout()
        self.loss_form_layout.addRow("Loss (Error):", self.loss_input)
        self.loss_group_layout.addLayout(self.loss_form_layout)
        
        self.loss_group.setLayout(self.loss_group_layout)
        layout.addWidget(self.loss_group)
        
        # Initialize loss param inputs list
        self.loss_param_inputs = []
        
        # Parameter inputs section
        params_group = QGroupBox("Model Parameters")
        params_layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(200)
        scroll_widget = QWidget()
        self.params_form_layout = QFormLayout()
        self.params_form_layout.setSpacing(8)
        
        scroll_widget.setLayout(self.params_form_layout)
        scroll.setWidget(scroll_widget)
        params_layout.addWidget(scroll)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Result area
        self.result_group = QGroupBox("Optimizer Output")
        result_layout = QVBoxLayout()
        self.result_display = QLabel("")
        self.result_display.setWordWrap(True)
        self.result_display.setMinimumHeight(100)
        dark_mode = self.settings.get("dark_mode", False)
        if dark_mode:
            self.result_display.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px; color: #e0e0e0; border: 1px solid #444444;")
        else:
            self.result_display.setStyleSheet("background-color: white; padding: 10px; border-radius: 4px; color: #333333; border: 1px solid #cccccc;")
        result_layout.addWidget(self.result_display)
        self.result_group.setLayout(result_layout)
        self.result_group.setVisible(False)
        layout.addWidget(self.result_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.tune_btn = QPushButton("Execute Tuning")
        self.tune_btn.setMinimumHeight(40)
        self.tune_btn.clicked.connect(self.tune_model)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self.clear_tune_form)
        
        button_layout.addWidget(self.tune_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_history_tab(self):
        """Create the history tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Tuning History:"))
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Loss", "Parameters", "Suggested Next", "Actions"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setMinimumHeight(300)
        
        layout.addWidget(self.history_table)
        
        # Button layout for history management
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        clear_history_btn = QPushButton("Clear All History")
        clear_history_btn.setObjectName("deleteBtn")
        clear_history_btn.setMaximumWidth(150)
        clear_history_btn.clicked.connect(self.clear_history)
        
        export_history_btn = QPushButton("Export History")
        export_history_btn.setMaximumWidth(150)
        export_history_btn.clicked.connect(self.export_history)
        
        button_layout.addWidget(clear_history_btn)
        button_layout.addWidget(export_history_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_config_tab(self):
        """Create the configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Config display
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.config_display = QLabel("")
        self.config_display.setTextFormat(Qt.RichText)
        self.config_display.setWordWrap(True)
        dark_mode = self.settings.get("dark_mode", False)
        if dark_mode:
            self.config_display.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px; color: #e0e0e0; border: 1px solid #444444;")
        else:
            self.config_display.setStyleSheet("background-color: white; padding: 10px; border-radius: 4px; color: #333333; border: 1px solid #cccccc;")
        scroll.setWidget(self.config_display)
        
        layout.addWidget(scroll)
        
        # Edit config button
        edit_btn = QPushButton("⚙ Edit Configuration")
        edit_btn.setMinimumHeight(40)
        edit_btn.setMaximumWidth(200)
        edit_btn.clicked.connect(self.open_edit_config)
        layout.addWidget(edit_btn)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_params_loss_tab(self):
        """Create the parameters and loss function tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Parameters section
        param_group = QGroupBox("Model Parameters")
        param_layout = QVBoxLayout()
        
        self.param_display = QLabel("")
        self.param_display.setWordWrap(True)
        param_layout.addWidget(self.param_display)
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        
        # Loss function section
        loss_group = QGroupBox("Custom Loss Function")
        loss_layout = QVBoxLayout()
        loss_layout.setSpacing(8)
        
        info_label = QLabel("Define a mathematical expression using parameter names.")
        info_label.setWordWrap(True)
        loss_layout.addWidget(info_label)
        
        loss_layout.addWidget(QLabel("Example: distance/time or (x + y) * z"))
        
        self.loss_func_input = QLineEdit()
        self.loss_func_input.setPlaceholderText("Enter loss function (e.g., distance/time)")
        self.loss_func_input.setMinimumHeight(35)
        self.loss_func_input.setToolTip("Use parameter names in mathematical expressions")
        self.loss_func_input.textChanged.connect(self.on_loss_function_changed)
        loss_layout.addWidget(self.loss_func_input)
        
        # Custom parameters section
        custom_param_label = QLabel("Additional Parameters for Loss Function:")
        loss_layout.addWidget(custom_param_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.custom_params_layout = QVBoxLayout()
        self.custom_param_fields = []
        
        self.add_custom_param_btn = QPushButton("+ Add Custom Parameter")
        self.add_custom_param_btn.setMinimumHeight(35)
        self.add_custom_param_btn.clicked.connect(self.add_custom_parameter)
        self.custom_params_layout.addWidget(self.add_custom_param_btn)
        self.custom_params_layout.addStretch()
        
        scroll_widget.setLayout(self.custom_params_layout)
        scroll.setWidget(scroll_widget)
        scroll.setMaximumHeight(150)
        loss_layout.addWidget(scroll)
        
        # Save button
        save_loss_btn = QPushButton("Save Loss Function")
        save_loss_btn.setMinimumHeight(40)
        save_loss_btn.clicked.connect(self.save_loss_function)
        loss_layout.addWidget(save_loss_btn)
        
        loss_group.setLayout(loss_layout)
        layout.addWidget(loss_group)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def add_custom_parameter(self):
        """Add a custom parameter field"""
        param_widget = QWidget()
        param_h_layout = QHBoxLayout()
        param_h_layout.setContentsMargins(5, 5, 5, 5)
        param_h_layout.setSpacing(5)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Parameter name")
        name_input.setMinimumHeight(30)
        
        value_spin = QDoubleSpinBox()
        value_spin.setRange(-10000, 10000)
        value_spin.setValue(1.0)
        value_spin.setMinimumHeight(30)
        
        remove_btn = QPushButton("-")
        remove_btn.setMaximumWidth(30)
        remove_btn.setMinimumHeight(30)
        remove_btn.setObjectName("deleteBtn")
        
        def remove_param():
            param_widget.deleteLater()
            self.custom_param_fields.remove((name_input, value_spin))
        
        remove_btn.clicked.connect(remove_param)
        
        param_h_layout.addWidget(QLabel("Name:"))
        param_h_layout.addWidget(name_input, 1)
        param_h_layout.addWidget(QLabel("Value:"))
        param_h_layout.addWidget(value_spin, 1)
        param_h_layout.addWidget(remove_btn)
        
        param_widget.setLayout(param_h_layout)
        
        # Insert before stretch and add button
        self.custom_params_layout.insertWidget(
            self.custom_params_layout.count() - 2, param_widget
        )
        
        self.custom_param_fields.append((name_input, value_spin))
    
    def on_loss_function_changed(self):
        """Handle loss function text change"""
        pass
    
    def save_loss_function(self):
        """Save the loss function and custom parameters"""
        if not self.current_model:
            QMessageBox.warning(self, "No Model", "Please select a model first")
            return
        
        loss_func = self.loss_func_input.text().strip()
        custom_param_names = []
        
        for name_input, _ in self.custom_param_fields:
            param_name = name_input.text().strip()
            if param_name:
                custom_param_names.append(param_name)
        
        # Get current model config
        config = self.manager.get_model(self.current_model)
        config['loss_function'] = loss_func
        config['custom_param_names'] = custom_param_names
        config['custom_param_values'] = []
        
        # Save to models.json
        self.manager.update_model(self.current_model, config)

        # Refresh the tune tab to reflect the new loss mode
        self.update_loss_section(config)
        
        QMessageBox.information(self, "Success", 
            "✓ Loss function and parameters saved!")

    def create_notes_tab(self):
        """Create the notes tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("Model Notes:"))
        
        self.notes_edit = QLineEdit()
        self.notes_edit.setPlaceholderText("Add notes about this model...")
        self.notes_edit.setMinimumHeight(50)
        self.notes_edit.textChanged.connect(self.save_notes)
        
        layout.addWidget(self.notes_edit)
        
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("Last Updated: "))
        self.notes_timestamp = QLabel("-")
        layout.addWidget(self.notes_timestamp)
        
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def show_empty_state(self):
        """Show empty state when no model is selected"""
        self.title_label.setText("No Controller Selected")
        self.tabs.setEnabled(False)
        self.result_display.setText("Select a controller from the left panel to get started.")
    
    def load_model(self, model_name: str):
        """Load and display a model"""
        self.current_model = model_name
        self.tabs.setEnabled(True)
        
        config = self.manager.get_model(model_name)
        self.title_label.setText(f"Controller: {model_name}")
        
        # Update tune tab
        self.update_tune_form(config)
        self.update_loss_section(config)
        
        # Update config tab
        self.update_config_display(config)
        
        # Update parameters & loss tab
        self.update_params_loss_display(config)
        
        # Load history from file
        self.load_history()
        self.update_history_display()
        
        # Load notes if they exist
        self.load_notes()
        
        # Clear result display
        self.result_group.setVisible(False)
    
    def update_tune_form(self, config):
        """Update the tune form with current model parameters"""
        # Clear existing fields
        while self.params_form_layout.count():
            self.params_form_layout.takeAt(0).widget().deleteLater()
        
        self.param_inputs = []
        param_names = config.get('param_names', [])
        
        for i in range(config['num_params']):
            min_val = config['mins'][i]
            max_val = config['maxs'][i]
            current_val = config['current_weights'][i]
            
            # Use named parameter if available
            if i < len(param_names) and param_names[i]:
                label = f"{param_names[i]} [{min_val:.4f}, {max_val:.4f}]"
            else:
                label = f"Parameter {i + 1} [{min_val:.4f}, {max_val:.4f}]"
            
            spin = QDoubleSpinBox()
            spin.setRange(min_val, max_val)
            spin.setValue(current_val)
            spin.setSingleStep((max_val - min_val) / 100)
            spin.setMinimumHeight(30)
            
            self.params_form_layout.addRow(label, spin)
            self.param_inputs.append(spin)
    
    def update_config_display(self, config):
        """Update the configuration display"""
        text = f"<b>Model Name:</b> {config['name']}<br>"
        text += f"<b>Optimizer:</b> {config['optimizer_type']}<br>"
        text += f"<b>Parameters:</b> {config['num_params']}<br><br>"
        
        text += "<b>Parameter Bounds:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i in range(config['num_params']):
            text += f"<tr><td>P{i+1}:</td><td style='padding-left: 20px;'>"
            text += f"[{config['mins'][i]:.6f}, {config['maxs'][i]:.6f}]</td></tr>"
        text += "</table><br>"
        
        text += "<b>Learning Rates:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i, lr in enumerate(config['learning_rates']):
            text += f"<tr><td>P{i+1}:</td><td style='padding-left: 20px;'>{lr:.8f}</td></tr>"
        text += "</table>"
        
        self.config_display.setText(text)
    
    def update_params_loss_display(self, config):
        """Update the parameters and loss function display"""
        # Display parameters
        param_names = config.get('param_names', [])
        param_text = "<b>Model Parameters:</b><br><table style='margin-left: 20px;'>"
        
        for i in range(config['num_params']):
            if i < len(param_names) and param_names[i]:
                param_text += f"<tr><td><b>{param_names[i]}:</b></td>"
            else:
                param_text += f"<tr><td><b>param_{i+1}:</b></td>"
            
            param_text += f"<td style='padding-left: 15px;'>"
            param_text += f"[{config['mins'][i]:.4f}, {config['maxs'][i]:.4f}]"
            param_text += f" = {config['current_weights'][i]:.6f}</td></tr>"
        
        param_text += "</table>"
        self.param_display.setText(param_text)
        
        # Load loss function and custom parameters
        loss_func = config.get('loss_function', '')
        self.loss_func_input.setText(loss_func)
        
        # Clear and reload custom parameters
        for name_input, _ in self.custom_param_fields:
            param_widget = name_input.parentWidget()
            if param_widget:
                param_widget.deleteLater()

        self.custom_param_fields.clear()
        
        custom_param_names = config.get('custom_param_names', [])
        
        for param_name in custom_param_names:
            self.add_custom_parameter()
            name_input, value_spin = self.custom_param_fields[-1]
            name_input.setText(param_name)
            value_spin.setValue(0.0)
    
    def update_loss_section(self, config):
        """Update the loss section to show either loss input or custom parameters based on loss function"""
        loss_func = config.get('loss_function', '')
        
        # Clear the entire layout completely without destroying the persistent loss input
        while self.loss_form_layout.count():
            item = self.loss_form_layout.takeAt(0)
            widget = item.widget()
            if not widget:
                continue
            # Keep the shared loss_input alive when swapping between modes
            if widget is self.loss_input:
                widget.setParent(None)
            else:
                widget.deleteLater()
        
        # Clear previous loss param inputs
        for widget in [spin for _, spin in self.loss_param_inputs]:
            widget.deleteLater()
        self.loss_param_inputs = []
        
        if loss_func:
            # Show custom parameters instead of loss input
            self.loss_group.setTitle("Loss Function Parameters")
            
            custom_param_names = config.get('custom_param_names', [])
            
            for param_name in custom_param_names:
                spin = QDoubleSpinBox()
                spin.setRange(-1000000, 1000000)
                spin.setValue(0.0)
                spin.setMinimumHeight(30)
                spin.setToolTip(f"Value for {param_name} in loss function")
                
                self.loss_form_layout.addRow(f"{param_name}:", spin)
                self.loss_param_inputs.append((param_name, spin))
        else:
            # Show loss input
            self.loss_group.setTitle("Loss Value")
            self.loss_input.setValue(0.0)
            self.loss_form_layout.addRow("Loss (Error):", self.loss_input)
    
    def update_history_display(self):
        """Update the history table display"""
        self.history_table.setRowCount(len(self.history_data))
        
        for row, entry in enumerate(self.history_data):
            time_item = QTableWidgetItem(entry['timestamp'])
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            
            loss_item = QTableWidgetItem(f"{entry['loss']:.6f}")
            loss_item.setTextAlignment(Qt.AlignCenter)
            loss_item.setFlags(loss_item.flags() & ~Qt.ItemIsEditable)
            
            params_text = ", ".join([f"{p:.4f}" for p in entry['parameters']])
            params_item = QTableWidgetItem(params_text)
            params_item.setFlags(params_item.flags() & ~Qt.ItemIsEditable)
            
            suggested_text = "N/A"
            if entry.get('suggested'):
                suggested_text = ", ".join([f"{s:.4f}" for s in entry['suggested']])
            suggested_item = QTableWidgetItem(suggested_text)
            suggested_item.setFlags(suggested_item.flags() & ~Qt.ItemIsEditable)
            
            # Delete button
            delete_btn = QPushButton("✕")
            delete_btn.setMaximumWidth(40)
            delete_btn.setObjectName("deleteBtn")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_history_entry(r))
            
            self.history_table.setItem(row, 0, time_item)
            self.history_table.setItem(row, 1, loss_item)
            self.history_table.setItem(row, 2, params_item)
            self.history_table.setItem(row, 3, suggested_item)
            self.history_table.setCellWidget(row, 4, delete_btn)
    
    def tune_model(self):
        """Tune the model with entered parameters"""
        if not self.current_model:
            QMessageBox.warning(self, "Error", "No model selected!")
            return
        
        parameters = [spin.value() for spin in self.param_inputs]
        
        # Get loss value - either direct input or from loss function
        config = self.manager.get_model(self.current_model)
        loss_func = config.get('loss_function', '')
        
        if loss_func:
            # Evaluate loss function with custom parameters
            try:
                # Build the evaluation context
                eval_context = {}
                
                # Add model parameters to context
                param_names = config.get('param_names', [])
                for i, param_name in enumerate(param_names):
                    if i < len(parameters):
                        eval_context[param_name] = parameters[i]
                
                # Add custom loss parameters to context
                for param_name, spin in self.loss_param_inputs:
                    eval_context[param_name] = spin.value()
                
                # Evaluate the loss function
                loss = eval(loss_func, {"__builtins__": {}}, eval_context)
            except Exception as e:
                QMessageBox.warning(self, "Loss Function Error", 
                    f"Failed to evaluate loss function:\n{e}")
                return
        else:
            # Use direct loss input
            loss = self.loss_input.value()
        
        try:
            controller = self.manager.get_controller(self.current_model)
            
            if controller is not None:
                # Pass the loss and parameters to the controller
                controller.tell(loss, parameters)
                
                # Get the optimizer output (next suggested parameters)
                optimizer_output = controller.opt.ask()
                
                # Update the controller's current state
                controller.opt.current = np.array(parameters)
                controller.current = np.array(parameters)
            
            config["current_weights"] = parameters
            self.manager.update_model(self.current_model, config)
            
            # Add to history
            self.history_data.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'loss': loss,
                'parameters': parameters,
                'suggested': optimizer_output.tolist() if isinstance(optimizer_output, np.ndarray) else []
            })
            
            # Save history to file
            self.save_history()
            
            # Update displays
            self.update_history_display()
            
            # Format optimizer output
            opt_output_text = "N/A"
            if optimizer_output is not None:
                if isinstance(optimizer_output, np.ndarray):
                    opt_output_text = ", ".join([f"{o:.6f}" for o in optimizer_output])
                else:
                    opt_output_text = str(optimizer_output)
            
            result_text = f"<b>✓ Tuning Complete</b><br><br>"
            result_text += f"<b>Loss Value:</b> {loss:.6f}<br>"
            result_text += f"<b>Parameters:</b> " + ", ".join([f"{p:.6f}" for p in parameters]) + "<br><br>"
            result_text += f"<b>Optimizer Suggested Next Parameters:</b><br>"
            result_text += f"<code>{opt_output_text}</code>"
            
            self.result_display.setText(result_text)
            self.result_group.setVisible(True)
            
            QMessageBox.information(self, "Success", "✓ Model tuned successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"✗ Error during tuning:\n{e}")
            import traceback
            traceback.print_exc()
    
    def clear_tune_form(self):
        """Clear the tune form"""
        config = self.manager.get_model(self.current_model)
        for i, spin in enumerate(self.param_inputs):
            spin.setValue(config['current_weights'][i])
        
        # Clear loss input or loss parameters based on configuration
        loss_func = config.get('loss_function', '')
        if not loss_func:
            self.loss_input.setValue(0.0)
        else:
            for param_name, spin in self.loss_param_inputs:
                spin.setValue(0.0)
        
        self.result_group.setVisible(False)
    
    def clear_history(self):
        """Clear tuning history"""
        reply = QMessageBox.question(self, "Clear History", 
            "⚠ Are you sure you want to clear all history?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.history_data = []
            self.save_history()
            self.update_history_display()
            QMessageBox.information(self, "Success", "✓ History cleared!")
    
    def delete_history_entry(self, row):
        """Delete a specific history entry"""
        if 0 <= row < len(self.history_data):
            reply = QMessageBox.question(self, "Delete Entry", 
                "⚠ Delete this history entry?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                del self.history_data[row]
                self.save_history()
                self.update_history_display()
    
    def export_history(self):
        """Export history to CSV file"""
        if not self.history_data:
            QMessageBox.warning(self, "No Data", "⚠ No history to export!")
            return
        
        try:
            import csv
            from datetime import datetime
            
            filename = f"astrolabe_history_{self.current_model}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Loss", "Parameters", "Suggested Next"])
                
                for entry in self.history_data:
                    params_str = "|".join([f"{p:.6f}" for p in entry['parameters']])
                    suggested_str = "|".join([f"{s:.6f}" for s in entry.get('suggested', [])])
                    
                    writer.writerow([
                        entry['timestamp'],
                        f"{entry['loss']:.6f}",
                        params_str,
                        suggested_str
                    ])
            
            QMessageBox.information(self, "Success", 
                f"✓ History exported to:\n{filename}")
        
        except Exception as e:
            QMessageBox.critical(self, "Export Error", 
                f"✗ Failed to export history:\n{e}")
    
    def save_notes(self):
        """Save model notes"""
        if self.current_model:
            # TODO: Implement persistent note storage
            pass
    
    def load_notes(self):
        """Load model notes"""
        # TODO: Implement persistent note loading
        self.notes_edit.setText("")
        self.notes_timestamp.setText("-")
    
    def open_edit_config(self):
        """Open edit configuration dialog"""
        if self.current_model:
            dialog = EditConfigDialog(self.manager, self.current_model, self)
            if dialog.exec_():
                self.load_model(self.current_model)
    
    def update_styling(self, dark_mode):
        """Update styling for dark/light mode"""
        if dark_mode:
            # Update title label color
            self.title_label.setStyleSheet("color: #e0e0e0; font-size: 18px; font-weight: bold;")
            self.result_display.setStyleSheet(
                "background-color: #2d2d2d; color: #e0e0e0; border: 1px solid #444444; border-radius: 4px; padding: 10px;"
            )
            self.config_display.setStyleSheet(
                "background-color: #2d2d2d; color: #e0e0e0; border: 1px solid #444444; border-radius: 4px; padding: 10px;"
            )
        else:
            # Update title label color
            self.title_label.setStyleSheet("color: #333333; font-size: 18px; font-weight: bold;")
            self.result_display.setStyleSheet(
                "background-color: #ffffff; color: #333333; border: 1px solid #cccccc; border-radius: 4px; padding: 10px;"
            )
            self.config_display.setStyleSheet(
                "background-color: #ffffff; color: #333333; border: 1px solid #cccccc; border-radius: 4px; padding: 10px;"
            )


class SettingsDialog(QDialog):
    """Settings dialog for app preferences"""
    
    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 500, 250)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Application Settings")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        layout.addWidget(QLabel(""))
        
        # Data folder
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(10)
        
        layout.addWidget(QLabel("Data Folder:"))
        self.folder_input = QLineEdit()
        self.folder_input.setText(self.settings.get("data_folder", "./astrolabe_data"))
        self.folder_input.setReadOnly(True)
        self.folder_input.setMinimumHeight(30)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setMaximumWidth(100)
        browse_btn.clicked.connect(self.browse_folder)
        
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)
        
        layout.addWidget(QLabel(""))
        
        # Dark mode
        self.dark_mode_check = QCheckBox("Dark Mode")
        self.dark_mode_check.setChecked(self.settings.get("dark_mode", False))
        self.dark_mode_check.setMinimumHeight(30)
        layout.addWidget(self.dark_mode_check)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Settings")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancelBtn")
        
        save_btn.setMinimumHeight(40)
        cancel_btn.setMinimumHeight(40)
        
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Data Folder",
            self.folder_input.text()
        )
        if folder:
            self.folder_input.setText(folder)
    
    def save_settings(self):
        self.settings.set("data_folder", self.folder_input.text())
        self.settings.set("dark_mode", self.dark_mode_check.isChecked())
        QMessageBox.information(self, "Success", "✓ Settings saved!")
        self.accept()


class AstrolabeApp(QMainWindow):
    """Main Qt Application with split-pane layout"""
    
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.manager = ModelManager(self.settings)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Astrolabe RL Model Manager")
        self.setGeometry(100, 100, 1400, 850)
        
        # Apply stylesheet with dark mode setting
        dark_mode = self.settings.get("dark_mode", False)
        self.setStyleSheet(get_stylesheet(dark_mode))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)  # Reduced from 0 for less vertical line
        
        # Left sidebar
        sidebar_widget = QWidget()
        if dark_mode:
            sidebar_widget.setStyleSheet("""
                QWidget#sidebarWidget {
                    background-color: #2d2d2d;
                    border-right: 1px solid #444444;
                }
            """)
        else:
            sidebar_widget.setStyleSheet("""
                QWidget#sidebarWidget {
                    background-color: #f0f0f0;
                    border-right: 1px solid #cccccc;
                }
            """)
        sidebar_widget.setObjectName("sidebarWidget")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(10)
        
        # App title in sidebar
        app_title = QLabel("Astrolabe")
        app_title_font = QFont()
        app_title_font.setPointSize(14)
        app_title_font.setBold(True)
        app_title.setFont(app_title_font)
        if dark_mode:
            app_title.setStyleSheet("color: #e0e0e0;")
        else:
            app_title.setStyleSheet("color: #333333;")
        sidebar_layout.addWidget(app_title)
        
        # Main content area (create before controller list)
        self.main_content = MainContentWidget(self.manager, self.settings)
        
        # Controller list widget
        self.controller_list = ControllerListWidget(
            self.manager, 
            on_selection_changed=self.on_controller_selected,
            dark_mode=dark_mode
        )
        sidebar_layout.addWidget(self.controller_list)
        
        # Connect add/remove buttons
        self.controller_list.add_btn.clicked.disconnect()
        self.controller_list.remove_btn.clicked.disconnect()
        self.controller_list.add_btn.clicked.connect(self.add_controller)
        self.controller_list.remove_btn.clicked.connect(self.remove_controller)
        
        # Add stretch to push settings button to bottom
        sidebar_layout.addStretch()
        
        # Settings button
        settings_btn = QPushButton("⚙ Settings")
        settings_btn.setMinimumHeight(35)
        settings_btn.clicked.connect(self.open_settings)
        sidebar_layout.addWidget(settings_btn)
        
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setMaximumWidth(280)
        sidebar_widget.setMinimumWidth(200)
        
        main_layout.addWidget(sidebar_widget, 0)
        main_layout.addWidget(self.main_content, 1)
        
        central_widget.setLayout(main_layout)
        
        # Initialize status bar message
        self.statusBar().showMessage("Ready")
    
    def on_controller_selected(self, model_name: str):
        """Handle controller selection"""
        self.main_content.load_model(model_name)
        self.statusBar().showMessage(f"Loaded controller: {model_name}", 2000)
    
    def add_controller(self):
        """Open dialog to add a new controller"""
        self.statusBar().showMessage("Opening Add Controller dialog...")
        dialog = AddModelDialog(self.manager, self)
        if dialog.exec_():
            self.controller_list.refresh_list()
            # Select the newly added model
            if self.manager.get_all_models():
                self.controller_list.list_widget.setCurrentRow(0)
            self.statusBar().showMessage("Controller added successfully", 3000)
    
    def remove_controller(self):
        """Remove selected controller"""
        model_name = self.controller_list.get_selected()
        
        if not model_name:
            QMessageBox.warning(self, "No Selection", 
                "⚠ Please select a controller to remove!")
            return
        
        reply = QMessageBox.question(self, "Confirm Removal", 
            f"⚠ Are you sure you want to remove '{model_name}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.manager.remove_model(model_name)
            self.controller_list.refresh_list()
            self.main_content.show_empty_state()
            self.statusBar().showMessage(f"Controller '{model_name}' removed", 3000)
    
    def open_settings(self):
        """Open settings dialog"""
        old_data_folder = self.settings.get("data_folder", "./astrolabe_data")
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            # Refresh the entire app with new settings
            dark_mode = self.settings.get("dark_mode", False)
            self.setStyleSheet(get_stylesheet(dark_mode))
            
            # Update sidebar styling
            sidebar_widget = self.findChild(QWidget, "sidebarWidget")
            if sidebar_widget:
                if dark_mode:
                    sidebar_widget.setStyleSheet("""
                        QWidget#sidebarWidget {
                            background-color: #2d2d2d;
                            border-right: 1px solid #444444;
                        }
                    """)
                else:
                    sidebar_widget.setStyleSheet("""
                        QWidget#sidebarWidget {
                            background-color: #f0f0f0;
                            border-right: 1px solid #cccccc;
                        }
                    """)
            
            # Update controller list styling
            self.controller_list.dark_mode = dark_mode
            self.controller_list.update_styling()
            
            # Update main content widget styling
            self.main_content.update_styling(dark_mode)

            # If the data folder changed, reload models from the new location
            new_data_folder = self.settings.get("data_folder", "./astrolabe_data")
            if new_data_folder != old_data_folder:
                self.manager = ModelManager(self.settings)
                self.controller_list.manager = self.manager
                self.main_content.manager = self.manager
                self.controller_list.refresh_list()
                self.main_content.show_empty_state()
            
            self.statusBar().showMessage("Settings updated successfully", 2000)


def main():
    app = QApplication(sys.argv)
    window = AstrolabeApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
