"""Main module for UAV Collision Avoidance application"""

import logging
import platform
import datetime
import signal
from pathlib import Path
from screeninfo import get_monitors

from PySide6.QtWidgets import QApplication
from .version import __version__ as version
from .src.simulation.simulation import Simulation, SimulationSettings

def signal_handler(sig, frame):
    logging.warning("Ctrl+C keyboard interrupt. Exiting...")
    try:
        signal.default_int_handler(sig, frame)
    except KeyboardInterrupt:
        import sys
        sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)
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

def main(arg = None):
    """Executes main function"""
    import sys
    args = sys.argv[1:]
    app = QApplication(args)
    app.setApplicationName("UAV Collsion Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    logging.info("%s %s", app.applicationName(), app.applicationVersion())
    sim : Simulation | None = None
    if len(args) > 0 or arg is not None:
        if args[0] == "realtime":
            if len(get_monitors) == 0:
                logging.warning("Launching GUI Application without monitors detected")
            sim = Simulation()
            sys.exit(app.exec())
        elif args[0] == "headless" or arg == "headless":
            sim = Simulation(headless = True)
            QApplication.shutdown(app)
            sys.exit(0)
        elif args[0] == "tests" or arg == "tests":
            sim = Simulation(headless = True, tests = True)
            QApplication.shutdown(app)
            sys.exit(0)
        elif len(args) > 1:
            print(f"Invalid arguments: {args}")
            logging.error("Invalid arguments: %s", args)
            sys.exit(1)
        else:
            print(f"Invalid argument: {args[0]}")
            logging.error("Invalid argument: %s", args[0])
            sys.exit(1)
    else:
        sim = Simulation()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
