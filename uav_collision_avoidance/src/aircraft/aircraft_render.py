# aircraft_render.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent, QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class AircraftRender(QObject):
    """Aircraft graphical representation"""

    positionChanged = Signal(float, float, float)

    def __init__(self, color : str, vehicle : AircraftVehicle, state : SimulationState) -> None:
        super().__init__()
        self.position : QVector3D = QVector3D(0, 0, 0)
        self.color = color
        self.state = state

        self.size : float = 0.0
        self.yaw_angle : float = 45.0
        self.safezone_occupied : bool = False

        if vehicle:
            self.vehicle = vehicle
            self.vehicle.positionChanged.connect(self.update)
        return
    
    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        self.vehicle.move(dx, dy, dz)
        return

    def set_vehicle(self, vehicle) -> None:
        if not self.vehicle:
            self.vehicle = vehicle
            self.vehicle.positionChanged.connect(self.update)
        return

    def update(self) -> None:
        self.position.setX(self.vehicle.position.x() / self.state.scale)
        self.position.setY(self.vehicle.position.y() / self.state.scale)
        self.position.setZ(self.vehicle.position.z() / self.state.scale)
        self.positionChanged.emit(self.position.x(), self.position.y(), self.position.z())
        self.size = self.vehicle.size / self.state.scale
        self.yaw_angle = self.vehicle.yaw_angle()
        self.safezone_occupied = self.vehicle.safezone_occupied
        return
