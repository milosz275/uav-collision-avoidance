"""Main module for UAV Collision Avoidance application"""

import sys
import logging
import platform
from pathlib import Path

from PySide6.QtWidgets import QApplication
from version import __version__ as version
from src.simulation.simulation import Simulation, SimulationSettings

Path("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename="logs/simulation.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s")

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        f"io.github.mldxo.uav-collision-avoidance.{version}")
logging.info("Detected platform: %s", platform.system())

def main(args):
    """Executes main function"""
    app = QApplication(args)
    app.setApplicationName("UAV Collsion Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    logging.info("%s %s", app.applicationName(), app.applicationVersion())
    sim = Simulation()
    sim.run_realtime()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv[1:])
