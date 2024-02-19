# aircraft_vehicle.py

import sys
from math import atan2, degrees
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent, QVector3D

from src.simulation.simulation_state import SimulationState

class AircraftVehicle(QObject):
    """Aircraft physical UAV"""

    positionChanged = Signal(float, float, float)

    def __init__(self, position : QVector3D, speed : QVector3D, state : SimulationState) -> None:
        super().__init__()
        self.position = position
        if self.position.z() < 0:
            self.position.setZ(0)
        self.speed = speed
        self.state = state

        self.size : float = 20.0
        self.safezone_occupied : bool = False

        return

    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        self.position.setX(self.position.x() + dx)
        self.position.setY(self.position.y() + dy)
        self.position.setZ(self.position.z() + dz)
        self.positionChanged.emit(self.position.x(), self.position.y(), self.position.z())
        return
    
    def absolute_speed(self) -> float:
        return self.speed.length()

    def yaw_angle(self) -> float:
        return degrees(atan2(self.speed.y(), self.speed.x()))
