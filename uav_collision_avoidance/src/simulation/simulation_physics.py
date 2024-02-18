# simulation_physics.py

import sys
from typing import List
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class SimulationPhysics(QThread):
    """Thread running simulation's physics"""

    def __init__(self, parent, aircrafts : List[AircraftVehicle], simulation_state : SimulationState) -> None:
        super(SimulationPhysics, self).__init__(parent)
        self.aircrafts = aircrafts
        self.simulation_state = simulation_state
        return
        
    def run(self) -> None:
        while not self.isInterruptionRequested():
            if not self.simulation_state.is_paused:
                for aircraft in self.aircrafts:
                    aircraft.move(1, 1, 0)
            self.msleep(self.simulation_state.simulation_threshold)
        return super().run()
