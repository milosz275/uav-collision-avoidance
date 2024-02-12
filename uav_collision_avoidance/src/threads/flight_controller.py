# flight_controller.py
from PySide6.QtCore import QThread

class FlightController(QThread):
    """Flight Controller"""

    def __init__(self, simulator):
        super().__init__()
        self.setParent(simulator)
        self.simulator = simulator

    def run(self):
        while not self.isInterruptionRequested():
            #self.simulator.collision_avoidance()
            self.msleep(1000)
