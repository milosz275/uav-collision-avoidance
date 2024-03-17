""""""

from math import cos, radians
from typing import List

from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QKeyEvent, \
    QMouseEvent, QIcon, QPixmap, QCloseEvent, QVector3D
from PySide6.QtWidgets import QWidget, QApplication

from src.aircraft.aircraft import Aircraft
from src.aircraft.aircraft_fcc import AircraftFCC
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_render import AircraftRender
from src.simulation.simulation_fps import SimulationFPS
from src.simulation.simulation_settings import SimulationSettings

class SimulationWidget(QWidget):
    """Main widget representing the simulation"""
    stop_signal = Signal(str)
    def __init__(self, aircrafts : List[Aircraft],
                 simulation_fps : SimulationFPS, simulation_state : SimulationSettings):
        super().__init__()
        self.aircrafts = aircrafts
        self.aircraft_vehicles : List[AircraftVehicle] = [
            aircraft.vehicle() for aircraft in self.aircrafts]
        self.aircraft_fccs : List[AircraftFCC] = [
            aircraft.fcc() for aircraft in self.aircrafts]
        self.aircraft_renders : List[AircraftRender] = [
            aircraft.render() for aircraft in self.aircrafts]
        self.simulation_fps = simulation_fps
        self.simulation_state = simulation_state

        self.bounding_box_resolution = [SimulationSettings.resolution[0], SimulationSettings.resolution[1]]
        window_width : float = SimulationSettings.resolution[0] + 10
        window_height : float = SimulationSettings.resolution[1] + 10
        self.setGeometry(
            SimulationSettings.screen_resolution.width() / 2 - window_width / 2,
            SimulationSettings.screen_resolution.height() / 2 - window_height / 2,
            window_width,
            window_height)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle(QApplication.applicationName() + " " + QApplication.applicationVersion())

        self.icon = QIcon()
        self.icon.addPixmap(self.simulation_state.aircraft_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)
        return
    
    def update_aircrafts(self) -> None:
        """Updates aircrafts position"""
        for aircraft in self.aircraft_renders:
            aircraft.update()
        return

    def paintEvent(self, event: QPaintEvent) -> None:
        """Qt method painting the aircrafts"""
        if self.simulation_state.aircraft_pixmap.isNull():
            return super().paintEvent(event)
        self.simulation_fps.count_frame()
        for aircraft in self.aircraft_renders:
            pixmap : QPixmap = self.simulation_state.aircraft_pixmap.scaled(
                aircraft.size * abs(cos(radians(aircraft.roll_angle))),
                aircraft.size * abs(cos(radians(aircraft.pitch_angle)))
            )
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
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
            painter = QPainter(self)
            painter.setBrush(Qt.BrushStyle.SolidPattern)
            for destination in aircraft.fcc.destinations:
                painter.drawEllipse(
                    destination.x() * self.simulation_state.gui_scale - 5,
                    destination.y() * self.simulation_state.gui_scale - 5,
                    10, 10)
            painter.end()
        return super().paintEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling single click mouse input"""
        print("click x: " + str(event.pos().x() / self.simulation_state.gui_scale) + "; y: " + str(event.pos().y() / self.simulation_state.gui_scale))
        if event.button() == Qt.MouseButton.LeftButton:
            self.aircraft_fccs[0].push_destination_top(QVector3D(
                float(event.pos().x() / self.simulation_state.gui_scale),
                float(event.pos().y() / self.simulation_state.gui_scale),
                1000.0))
        elif event.button() == Qt.MouseButton.RightButton:
            self.aircraft_fccs[0].append_destination(QVector3D(
                float(event.pos().x() / self.simulation_state.gui_scale),
                float(event.pos().y() / self.simulation_state.gui_scale),
                1000.0))
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.aircraft_vehicles[0].teleport(
                float(event.pos().x() / self.simulation_state.gui_scale),
                float(event.pos().y() / self.simulation_state.gui_scale),
                1000.0)
        return super().mousePressEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling double click mouse input"""
        QApplication.beep()
        return super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Qt method controlling keyboard input"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Slash:
            self.simulation_state.toggle_pause()
        elif event.key() == Qt.Key.Key_R:
            self.simulation_state.reset()
        if self.aircrafts[0]:
            if event.key() == Qt.Key.Key_A:
                self.aircraft_fccs[0].target_yaw_angle = -90.0
            elif event.key() == Qt.Key.Key_D:
                self.aircraft_fccs[0].target_yaw_angle = 90.0
            elif event.key() == Qt.Key.Key_W:
                self.aircraft_fccs[0].target_yaw_angle = 0.0
            elif event.key() == Qt.Key.Key_S:
                self.aircraft_fccs[0].target_yaw_angle = 180.0
        if self.aircrafts[1]:
            if event.key() == Qt.Key.Key_Left:
                self.aircraft_fccs[1].target_yaw_angle = -90.0
            elif event.key() == Qt.Key.Key_Right:
                self.aircraft_fccs[1].target_yaw_angle = 90.0
            elif event.key() == Qt.Key.Key_Up:
                self.aircraft_fccs[1].target_yaw_angle = 0.0
            elif event.key() == Qt.Key.Key_Down:
                self.aircraft_fccs[1].target_yaw_angle = 180.0
        return super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        self.stop_signal.emit("stop")
        event.accept()
        return super().closeEvent(event)
