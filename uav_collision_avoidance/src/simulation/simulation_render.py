# simulation_render.py

import sys
from typing import List
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QObject, QThread, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush, QKeyEvent, QIcon

from src.aircraft.aircraft_render import AircraftRender
from src.simulation.simulation_settings import SimulationSettings

class SimulationRender(QWidget):
    """Main widget rendering the simulation"""

    def __init__(self, aircrafts : List[AircraftRender], simulation_state):
        super().__init__()
        self.simulation_state = simulation_state

        self.bounding_box_resolution = [SimulationSettings.resolution[0], SimulationSettings.resolution[1]]
        self.setGeometry(0, 0, SimulationSettings.resolution[0] + 10, SimulationSettings.resolution[1] + 10)
        self.setWindowTitle("UAV Collision Avoidance")

        self.icon = QIcon()
        self.icon.addPixmap(self.simulation_state.aircraft_image, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.aircrafts = aircrafts
        
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
            self.simulation_state.toggle_pause()
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
