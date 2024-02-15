# aircraft_render.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent

from src.aircraft.aircraft_vehicle import AircraftVehicle

class AircraftRender(QObject):
    positionChanged = Signal(float, float)

    def __init__(self, color : str, vehicle : AircraftVehicle):
        super().__init__()
        self.scale = 1
        self.x = 0
        self.y = 0
        self.color = color
        if vehicle:
            self.vehicle = vehicle
            self.vehicle.positionChanged.connect(self.update)

    def set_vehicle(self, vehicle):
        if not self.vehicle:
            self.vehicle = vehicle
            self.vehicle.positionChanged.connect(self.update)

    def update(self):
        self.x = self.vehicle.x / self.scale
        self.y = self.vehicle.y / self.scale
        self.positionChanged.emit(self.x, self.y)
