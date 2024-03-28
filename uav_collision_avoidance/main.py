"""Main module for UAV Collision Avoidance application"""

import logging
import platform
import datetime
import signal
from pathlib import Path

from PySide6.QtWidgets import QApplication
from .version import __version__ as version
from .src.simulation.simulation import Simulation, SimulationSettings

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

logging.info("-" * 120)
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        f"io.github.mldxo.uav-collision-avoidance.{version}")
logging.info("Detected platform: %s", platform.system())

def main():
    """Executes main function"""
    import sys
    args = sys.argv[1:]
    realtime : bool = True
    run_tests : bool = False
    if len(args) > 0:
        if args[0] == "realtime":
            realtime = True
        elif args[0] == "prerender":
            realtime = False
        elif args[0] == "tests":
            run_tests = True
        elif len(args) > 1:
            logging.error("Invalid arguments: %s", args)
            sys.exit(1)
        else:
            logging.error("Invalid argument: %s", args[0])
            sys.exit(1)
    app = QApplication(args)
    app.setApplicationName("UAV Collsion Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    logging.info("%s %s", app.applicationName(), app.applicationVersion())
    sim = Simulation()
    if run_tests:
        realtime = False
        sim.run_tests(20)
        sys.exit()
    elif realtime:
        sim.run_realtime()
        sys.exit(app.exec())
    else:
        sim.run_prerender()
        sys.exit()

if __name__ == "__main__":
    main()
