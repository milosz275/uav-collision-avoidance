# main.py

with open("../version", "r") as file:
    version = file.read()

from pathlib import Path
Path("logs").mkdir(parents=True, exist_ok=True)

import logging
logging.basicConfig(filename="logs/simulation.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s")

import sys
import platform
if platform.system() == 'Windows':
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(f'io.github.mldxo.uav-collision-avoidance.{version}')
logging.info(f"Detected platform: {platform.system()}")

from PySide6.QtWidgets import QApplication

from src.simulation.simulation_settings import SimulationSettings
from src.simulation.simulation import Simulation

def main(args):
    """Executes main function"""
    app = QApplication(args)
    app.setApplicationName("UAV Collsion Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    logging.info("Creating simulation")
    sim = Simulation()
    sim.run_realtime()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv[1:])
