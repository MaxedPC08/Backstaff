"""Sidebar widget for controller management"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ControllerListWidget(QWidget):
    """Left sidebar widget for controller selection and management"""
    
    def __init__(self, manager, on_selection_changed=None, dark_mode=False, parent=None):
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
            title.setStyleSheet("color: #e0e0e0; background-color: transparent;")
        else:
            title.setStyleSheet("color: #333333; background-color: transparent;")
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
        
        add_btn = QPushButton("Add")
        add_btn.setMinimumHeight(35)
        add_btn.setToolTip("Create a new controller")
        
        remove_btn = QPushButton("Remove")
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
                    widget.setStyleSheet("color: #e0e0e0; background-color: transparent;")
                else:
                    widget.setStyleSheet("color: #333333; background-color: transparent;")
        
        # Update list widget styling
        if self.dark_mode:
            self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #2d2d2d;
                    border: 0px solid #2d2d2d;
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
                    border: 0px solid #ffffff;
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
