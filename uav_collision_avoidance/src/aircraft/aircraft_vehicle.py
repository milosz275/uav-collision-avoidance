# aircraft_vehicle.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent, QVector3D

from src.simulation.simulation_state import SimulationState

class AircraftVehicle(QObject):
    """Aircraft physical UAV"""

    positionChanged = Signal(float, float)

    def __init__(self, position : QVector3D, speed : QVector3D, state : SimulationState) -> None:
        super().__init__()
        self.position = position
        self.speed = speed
        self.state = state
        return

    def move(self, dx, dy) -> None:
        self.x += dx
        self.y += dy
        self.positionChanged.emit(self.x, self.y)
        return
