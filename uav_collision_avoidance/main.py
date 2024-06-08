"""Main module for UAV Collision Avoidance application"""

import signal
import logging
import platform
import datetime
import multiprocessing
from pathlib import Path
from screeninfo import get_monitors

from PySide6.QtWidgets import QApplication
from .version import __version__ as version
from .src.simulation.simulation import Simulation, SimulationSettings

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
    
def signal_handler(sig, frame) -> None:
    logging.warning("Ctrl+C keyboard interrupt. Exiting...")
    try:
        signal.default_int_handler(sig, frame)
    except KeyboardInterrupt:
        import sys
        sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)

logging.info("-" * 120)
if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        f"io.github.mldxo.uav-collision-avoidance.{version}")
logging.info("Detected platform: %s", platform.system())

def run_simulation_tests(test_number : int) -> None:
    sim : Simulation = Simulation(headless = True, tests = True)
    if test_number > 0:
        sim.run_tests(test_number)
    else:
        sim.run()

def main(arg = None) -> None:
    """Executes main function"""
    import sys
    args = sys.argv[1:]
    app = QApplication(args)
    app.setApplicationName("UAV Collision Avoidance")
    app.setApplicationVersion(version)
    SimulationSettings.screen_resolution = app.primaryScreen().size()
    logging.info("%s %s", app.applicationName(), app.applicationVersion())
    sim : Simulation | None = None
    if len(args) > 0 or arg is not None:
        if args[0] == "realtime" or args[0] == "default" or args[0] == "gui":
            if len(get_monitors()) == 0:
                logging.warning("Launching GUI Application without monitors detected")
            sim = Simulation()
            if len(args) >= 2:
                file_path : str = args[1]
                test_id : int = 0
                avoid_collisions : bool = False
                if len(args) >= 3:
                    test_id = int(args[2])
                if len(args) >= 4:
                    avoidance : str = str(args[3])
                    if avoidance == "true" or avoidance == "True" or avoidance == "t" or avoidance == "T" or avoidance == "yes" or avoidance == "1":
                        avoid_collisions = True
                if len(args) >= 5:
                    print(f"Invalid arguments: {args}")
                    logging.warning("Invalid arguments: %s", args)
                sim.load_simulation_data_from_file(file_path = file_path, test_id = test_id, avoid_collisions = avoid_collisions)
                sim.run_gui(avoid_collisions = avoid_collisions, load_latest_data_file = False)
            else:
                sim.run()
            sys.exit(app.exec())
        elif args[0] == "headless" or arg == "headless":
            sim = Simulation(headless = True)
            sim.run()
            QApplication.shutdown(app)
            sys.exit(0)
        elif args[0] == "tests" or arg == "tests":
            sim = Simulation(headless = True, tests = True)
            if len(args) > 1 and int(args[1]) > 0:
                sim.run_tests(test_number = int(args[1]))
            else:
                sim.run()
            QApplication.shutdown(app)
            sys.exit(0)
        elif args[0] == "load":
            file_path : str = "data/simulation-2024-06-08-15-52-45.csv"
            test_id : int = 0
            if len(args) >= 2:
                file_path = args[1]
                if len(args) == 3:
                    test_id = int(args[2])
                if len(args) >= 4:
                    print(f"Invalid arguments: {args}")
                    logging.warning("Invalid arguments: %s", args)
            sim = Simulation(headless = True)
            assert sim.load_simulation_data_from_file(file_path = file_path, test_id = test_id, avoid_collisions = False)
            sim.run_headless(avoid_collisions = False)
            assert sim.load_simulation_data_from_file(file_path = file_path, test_id = test_id, avoid_collisions = True)
            sim.run_headless(avoid_collisions = True)
            QApplication.shutdown(app)
            sys.exit(0)
        elif args[0] == "ongoing":
            processes = []
            concurrent_tests = multiprocessing.cpu_count()
            logging.info("Running %d concurrent tests", concurrent_tests)
            logging.warning("Disabling logging because due to log storm")
            logging.disable()
            for i in range(concurrent_tests):
                process = multiprocessing.Process(target=run_simulation_tests, args=(i,))
                process.start()
                processes.append(process)
            for process in processes:
                process.join()
        elif args[0] == "help" and len(args) > 1:
            if args[1] == "realtime":
                print("Usage: uav_collision_avoidance realtime [file_path] [test_index] [collision_avoidance]")
                print("Description: Runs the simulation in real-time with GUI")
                sys.exit(0)
            elif args[1] == "headless":
                print("Usage: uav_collision_avoidance headless")
                print("Description: Runs the simulation in headless mode without GUI")
                sys.exit(0)
            elif args[1] == "tests":
                print("Usage: uav_collision_avoidance tests [test_number]")
                print("Description: Runs the simulation multiple times in headless mode without GUI defaulting to 10 times")
                sys.exit(0)
            elif args[1] == "load":
                print("Usage: uav_collision_avoidance load [file_path] [test_index]")
                print("Description: Loads a simulation data file and runs the simulation in headless mode without GUI, defaults to example data file")
                sys.exit(0)
            elif args[1] == "ongoing":
                print("Usage: uav_collision_avoidance ongoing")
                print("Description: Runs the simulation tests indefinitely")
                sys.exit(0)
            elif args[1] == "help":
                print("Usage: uav_collision_avoidance help [app_argument]")
                print("Description: Displays help information for the specified app argument")
                sys.exit(0)
            else:
                print(f"Invalid argument: {args[1]}")
                logging.error("Invalid argument: %s", args[1])
                sys.exit(1)
        elif args[0] == "help":
            print("Usage: uav_collision_avoidance [realtime|headless|tests|load|ongoing|help|version]")
            sys.exit(0)
        elif args[0] == "version":
            print(f"{app.applicationName()} {app.applicationVersion()}")
            sys.exit(0)
        elif len(args) > 1:
            print(f"Invalid arguments: {args}")
            logging.error("Invalid arguments: %s", args)
            sys.exit(1)
        else:
            print(f"Invalid argument: {args[0]}")
            print("Usage: uav_collision_avoidance [realtime|headless|tests|load|ongoing|help|version]")
            logging.error("Invalid argument: %s", args[0])
            sys.exit(1)
    else:
        sim = Simulation()
        sim.run()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
