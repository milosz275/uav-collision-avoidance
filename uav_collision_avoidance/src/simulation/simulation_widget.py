# simulation_widget.py

from math import cos, radians
from typing import List

from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QKeyEvent, QIcon, QPixmap, QCloseEvent
from PySide6.QtWidgets import QWidget

from src.aircraft.aircraft_render import AircraftRender
from src.simulation.simulation_fps import SimulationFPS
from src.simulation.simulation_settings import SimulationSettings

class SimulationWidget(QWidget):
    """Main widget representing the simulation"""
    stop_signal = Signal(str)

    def __init__(self, aircrafts : List[AircraftRender], simulation_fps : SimulationFPS, simulation_state : SimulationSettings):
        super().__init__()
        self.simulation_fps = simulation_fps
        self.simulation_state = simulation_state

        self.bounding_box_resolution = [SimulationSettings.resolution[0], SimulationSettings.resolution[1]]
        self.setGeometry(0, 0, SimulationSettings.resolution[0] + 10, SimulationSettings.resolution[1] + 10)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("UAV Collision Avoidance")

        self.icon = QIcon()
        self.icon.addPixmap(self.simulation_state.aircraft_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.aircrafts = aircrafts
        return

    def paintEvent(self, event: QPaintEvent) -> None:
        """Qt method painting the aircrafts"""
        if self.simulation_state.aircraft_pixmap.isNull():
            return super().paintEvent(event)
        self.simulation_fps.count_frame()
        for aircraft in self.aircrafts:
            pixmap : QPixmap = self.simulation_state.aircraft_pixmap.scaled(aircraft.size, aircraft.size)
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            pixmap = pixmap.scaled(
                aircraft.size * abs(cos(radians(aircraft.roll_angle))),
                aircraft.size * abs(cos(radians(aircraft.pitch_angle))))
            painter.translate(QPointF(
                aircraft.position.x(),
                aircraft.position.y()))
            painter.rotate(aircraft.yaw_angle)
            painter.translate(QPointF(
                -aircraft.size / 2,
                -aircraft.size / 2))
            painter.drawPixmap(0, 0, pixmap)
            painter.drawEllipse(0, 0,
                aircraft.size * abs(cos(radians(aircraft.roll_angle))),
                aircraft.size * abs(cos(radians(aircraft.pitch_angle))))
            painter.end()
        return super().paintEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Qt method controlling keyboard input"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Slash:
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
        self.stop_signal.emit("stop")
        event.accept()
        return super().closeEvent(event)

    def update_aircrafts(self) -> None:
        """Updates aircrafts position"""
        for aircraft in self.aircrafts:
            aircraft.update()
        return
