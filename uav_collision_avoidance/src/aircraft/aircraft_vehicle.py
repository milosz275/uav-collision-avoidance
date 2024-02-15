# aircraft_vehicle.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent

class AircraftVehicle(QObject):
    positionChanged = Signal(float, float)

    def __init__(self, x : float, y : float, speed : float):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.positionChanged.emit(self.x, self.y)
