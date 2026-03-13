"""Stylesheet definitions for the application"""


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
            border: 1px solid #4CAF50;
            outline: none;
        }
        
        QTextEdit {
            background-color: #2d2d2d;
            border: 2px solid #555555;
            border-radius: 4px;
            padding: 8px;
            color: #e0e0e0;
            selection-background-color: #4CAF50;
        }
        
        QTextEdit:focus {
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
            border: none;
            color: #e0e0e0;
        }
        
        QPushButton#deleteBtn:hover {
            background-color: #7a4a4a;
            border: none;
            color: #e0e0e0;
        }
        
        QPushButton#deleteBtn:pressed {
            background-color: #5a2a2a;
            border: none;
            color: #e0e0e0;
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
            gridline-color: #555555;
            border: 1px solid #444444;
            border-radius: 4px;
            color: #e0e0e0;
        }
        
        QTableWidget::item {
            padding: 5px;
            color: #e0e0e0;
            border: 1px solid #555555;
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
            text-align: left;
        }
        
        QGroupBox {
            color: #e0e0e0;
            border: 1px solid #444444;
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
            border: none;
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
            border: none;
            border-radius: 4px;
        }
        
        QStatusBar {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        
        QListWidget {
            background-color: #2d2d2d;
            color: #e0e0e0;
            border: none;
            border-radius: 0px;
        }
        
        QListWidget::item {
            padding: 8px;
        }
        
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px;
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
            border: 1px solid #4CAF50;
            outline: none;
        }
        
        QTextEdit {
            background-color: white;
            border: 2px solid #999999;
            border-radius: 4px;
            padding: 8px;
            color: #333333;
            selection-background-color: #4CAF50;
        }
        
        QTextEdit:focus {
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
            border: none;
            color: #333333;
        }
        
        QPushButton#deleteBtn:hover {
            background-color: #e6cccc;
            border: none;
            color: #333333;
        }
        
        QPushButton#deleteBtn:pressed {
            background-color: #cc9999;
            border: none;
            color: #333333;
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
            gridline-color: #cccccc;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            color: #333333;
        }
        
        QTableWidget::item {
            padding: 5px;
            color: #333333;
            border: 1px solid #cccccc;
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
            text-align: left;
        }
        
        QGroupBox {
            color: #333333;
            border: 1px solid #cccccc;
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
            border: none;
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
            border: none;
            border-radius: 4px;
        }
        
        QStatusBar {
            background-color: #424242;
            color: white;
        }
        
        QListWidget {
            background-color: white;
            color: #333333;
            border: none;
            border-radius: 0px;
        }
        
        QListWidget::item {
            padding: 8px;
            margin: 0px;
            border: 1px solid transparent;
        }
        
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: white;
            padding: 8px;
            margin: 0px;
            border: 1px solid transparent;
        }
        
        QCheckBox {
            color: #333333;
        }
    """
