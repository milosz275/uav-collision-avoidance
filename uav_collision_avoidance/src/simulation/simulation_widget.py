"""Simulation widget for the main window of the simulation app"""

from copy import copy
from math import cos, radians, sqrt, degrees, atan2
from typing import List

from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QKeyEvent, \
    QMouseEvent, QIcon, QPixmap, QCloseEvent, QVector3D, QPolygonF, QWheelEvent
from PySide6.QtWidgets import QWidget, QApplication

from src.aircraft.aircraft import Aircraft
from src.aircraft.aircraft_fcc import AircraftFCC
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_fps import SimulationFPS
from src.simulation.simulation_settings import SimulationSettings

class SimulationWidget(QWidget):
    """Main widget representing the simulation"""
    stop_signal = Signal(str)
    def __init__(self, aircrafts : List[Aircraft],
                 simulation_fps : SimulationFPS, simulation_state : SimulationSettings) -> None:
        super().__init__()
        self.aircrafts = aircrafts
        self.aircraft_vehicles : List[AircraftVehicle] = [
            aircraft.vehicle for aircraft in self.aircrafts]
        self.aircraft_fccs : List[AircraftFCC] = [
            aircraft.fcc for aircraft in self.aircrafts]
        self.simulation_fps = simulation_fps
        self.simulation_state = simulation_state

        self.bounding_box_resolution = [SimulationSettings.resolution[0], SimulationSettings.resolution[1]]
        self.window_width : float = SimulationSettings.resolution[0] + 10
        self.window_height : float = SimulationSettings.resolution[1] + 10
        self.screen_offset_x : float = 0.0
        self.screen_offset_y : float = 0.0
        self.setGeometry(
            SimulationSettings.screen_resolution.width() / 2 - self.window_width / 2,
            SimulationSettings.screen_resolution.height() / 2 - self.window_height / 2,
            self.window_width,
            self.window_height)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle(QApplication.applicationName() + " " + QApplication.applicationVersion())

        self.icon = QIcon()
        self.icon.addPixmap(self.simulation_state.aircraft_pixmap, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

    def draw_aircraft(self, aircraft : AircraftVehicle, scale : float) -> None:
        """Draws given aircraft vehicle"""
        yaw_angle : float = aircraft.yaw_angle
        size : float = aircraft.size * scale
        pixmap : QPixmap = self.simulation_state.aircraft_pixmap.scaled(
            size * abs(cos(radians(aircraft.roll_angle))),
            size * abs(cos(radians(aircraft.pitch_angle)))
        )

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.translate(QPointF(
            (aircraft.position.x() * scale) + x_offset,
            (aircraft.position.y() * scale) + y_offset))
        painter.rotate(yaw_angle)
        painter.translate(QPointF(
            (- size / 2) - x_offset,
            (- size / 2) - y_offset))
        painter.drawPixmap(x_offset, y_offset, pixmap)
        painter.drawEllipse(x_offset, y_offset,
            size * abs(cos(radians(aircraft.roll_angle))),
            size * abs(cos(radians(aircraft.pitch_angle))))
        painter.rotate(-yaw_angle)
        painter.end()
        self.draw_text(aircraft.position, scale, f"Aircraft {aircraft.aircraft_id}")
        return

    def draw_destinations(self, aircraft : AircraftVehicle, scale : float) -> None:
        """Draws destinations of given aircraft vehicle"""
        for idx, destination in enumerate(self.aircraft_fccs[aircraft.aircraft_id].destinations):
            self.draw_disk(destination, 10, scale)
            self.draw_text(destination, scale, f"Destination {idx} of Aircraft {aircraft.aircraft_id}")
        return

    def draw_text(self, point : QVector3D, scale : float, text : str) -> None:
        """Draws text at given coordinates"""
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        if scale != 0:
            painter.drawText(
                ((point.x() + 10) * scale) + x_offset,
                ((point.y() + 10) * scale) + y_offset,
                text)
        else:
            painter.drawText(
                point.x(),
                point.y(),
                text)
        painter.end()
        return

    def draw_circle(self, point : QVector3D, size : float, scale : float) -> None:
        """Draws circle at given coordinates (empty)"""
        painter = QPainter(self)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.drawEllipse(
            point.x() * scale - (size * scale / 2) + x_offset,
            point.y() * scale - (size * scale / 2) + y_offset,
            size * scale,
            size * scale)
        painter.end()
        return
    
    def draw_disk(self, point : QVector3D, size : float, scale : float) -> None:
        """Draws disk at given coordinates (full)"""
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.drawEllipse(
            point.x() * scale - (size * scale / 2) + x_offset,
            point.y() * scale - (size * scale / 2) + y_offset,
            size * scale,
            size * scale)
        painter.end()
        return

    def draw_line(self, point1 : QVector3D, point2 : QVector3D, scale : float) -> None:
        """Draws line connecting given points"""
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.drawLine(
            int((point1.x() * scale) + x_offset),
            int((point1.y() * scale) + y_offset),
            int((point2.x() * scale) + x_offset),
            int((point2.y() * scale) + y_offset))
        painter.end()
        return

    def draw_vector(self, point1 : QVector3D, point2 : QVector3D, scale : float) -> None:
        """Draws vector pointing from first to second point"""
        self.draw_line(point1, point2, scale)
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        angle = degrees(atan2(point1.x() - point2.x(), point1.y() - point2.y()))
        arrowhead_size = SimulationSettings.screen_resolution.width() / 400 * scale
        arrowhead_height = arrowhead_size * sqrt(3) / 2
        polygon = QPolygonF()
        polygon.append(
            QPointF(
                (point2.x() * scale - arrowhead_size / 2) + x_offset,
                (point2.y() * scale + arrowhead_height / 3) + y_offset))
        polygon.append(
            QPointF(
                (point2.x() * scale + arrowhead_size / 2) + x_offset,
                (point2.y() * scale + arrowhead_height / 3) + y_offset))
        polygon.append(
            QPointF(
                (point2.x() * scale) + x_offset,
                (point2.y() * scale - 2 * arrowhead_height / 3) + y_offset))
        painter.translate(
            (point2.x() * scale) + x_offset,
            (point2.y() * scale) + y_offset
        )
        painter.rotate(-angle)
        painter.translate(
            (- point2.x() * scale) - x_offset,
            (- point2.y() * scale) - y_offset
        )
        painter.drawPolygon(polygon)
        painter.end()
        return

    def draw_miss_distance_vector(self, aircraft: AircraftVehicle, other_aircraft: AircraftVehicle, scale: float) -> None:
        """Draws miss distance vector for given aircraft vehicle"""
        # todo
        return

    def paintEvent(self, event : QPaintEvent) -> None:
        """Qt method painting the aircrafts"""
        if self.simulation_state.aircraft_pixmap.isNull():
            return super().paintEvent(event)
        self.simulation_fps.count_frame()
        scale : float = self.simulation_state.gui_scale
        if self.simulation_state.draw_fps:
            self.draw_text(QVector3D(10, 10, 0), 0, "FPS: " + "{:.2f}".format(self.simulation_state.fps))
        if self.simulation_state.draw_grid:
            for x in range(0, int(self.window_width / scale), 100):
                self.draw_line(QVector3D(x, 0, 0), QVector3D(x, self.window_height / scale, 0), scale)
            for y in range(0, int(self.window_height / scale), 100):
                self.draw_line(QVector3D(0, y, 0), QVector3D(self.window_width / scale, y, 0), scale)
        for aircraft in self.aircraft_vehicles:
            if self.simulation_state.draw_aircraft:
                self.draw_aircraft(aircraft, scale)
                self.draw_destinations(aircraft, scale)
            if self.simulation_state.draw_speed_vectors:
                self.draw_vector(aircraft.position, aircraft.position + aircraft.speed, scale)
            if self.simulation_state.draw_safezones:
                self.draw_circle(aircraft.position, self.aircraft_fccs[aircraft.aircraft_id].safezone_size, scale)
            if self.simulation_state.draw_miss_distance and aircraft.aircraft_id == 0:
                self.draw_miss_distance_vector(aircraft, self.aircraft_vehicles[1 - aircraft.aircraft_id], scale)
        return super().paintEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling single click mouse input"""
        scale : float = self.simulation_state.gui_scale
        click_x : int = event.pos().x()
        click_y : int = event.pos().y()
        real_x : float = click_x / scale - (self.screen_offset_x / scale)
        real_y : float = click_y / scale - (self.screen_offset_y / scale)
        print(
            "click: physical coords: x: " + "{:.2f}".format(real_x) +
            "; y: " + "{:.2f}".format(real_y) +
            " | window coords: x: " + "{:.2f}".format(click_x) +
            "; y: " + "{:.2f}".format(click_y))
        if event.button() == Qt.MouseButton.LeftButton:
            self.aircraft_fccs[0].add_first_destination(QVector3D(
                real_x,
                real_y,
                1000.0))
        elif event.button() == Qt.MouseButton.RightButton:
            self.aircraft_fccs[0].add_last_destination(QVector3D(
                real_x,
                real_y,
                1000.0))
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.aircraft_vehicles[0].position = QVector3D(
                real_x,
                real_y,
                1000.0)
        return super().mousePressEvent(event)
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        """Qt method controlling mouse wheel input"""
        if event.angleDelta().y() > 0:
            self.simulation_state.gui_scale += 0.125
        else:
            self.simulation_state.gui_scale -= 0.125
        return super().wheelEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling double click mouse input"""
        QApplication.beep()
        return super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Qt method controlling keyboard input"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Slash:
            if event.isAutoRepeat():
                return super().keyPressEvent(event)
            self.simulation_state.toggle_pause()
        elif event.key() == Qt.Key.Key_R:
            if event.isAutoRepeat():
                return super().keyPressEvent(event)
            self.simulation_state.reset()
        elif event.key() == Qt.Key.Key_Plus:
            self.simulation_state.gui_scale += 0.25
        elif event.key() == Qt.Key.Key_Minus:
            self.simulation_state.gui_scale -= 0.25
        elif event.key() == Qt.Key.Key_F1:
            self.simulation_state.toggle_adsb_report()
        elif event.key() == Qt.Key.Key_F2:
            self.aircraft_fccs[0].target_speed -= 10.0
        elif event.key() == Qt.Key.Key_F3:
            self.aircraft_fccs[0].target_speed += 10.0
        elif event.key() == Qt.Key.Key_Left:
            self.screen_offset_x -= 10.0
        elif event.key() == Qt.Key.Key_Right:
            self.screen_offset_x += 10.0
        elif event.key() == Qt.Key.Key_Up:
            self.screen_offset_y -= 10.0
        elif event.key() == Qt.Key.Key_Down:
            self.screen_offset_y += 10.0
        if self.aircrafts[0]:
            if event.key() == Qt.Key.Key_A:
                self.aircraft_fccs[0].target_yaw_angle = -90.0
            elif event.key() == Qt.Key.Key_D:
                self.aircraft_fccs[0].target_yaw_angle = 90.0
            elif event.key() == Qt.Key.Key_W:
                self.aircraft_fccs[0].target_yaw_angle = 0.0
            elif event.key() == Qt.Key.Key_S:
                self.aircraft_fccs[0].target_yaw_angle = 180.0
        return super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        """Qt method controlling keyboard input"""
        if event.key() == Qt.Key.Key_Slash and event.isAutoRepeat() and self.simulation_state.is_paused:
            self.simulation_state.toggle_pause()
        return super().keyReleaseEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        self.stop_signal.emit("stop")
        event.accept()
        return super().closeEvent(event)
