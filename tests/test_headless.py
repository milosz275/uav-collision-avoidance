import sys
import pytest
from PySide6.QtWidgets import QApplication
from main import *
from . import Simulation, SimulationSettings

def test_headless():
        with pytest.raises(SystemExit) as e:
            main("headless")
        assert e.value.code == 0

test_path : str = "data/simulation-2024-06-08-15-52-45.csv"
lowest_frequency_tested : int = 10
highest_frequency_tested : int = 100

@pytest.fixture
def tester(request):
    """Creates headless testing object"""
    return TestHeadless(request.param)

class Test:
    @pytest.mark.parametrize("tester", list(range(lowest_frequency_tested, highest_frequency_tested + 1, 10)), indirect=["tester"])
    def test_tc1(self, tester):
       tester.test_headless_load()

class TestHeadless:
    """Test headless simulation"""
    def __init__(self, simulation_frequency : float):
        self.simulation_frequency = simulation_frequency

    def test_headless_load(self):
        with pytest.raises(SystemExit) as e:
            app = QApplication.instance()
            if app:
                app.quit()
            app = QApplication()
            SimulationSettings.__init__()
            SimulationSettings.set_simulation_frequency(self.simulation_frequency)
            sim = Simulation(headless = True)
            assert sim.load_simulation_data_from_file(test_path, test_id = 0, avoid_collisions = False)
            sim.run_headless(avoid_collisions = False)
            assert sim.load_simulation_data_from_file(test_path, test_id = 0, avoid_collisions = True)
            sim.run_headless(avoid_collisions = True)
            QApplication.shutdown(app)
            sys.exit(0)
        assert e.value.code == 0
