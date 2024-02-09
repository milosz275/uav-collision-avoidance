# main.py
import sys
from PySide6.QtWidgets import QApplication
from src.settings import Settings
from src.simulator import Simulator

def main():
    """Executes main function"""
    app = QApplication(sys.argv)
    Settings.screen_resolution = app.primaryScreen().size()
    sim = Simulator()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
