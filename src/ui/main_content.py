import os
import json
from datetime import datetime
import numpy as np
from typing import Dict, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem, QDialog, QMessageBox,
    QListWidget, QListWidgetItem, QTabWidget, QInputDialog, QScrollArea,
    QFormLayout, QGroupBox, QHeaderView, QProgressBar, QStatusBar,
    QSizePolicy, QFileDialog, QCheckBox, QPushButton
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QBrush

from Reinforcement.controller import Controller
from Reinforcement.optimizer import Optimizer
from ui.dialogs import EditConfigDialog


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
        data_folder = self.settings.get("data_folder", "./backstaff_data")
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

        # Warning banner shown when no model is loaded
        self.warning_label = QLabel("No model selected. Add or select a controller before tuning or editing.")
        self.warning_label.setWordWrap(True)
        self.warning_label.setContentsMargins(8, 6, 8, 6)
        layout.addWidget(self.warning_label)
        
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
        
        # Wrapper container for Loss and Parameters sections
        params_container = QGroupBox()
        params_container.setTitle("")
        params_container.setStyleSheet("QGroupBox { border: none; }")
        params_container_layout = QVBoxLayout()
        params_container_layout.setSpacing(10)
        
        # Loss/Custom parameters section (dynamic based on loss function)
        self.loss_group = QGroupBox("Loss Value")
        self.loss_group.setStyleSheet("QGroupBox { border: 3px solid #444444; }")
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
        params_container_layout.addWidget(self.loss_group)
        
        # Initialize loss param inputs list
        self.loss_param_inputs = []
        
        # Parameter inputs section
        params_group = QGroupBox("Model Parameters")
        params_group.setStyleSheet("QGroupBox { border: 3px solid #444444; }")
        params_layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        scroll.setMinimumHeight(200)
        scroll_widget = QWidget()
        self.params_form_layout = QFormLayout()
        self.params_form_layout.setSpacing(8)
        
        scroll_widget.setLayout(self.params_form_layout)
        scroll.setWidget(scroll_widget)
        params_layout.addWidget(scroll)
        
        params_group.setLayout(params_layout)
        params_container_layout.addWidget(params_group)
        
        params_container.setLayout(params_container_layout)
        layout.addWidget(params_container)
        
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
        
        # Greedy mode checkbox
        greedy_layout = QHBoxLayout()
        self.greedy_checkbox = QCheckBox("Use Greedy Mode")
        self.greedy_checkbox.setChecked(True)
        self.greedy_checkbox.setToolTip("When enabled, optimizer uses best known parameters. When disabled, balances exploration and exploitation.")
        greedy_layout.addWidget(self.greedy_checkbox)
        greedy_layout.addStretch()
        layout.addLayout(greedy_layout)
        
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
        # Style the label to match group box titles
        history_label = layout.itemAt(layout.count() - 1).widget()
        history_label.setStyleSheet("font-weight: bold;")
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Loss", "Parameters", "Suggested Next", "Actions"])
        self.history_table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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
        
        # Add title
        layout.addWidget(QLabel("Model Configuration:"))
        # Style the label to match group box titles
        config_label = layout.itemAt(layout.count() - 1).widget()
        config_label.setStyleSheet("font-weight: bold;")
        
        # Config display
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.config_display = QLabel("")
        self.config_display.setTextFormat(Qt.RichText)
        self.config_display.setWordWrap(True)
        self.config_display.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        dark_mode = self.settings.get("dark_mode", False)
        if dark_mode:
            self.config_display.setStyleSheet("background-color: #2d2d2d; padding: 10px; border-radius: 4px; color: #e0e0e0; border: 1px solid #444444;")
        else:
            self.config_display.setStyleSheet("background-color: white; padding: 10px; border-radius: 4px; color: #333333; border: 1px solid #cccccc;")
        scroll.setWidget(self.config_display)
        
        layout.addWidget(scroll, 1)  # stretch factor of 1 to take available space
        
        # Edit config button
        button_layout = QHBoxLayout()
        edit_btn = QPushButton("Edit Configuration")
        edit_btn.setMinimumHeight(40)
        edit_btn.setMaximumWidth(200)
        edit_btn.clicked.connect(self.open_edit_config)
        button_layout.addWidget(edit_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
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
        loss_group.setStyleSheet("QGroupBox { border: 3px solid #444444; }")
        loss_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.custom_params_layout.setSpacing(8)
        self.custom_param_fields = []
        
        self.add_custom_param_btn = QPushButton("+ Add Custom Parameter")
        self.add_custom_param_btn.setMinimumHeight(35)
        self.add_custom_param_btn.clicked.connect(self.add_custom_parameter)
        self.custom_params_layout.addWidget(self.add_custom_param_btn)
        self.custom_params_layout.addStretch()
        
        scroll_widget.setLayout(self.custom_params_layout)
        scroll.setWidget(scroll_widget)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll.setMinimumHeight(300)
        loss_layout.addWidget(scroll, 1)
        
        # Save button
        save_loss_btn = QPushButton("Save Loss Function")
        save_loss_btn.setMinimumHeight(40)
        save_loss_btn.clicked.connect(self.save_loss_function)
        loss_layout.addWidget(save_loss_btn)
        
        loss_group.setLayout(loss_layout)
        layout.addWidget(loss_group, 1)
        
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
        
        remove_btn = QPushButton("-")
        remove_btn.setMaximumWidth(30)
        remove_btn.setMinimumHeight(30)
        remove_btn.setObjectName("deleteBtn")
        
        def remove_param():
            param_widget.deleteLater()
            if name_input in self.custom_param_fields:
                self.custom_param_fields.remove(name_input)
        
        remove_btn.clicked.connect(remove_param)
        
        param_h_layout.addWidget(QLabel("Name:"))
        param_h_layout.addWidget(name_input, 1)
        param_h_layout.addWidget(remove_btn)
        
        param_widget.setLayout(param_h_layout)
        
        # Insert before stretch and add button
        self.custom_params_layout.insertWidget(
            self.custom_params_layout.count() - 2, param_widget
        )
        
        self.custom_param_fields.append(name_input)
    
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
        
        for name_input in self.custom_param_fields:
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
        # Style the label to match group box titles
        notes_label = layout.itemAt(layout.count() - 1).widget()
        notes_label.setStyleSheet("font-weight: bold;")
        
        from PyQt5.QtWidgets import QTextEdit
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Add notes about this model...")
        self.notes_edit.textChanged.connect(self.save_notes)
        
        layout.addWidget(self.notes_edit, 1)  # stretch factor of 1 to take available space
        
        timestamp_layout = QHBoxLayout()
        timestamp_layout.addWidget(QLabel("Last Updated: "))
        self.notes_timestamp = QLabel("-")
        timestamp_layout.addWidget(self.notes_timestamp)
        timestamp_layout.addStretch()
        layout.addLayout(timestamp_layout)
        
        widget.setLayout(layout)
        return widget
    
    def show_empty_state(self):
        """Show empty state when no model is selected"""
        self.title_label.setText("No Controller Selected")
        self.tabs.setEnabled(False)
        self.result_display.setText("Select a controller from the left panel to get started.")
        self.warning_label.setVisible(True)
    
    def load_model(self, model_name: str):
        """Load and display a model"""
        self.current_model = model_name
        self.tabs.setEnabled(True)
        self.warning_label.setVisible(False)
        
        config = self.manager.get_model(model_name)
        
        # If config is None (model doesn't exist), return early
        if config is None:
            return
        
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
        text += f"<b>Parameters:</b> {config['num_params']}<br>"
        text += f"<b>Stochasticity Rate:</b> {config.get('stochasticity_rate', 1.0):.4f}<br><br>"
        
        param_names = config.get('param_names', [])
        
        text += "<b>Parameter Bounds:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i in range(config['num_params']):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i+1}"
            text += f"<tr><td>{param_label}:</td><td style='padding-left: 20px;'>"
            text += f"[{config['mins'][i]:.6f}, {config['maxs'][i]:.6f}]</td></tr>"
        text += "</table><br>"
        
        text += "<b>Learning Rates:</b><br>"
        text += "<table style='margin-left: 20px;'>"
        for i, lr in enumerate(config['learning_rates']):
            param_name = param_names[i] if i < len(param_names) else ""
            # Only use custom name if it's not a default param_N name
            param_label = param_name if param_name and not param_name.startswith('param_') else f"Parameter {i+1}"
            text += f"<tr><td>{param_label}:</td><td style='padding-left: 20px;'>{lr:.8f}</td></tr>"
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
        for name_input in self.custom_param_fields:
            param_widget = name_input.parentWidget()
            if param_widget:
                param_widget.deleteLater()

        self.custom_param_fields.clear()
        
        custom_param_names = config.get('custom_param_names', [])
        
        for param_name in custom_param_names:
            self.add_custom_parameter()
            name_input = self.custom_param_fields[-1]
            name_input.setText(param_name)
    
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
            delete_btn = QPushButton("Delete")
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
                greedy_mode = self.greedy_checkbox.isChecked()
                optimizer_output = controller.opt.ask(greedy=greedy_mode)
                
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
            
            # Add warning if history is short
            if len(self.history_data) < 5:
                result_text += f"<br><br><b style='color: orange;'>⚠ Note:</b> With fewer than 5 training samples, "
                result_text += "the suggested parameters are essentially random. You can choose your own values if preferred."
            
            self.result_display.setText(result_text)
            self.result_group.setVisible(True)
            
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
            
            filename = f"backstaff_history_{self.current_model}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
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
        """Save model notes to file"""
        if self.current_model:
            notes_file = self.get_notes_file()
            if notes_file:
                try:
                    notes_data = {
                        'notes': self.notes_edit.toPlainText(),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    with open(notes_file, 'w') as f:
                        json.dump(notes_data, f, indent=2)
                except Exception as e:
                    print(f"Error saving notes: {e}")
    
    def get_notes_file(self):
        """Get the notes file path for the current model"""
        if not self.current_model:
            return None
        data_folder = self.settings.get("data_folder", "./backstaff_data")
        os.makedirs(data_folder, exist_ok=True)
        return os.path.join(data_folder, f"{self.current_model}_notes.json")
    
    def load_notes(self):
        """Load model notes from file"""
        if not self.current_model:
            self.notes_edit.setPlainText("")
            self.notes_timestamp.setText("-")
            return
        
        notes_file = self.get_notes_file()
        if notes_file and os.path.exists(notes_file):
            try:
                with open(notes_file, 'r') as f:
                    notes_data = json.load(f)
                self.notes_edit.setPlainText(notes_data.get('notes', ''))
                self.notes_timestamp.setText(notes_data.get('timestamp', '-'))
            except Exception as e:
                print(f"Error loading notes: {e}")
                self.notes_edit.setPlainText("")
                self.notes_timestamp.setText("-")
        else:
            self.notes_edit.setPlainText("")
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
            self.warning_label.setStyleSheet(
                "background-color: #3a2b10; color: #f8e6c2; border: 1px solid #66512c; border-radius: 4px;"
                " padding: 8px;"
            )
            # Apply 3px borders to Loss/Model Parameters/Custom Loss Function
            border_style = "QGroupBox { border: 3px solid #444444; }"
            if hasattr(self, 'loss_group'):
                self.loss_group.setStyleSheet(border_style)
            if hasattr(self, 'tabs') and self.tabs.count() > 0:
                # Tune tab
                tune_widget = self.tabs.widget(0)
                for child in tune_widget.findChildren(QGroupBox):
                    title = child.title()
                    if title in ["Loss Value", "Model Parameters"]:
                        child.setStyleSheet(border_style)
                # Params & Loss tab
                params_widget = self.tabs.widget(3)
                if params_widget:
                    for child in params_widget.findChildren(QGroupBox):
                        if child.title() in ["Model Parameters", "Custom Loss Function"]:
                            child.setStyleSheet(border_style)
        else:
            # Update title label color
            self.title_label.setStyleSheet("color: #333333; font-size: 18px; font-weight: bold;")
            self.result_display.setStyleSheet(
                "background-color: #ffffff; color: #333333; border: 1px solid #cccccc; border-radius: 4px; padding: 10px;"
            )
            self.config_display.setStyleSheet(
                "background-color: #ffffff; color: #333333; border: 1px solid #cccccc; border-radius: 4px; padding: 10px;"
            )
            self.warning_label.setStyleSheet(
                "background-color: #fff8e1; color: #5d4400; border: 1px solid #f0d58c; border-radius: 4px;"
                " padding: 8px;"
            )
            # Apply 3px borders to Loss/Model Parameters/Custom Loss Function
            border_style = "QGroupBox { border: 3px solid #444444; }"
            if hasattr(self, 'loss_group'):
                self.loss_group.setStyleSheet(border_style)
            if hasattr(self, 'tabs') and self.tabs.count() > 0:
                # Tune tab
                tune_widget = self.tabs.widget(0)
                for child in tune_widget.findChildren(QGroupBox):
                    title = child.title()
                    if title in ["Loss Value", "Model Parameters"]:
                        child.setStyleSheet(border_style)
                # Params & Loss tab
                params_widget = self.tabs.widget(3)
                if params_widget:
                    for child in params_widget.findChildren(QGroupBox):
                        if child.title() in ["Model Parameters", "Custom Loss Function"]:
                            child.setStyleSheet(border_style)
