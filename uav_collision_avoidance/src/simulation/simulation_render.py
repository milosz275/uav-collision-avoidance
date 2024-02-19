# simulation_render.py

import sys
from copy import copy
from typing import List
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGraphicsPixmapItem, QLabel
from PySide6.QtCore import Qt, QObject, QThread, Signal, QPoint
from PySide6.QtGui import QPaintEvent, QPainter, QColor, QBrush, QKeyEvent, QIcon, QTransform, QImage, QPicture, QPixmap

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

        self.painter : QPainter = None

        self.icon = QIcon()
        self.icon.addPixmap(self.simulation_state.aircraft_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.aircrafts = aircrafts
        
        for aircraft in self.aircrafts:
            aircraft.positionChanged.connect(self.update)
        return

    def paintEvent(self, event: QPaintEvent) -> None:
        for aircraft in self.aircrafts:
            pixmap = self.simulation_state.aircraft_pixmap.scaled(aircraft.size, aircraft.size)

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.translate(QPoint(
                aircraft.position.x(),
                aircraft.position.y()))

            transform = QTransform()
            transform.rotate(aircraft.yaw_angle)
            rotated_pixmap : QPixmap = pixmap.transformed(transform)
            
            painter.drawPixmap(
                int(aircraft.position.x()),
                int(aircraft.position.y()),
                rotated_pixmap)
            painter.end()
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
