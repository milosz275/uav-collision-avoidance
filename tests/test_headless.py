import sys
import pytest
from PySide6.QtWidgets import QApplication
from main import *
from . import Simulation, SimulationSettings

def test_headless():
    with pytest.raises(SystemExit) as e:
        main("headless")
    assert e.value.code == 0

def test_headless_csv():
    with pytest.raises(SystemExit) as e:
        app = QApplication()
        SimulationSettings.__init__()
        sim = Simulation(headless = True)
        assert sim.load_simulation_data_from_file("data/simulation-2024-05-27-22-38-23.csv", test_id = 0, avoid_collisions = False)
        sim.run_headless(avoid_collisions = False)
        assert sim.load_simulation_data_from_file("data/simulation-2024-05-27-22-38-23.csv", test_id = 0, avoid_collisions = True)
        sim.run_headless(avoid_collisions = True)
        QApplication.shutdown(app)
        sys.exit(0)
    assert e.value.code == 0
