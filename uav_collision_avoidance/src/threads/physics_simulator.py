# physics_simulator.py
from PySide6.QtCore import QThread, QElapsedTimer

class PhysicsSimulator(QThread):
    """Physics Simulator"""

    def __init__(self, simulator):
        super().__init__()
        self.setParent(simulator)
        #self.timer = QElapsedTimer()
        #self.timer.start()
        self.simulator = simulator

    def run(self):
        while not self.isInterruptionRequested():
            if not self.simulator.simulation_paused:
                #self.timer.restart()
                self.simulator.update_simulation()
                #if self.timer.elapsed() < 200:
                #    self.msleep(200 - self.timer.elapsed())
            else:
                self.msleep(200)
