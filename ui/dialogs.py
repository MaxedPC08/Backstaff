"""Dialog windows for the application"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QPushButton, QMessageBox, QScrollArea, QWidget, QFormLayout, QGroupBox,
    QCheckBox, QFileDialog, QTabWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import numpy as np


class AddModelDialog(QDialog):
    """Dialog for adding a new model"""
    
    def __init__(self, manager, parent=None):
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
        
        # Stochasticity rate
        self.stoch_rate_spin = QDoubleSpinBox()
        self.stoch_rate_spin.setRange(0.0, 1.0)
        self.stoch_rate_spin.setValue(1.0)
        self.stoch_rate_spin.setSingleStep(0.1)
        self.stoch_rate_spin.setMinimumHeight(35)
        self.stoch_rate_spin.setToolTip("Controls exploration randomness (0.0 = pure deterministic, 1.0 = 50% deterministic + 50% random)")
        form_layout.addRow("Stochasticity Rate:", self.stoch_rate_spin)
        
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
        create_btn = QPushButton("Create Model")
        create_btn.setMinimumHeight(40)
        create_btn.setMinimumWidth(120)
        cancel_btn = QPushButton("Cancel")
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
            "stochasticity_rate": self.stoch_rate_spin.value(),
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


class EditConfigDialog(QDialog):
    """Dialog for editing model configuration"""
    
    def __init__(self, manager, model_name: str, parent=None):
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
        
        # Tab 1: Edit bounds (min and max side by side)
        bounds_widget = self.create_combined_bounds_tab()
        tabs.addTab(bounds_widget, "Bounds")
        
        # Tab 2: Edit learning rates
        lr_widget = self.create_learning_rates_tab()
        tabs.addTab(lr_widget, "Learning Rates")
        
        # Tab 4: Edit stochasticity rate
        stoch_widget = self.create_stochasticity_tab()
        tabs.addTab(stoch_widget, "Stochasticity")
        
        # Tab 5: View configuration
        view_widget = self.create_view_tab()
        tabs.addTab(view_widget, "View Config")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        save_btn = QPushButton("Save Changes")
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(120)
        cancel_btn = QPushButton("Cancel")
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
    
    def create_combined_bounds_tab(self):
        """Create a tab with min and max bounds side by side"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        title_label = QLabel("Edit Parameter Bounds:")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        main_layout.addWidget(QLabel(""))
        
        # Create horizontal layout for min and max columns
        columns_layout = QHBoxLayout()
        
        # Left column: Min bounds
        min_widget = QWidget()
        min_layout = QVBoxLayout()
        min_header = QLabel("Minimum Bounds")
        min_header_font = QFont()
        min_header_font.setBold(True)
        min_header.setFont(min_header_font)
        min_layout.addWidget(min_header)
        
        min_form = QFormLayout()
        min_form.setSpacing(10)
        
        self.bound_inputs = []
        mins = self.config['mins']
        maxs = self.config['maxs']
        param_names = self.config.get('param_names', [])
        
        for i, val in enumerate(mins):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i + 1}"
            spin = QDoubleSpinBox()
            spin.setRange(-100000, 100000)
            spin.setValue(val)
            spin.setMinimumHeight(35)
            spin.setToolTip(f"Set the minimum value for {param_label}")
            min_form.addRow(f"{param_label}:", spin)
            self.bound_inputs.append(('mins', i, spin))
        
        min_layout.addLayout(min_form)
        min_layout.addStretch()
        min_widget.setLayout(min_layout)
        columns_layout.addWidget(min_widget)
        
        # Right column: Max bounds
        max_widget = QWidget()
        max_layout = QVBoxLayout()
        max_header = QLabel("Maximum Bounds")
        max_header_font = QFont()
        max_header_font.setBold(True)
        max_header.setFont(max_header_font)
        max_layout.addWidget(max_header)
        
        max_form = QFormLayout()
        max_form.setSpacing(10)
        
        for i, val in enumerate(maxs):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i + 1}"
            spin = QDoubleSpinBox()
            spin.setRange(-100000, 100000)
            spin.setValue(val)
            spin.setMinimumHeight(35)
            spin.setToolTip(f"Set the maximum value for {param_label}")
            max_form.addRow(f"{param_label}:", spin)
            self.bound_inputs.append(('maxs', i, spin))
        
        max_layout.addLayout(max_form)
        max_layout.addStretch()
        max_widget.setLayout(max_layout)
        columns_layout.addWidget(max_widget)
        
        main_layout.addLayout(columns_layout)
        widget.setLayout(main_layout)
        return widget
    
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
        param_names = self.config.get('param_names', [])
        
        for i, lr in enumerate(learning_rates):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i + 1}"
            spin = QDoubleSpinBox()
            spin.setRange(0.0001, 100)
            spin.setValue(lr)
            spin.setSingleStep(0.01)
            spin.setMinimumHeight(35)
            spin.setToolTip(f"Learning rate for {param_label}")
            form_layout.addRow(f"{param_label}:", spin)
            self.lr_inputs.append(spin)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_stochasticity_tab(self):
        """Create a tab for editing stochasticity rate"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title_label = QLabel("Edit Stochasticity Rate:")
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        layout.addWidget(QLabel("Controls exploration randomness: 0.0 = pure deterministic, 1.0 = 50% deterministic + 50% random"))
        layout.addWidget(QLabel(""))
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.stoch_rate_spin = QDoubleSpinBox()
        self.stoch_rate_spin.setRange(0.0, 1.0)
        self.stoch_rate_spin.setValue(self.config.get('stochasticity_rate', 1.0))
        self.stoch_rate_spin.setSingleStep(0.1)
        self.stoch_rate_spin.setMinimumHeight(35)
        self.stoch_rate_spin.setToolTip("Controls exploration randomness (0.0 = pure deterministic, 1.0 = 50% deterministic + 50% random)")
        form_layout.addRow("Stochasticity Rate:", self.stoch_rate_spin)
        
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
        text += f"<b>Parameters:</b> {self.config['num_params']}<br>"
        text += f"<b>Stochasticity Rate:</b> {self.config.get('stochasticity_rate', 1.0):.4f}<br><br>"
        
        param_names = self.config.get('param_names', [])
        
        text += "<b>Parameter Bounds:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i in range(self.config['num_params']):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i+1}"
            text += f"<tr><td>{param_label}:</td><td style='padding-left: 20px;'>"
            text += f"[{self.config['mins'][i]:.6f}, {self.config['maxs'][i]:.6f}]</td></tr>"
        text += "</table><br>"
        
        text += "<b>Learning Rates:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i, lr in enumerate(self.config['learning_rates']):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i+1}"
            text += f"<tr><td>{param_label}:</td><td style='padding-left: 20px;'>{lr:.8f}</td></tr>"
        text += "</table><br>"
        
        text += "<b>Current Weights:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i, w in enumerate(self.config['current_weights']):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i+1}"
            text += f"<tr><td>{param_label}:</td><td style='padding-left: 20px;'>{w:.8f}</td></tr>"
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
            
            # Update stochasticity rate if the widget exists
            if hasattr(self, 'stoch_rate_spin'):
                self.config['stochasticity_rate'] = self.stoch_rate_spin.value()
            
            # Validate bounds
            param_names = self.config.get('param_names', [])
            for i in range(self.config['num_params']):
                param_name = param_names[i] if i < len(param_names) else ""
                # Only use custom name if it's not a default param_N name
                param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i+1}"
                if self.config['mins'][i] >= self.config['maxs'][i]:
                    QMessageBox.warning(self, "Validation Error", 
                        f"⚠ {param_label}: Min must be less than Max!")
                    return
            
            self.manager.update_model(self.model_name, self.config)
            QMessageBox.information(self, "Success", 
                "✓ Configuration updated successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"✗ Failed to save configuration:\n{e}")


class SettingsDialog(QDialog):
    """Settings dialog for app preferences"""
    
    def __init__(self, settings, parent=None):
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
        self.folder_input.setText(self.settings.get("data_folder", "./backstaff_data"))
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
