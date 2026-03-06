"""
Qt GUI Application for Backstaff Reinforcement Learning Controller
Main entry point - delegates to ui module
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import BackstaffApp


def main():
    app = QApplication(sys.argv)
    window = BackstaffApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
