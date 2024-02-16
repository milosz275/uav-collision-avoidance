# simulation_render.py

import sys
from typing import List
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush, QKeyEvent

from src.aircraft.aircraft_render import AircraftRender

class SimulationRender(QWidget):
    def __init__(self, aircrafts : List[AircraftRender], simulator):
        super().__init__()
        self.aircrafts = aircrafts
        self.simulator = simulator
        for aircraft in self.aircrafts:
            aircraft.positionChanged.connect(self.update)
        return

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        for aircraft in self.aircrafts:
            painter.setBrush(QColor(aircraft.color))
            painter.drawRect(int(aircraft.x), int(aircraft.y), 50, 50)
        return super().paintEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Slash:
            self.simulator.toggle_pause()
        step = 5
        for aircraft in self.aircrafts:
            if aircraft.color == "blue":
                if event.key() == Qt.Key.Key_A:
                    aircraft.move(-step, 0)
                elif event.key() == Qt.Key.Key_D:
                    aircraft.move(step, 0)
                elif event.key() == Qt.Key.Key_W:
                    aircraft.move(0, -step)
                elif event.key() == Qt.Key.Key_S:
                    aircraft.move(0, step)
            else:
                if event.key() == Qt.Key.Key_Left:
                    aircraft.move(-step, 0)
                elif event.key() == Qt.Key.Key_Right:
                    aircraft.move(step, 0)
                elif event.key() == Qt.Key.Key_Up:
                    aircraft.move(0, -step)
                elif event.key() == Qt.Key.Key_Down:
                    aircraft.move(0, step)
        return super().keyPressEvent(event)
