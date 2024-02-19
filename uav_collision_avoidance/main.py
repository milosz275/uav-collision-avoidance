# main.py

import sys
import platform
if platform.system() == 'Windows':
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('io.github.mldxo.uav-collision-avoidance.1')

from PySide6.QtWidgets import QApplication
from src.simulation.simulation_settings import SimulationSettings
from src.simulation.simulation import Simulation

def main(args):
    """Executes main function"""
    app = QApplication(args)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    sim = Simulation()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv[1:])
