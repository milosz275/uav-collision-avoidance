import pytest
import sys
from PySide6.QtWidgets import QApplication
from main import *
from . import Simulation, SimulationSettings


def test_headless():
    with pytest.raises(SystemExit) as e:
        main("headless")
    assert e.value.code == 0

def test_physics():
    with pytest.raises(SystemExit) as e:
        app = QApplication()
        SimulationSettings.__init__()
        sim = Simulation(headless = True)
        assert sim is not None
        QApplication.shutdown(app)
        sys.exit(0)
    assert e.value.code == 0
