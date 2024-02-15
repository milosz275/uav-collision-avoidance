# simulation_render.py

import sys
from typing import List
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPainter, QColor, QBrush, QKeyEvent

from src.aircraft.aircraft_render import AircraftRender

class SimulationRender(QWidget):
    def __init__(self, aircrafts : List[AircraftRender], simulator):
        super().__init__()
        self.aircrafts = aircrafts
        self.simulator = simulator
        for obj in self.aircrafts:
            obj.positionChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        for obj in self.aircrafts:
            painter.setBrush(QColor(obj.color))
            painter.drawRect(int(obj.x), int(obj.y), 50, 50)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Slash:
            self.simulator.toggle_pause()
        step = 5
        for obj in self.aircrafts:
            if obj.color == "blue":
                if event.key() == Qt.Key.Key_A:
                    obj.move(-step, 0)
                elif event.key() == Qt.Key.Key_D:
                    obj.move(step, 0)
                elif event.key() == Qt.Key.Key_W:
                    obj.move(0, -step)
                elif event.key() == Qt.Key.Key_S:
                    obj.move(0, step)
            else:
                if event.key() == Qt.Key.Key_Left:
                    obj.move(-step, 0)
                elif event.key() == Qt.Key.Key_Right:
                    obj.move(step, 0)
                elif event.key() == Qt.Key.Key_Up:
                    obj.move(0, -step)
                elif event.key() == Qt.Key.Key_Down:
                    obj.move(0, step)
        return super().keyPressEvent(event)
