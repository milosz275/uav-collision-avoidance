# simulation_render.py

from math import cos, radians
from typing import List

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QKeyEvent, QIcon, QTransform, QPixmap, QCloseEvent

from src.aircraft.aircraft_render import AircraftRender
from src.simulation.simulation_settings import SimulationSettings

class SimulationRender(QWidget):
    """Main widget rendering the simulation"""

    rendered = Signal(bool)

    def __init__(self, aircrafts : List[AircraftRender], simulation_state):
        super().__init__()
        self.simulation_state = simulation_state

        self.bounding_box_resolution = [SimulationSettings.resolution[0], SimulationSettings.resolution[1]]
        self.setGeometry(0, 0, SimulationSettings.resolution[0] + 10, SimulationSettings.resolution[1] + 10)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("UAV Collision Avoidance")

        self.painter : QPainter = None

        self.icon = QIcon()
        self.icon.addPixmap(self.simulation_state.aircraft_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.aircrafts = aircrafts
        
        for aircraft in self.aircrafts:
            aircraft.position_changed.connect(self.update)
        return

    def paintEvent(self, event: QPaintEvent) -> None:
        """Qt method painting the aircrafts"""
        if self.simulation_state.aircraft_pixmap.isNull():
            return super().paintEvent(event)
        for aircraft in self.aircrafts:
            self.rendered.emit(True)
            
            pixmap : QPixmap = self.simulation_state.aircraft_pixmap.scaled(aircraft.size, aircraft.size)

            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.translate(QPoint(
                aircraft.position.x(),
                aircraft.position.y()))
            pixmap = pixmap.scaled(
                pixmap.width() * abs(cos(radians(aircraft.roll_angle))),
                pixmap.height() * abs(cos(radians(aircraft.pitch_angle))))
            
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
        """Qt method controlling keyboard input"""
        if event.key() == Qt.Key.Key_Slash:
            self.simulation_state.toggle_pause()
        step = 5
        for aircraft in self.aircrafts:
            if aircraft.aircraft_id == "0":
                if event.key() == Qt.Key.Key_A:
                    aircraft.move(-step, 0)
                elif event.key() == Qt.Key.Key_D:
                    aircraft.move(step, 0)
                elif event.key() == Qt.Key.Key_W:
                    aircraft.move(0, -step)
                elif event.key() == Qt.Key.Key_S:
                    aircraft.move(0, step)
            elif aircraft.aircraft_id == "1":
                if event.key() == Qt.Key.Key_Left:
                    aircraft.move(-step, 0)
                elif event.key() == Qt.Key.Key_Right:
                    aircraft.move(step, 0)
                elif event.key() == Qt.Key.Key_Up:
                    aircraft.move(0, -step)
                elif event.key() == Qt.Key.Key_Down:
                    aircraft.move(0, step)
        return super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        for aircraft in self.aircrafts:
            aircraft.disconnect_vehicle()
            aircraft.position_changed.disconnect(self.update)
        event.accept()
        return super().closeEvent(event)
