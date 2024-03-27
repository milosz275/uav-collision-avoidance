"""Main module for UAV Collision Avoidance application"""

import sys
import logging
import platform
import datetime
import signal
from pathlib import Path

from PySide6.QtWidgets import QApplication
from version import __version__ as version
from src.simulation.simulation import Simulation, SimulationSettings

signal.signal(signal.SIGINT, signal.SIG_DFL)
try:
    start_time = datetime.datetime.now().strftime("%Y-%m-%d")
    Path("logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=f"logs/simulation-{start_time}.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s")
except:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
        handlers=[logging.StreamHandler()])

logging.info("-" * 80)
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        f"io.github.mldxo.uav-collision-avoidance.{version}")
logging.info("Detected platform: %s", platform.system())

realtime : bool = True

def main(args):
    """Executes main function"""
    app = QApplication(args)
    app.setApplicationName("UAV Collsion Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    logging.info("%s %s", app.applicationName(), app.applicationVersion())
    sim = Simulation()
    if realtime:
        sim.run_realtime()
        sys.exit(app.exec())
    else:
        sim.run_prerender()
        sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
