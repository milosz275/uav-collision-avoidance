# main.py

with open("../version", "r") as file:
    version = file.read()

import sys
import platform
if platform.system() == 'Windows':
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f'io.github.mldxo.uav-collision-avoidance.{version}')

from PySide6.QtWidgets import QApplication
from src.simulation.simulation_settings import SimulationSettings
from src.simulation.simulation import Simulation

def main(args):
    """Executes main function"""
    app = QApplication(args)
    app.setApplicationName("UAV Collsion Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    sim = Simulation()
    sim.run_realtime()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv[1:])
