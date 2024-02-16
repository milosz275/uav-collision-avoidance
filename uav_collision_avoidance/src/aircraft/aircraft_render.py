# aircraft_render.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class AircraftRender(QObject):
    """Aircraft graphical representation"""

    positionChanged = Signal(float, float, float)

    def __init__(self, color : str, vehicle : AircraftVehicle, state : SimulationState) -> None:
        super().__init__()
        self.x = 0
        self.y = 0
        self.z = 0
        self.color = color
        self.state = state
        if vehicle:
            self.vehicle = vehicle
            self.vehicle.positionChanged.connect(self.update)
        return
    
    def move(self, dx, dy, dz) -> None:
        self.vehicle.move(dx, dy, dz)
        return

    def set_vehicle(self, vehicle) -> None:
        if not self.vehicle:
            self.vehicle = vehicle
            self.vehicle.positionChanged.connect(self.update)
        return

    def update(self) -> None:
        self.x = self.vehicle.position.x / self.state.scale
        self.y = self.vehicle.position.y / self.state.scale
        self.z = self.vehicle.position.z / self.state.scale
        self.positionChanged.emit(self.x, self.y, self.z)
        return
