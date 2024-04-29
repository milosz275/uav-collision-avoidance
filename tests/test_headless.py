import pytest
import sys
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
        sim.load_simulation_data_from_file("../data/simulation-2024-04-29-23-14-57.csv")
        sim.run()
        assert sim is not None
        QApplication.shutdown(app)
        sys.exit(0)
    assert e.value.code == 0
