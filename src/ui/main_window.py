"""Main application window"""

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont

from ui.settings_manager import Settings
from ui.styles import get_stylesheet
from ui.model_manager import ModelManager
from ui.main_content import MainContentWidget
from ui.widgets import ControllerListWidget
from ui.dialogs import AddModelDialog, SettingsDialog


class BackstaffApp(QMainWindow):
    """Main Qt Application with split-pane layout"""
    
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.manager = ModelManager(self.settings)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Backstaff")
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
        self.app_title = QLabel("Backstaff")
        app_title_font = QFont()
        app_title_font.setPointSize(14)
        app_title_font.setBold(True)
        self.app_title.setFont(app_title_font)
        if dark_mode:
            self.app_title.setStyleSheet("color: #e0e0e0; background-color: transparent;")
        else:
            self.app_title.setStyleSheet("color: #333333; background-color: transparent;")
        sidebar_layout.addWidget(self.app_title)
        
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
        settings_btn = QPushButton("Settings")
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
            
            # Check if there are any remaining models
            remaining_models = self.manager.get_all_models()
            if remaining_models:
                # Select the first remaining model
                first_model = remaining_models[0]
                self.main_content.load_model(first_model)
            else:
                # No models left, show empty state
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

            # Update sidebar title styling
            if dark_mode:
                self.app_title.setStyleSheet("color: #e0e0e0; background-color: transparent;")
            else:
                self.app_title.setStyleSheet("color: #333333; background-color: transparent;")
            
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
    window = BackstaffApp()
    window.show()
    sys.exit(app.exec_())
