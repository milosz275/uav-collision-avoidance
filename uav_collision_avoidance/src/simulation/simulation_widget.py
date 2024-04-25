"""Simulation widget for the main window of the simulation app"""

from copy import copy
from math import cos, radians, sqrt, degrees, atan2, dist
from typing import List

from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QKeyEvent, \
    QMouseEvent, QIcon, QPixmap, QCloseEvent, QVector3D, QPolygonF, QWheelEvent, QColor
from PySide6.QtWidgets import QWidget, QApplication

from ..aircraft.aircraft import Aircraft
from ..aircraft.aircraft_fcc import AircraftFCC
from ..aircraft.aircraft_vehicle import AircraftVehicle
from .simulation_fps import SimulationFPS
from .simulation_settings import SimulationSettings

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

        self.window_width : float = SimulationSettings.resolution[0]
        self.window_height : float = SimulationSettings.resolution[1]
        self.screen_offset_x : float = 0.0
        self.screen_offset_y : float = 0.0
        self.setGeometry(
            SimulationSettings.screen_resolution.width() / 2 - self.window_width / 2,
            SimulationSettings.screen_resolution.height() / 2 - self.window_height / 2 - 30,
            self.window_width,
            self.window_height)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle(QApplication.applicationName() + " " + QApplication.applicationVersion())

        self.icon = QIcon()
        self.icon.addPixmap(self.generate_icon(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.__moving_view_up : bool = False
        self.__moving_view_down : bool = False
        self.__moving_view_left : bool = False
        self.__moving_view_right : bool = False
        self.__steering_left : bool = False
        self.__steering_right : bool = False
        self.__steering_up : bool = False
        self.__steering_down : bool = False

        self.center_offsets()

    def generate_icon(self) -> QPixmap:
        """Returns icon for the main window"""
        pixmap = QPixmap(self.simulation_state.aircraft_pixmap)
        painter = QPainter(pixmap)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(self.simulation_state.aircraft_pixmap.rect())
        painter.drawPixmap(
            self.simulation_state.aircraft_pixmap.width() * 0.125,
            self.simulation_state.aircraft_pixmap.height() * 0.125,
            self.simulation_state.aircraft_pixmap.scaled(self.simulation_state.aircraft_pixmap.width() * 0.75,
            self.simulation_state.aircraft_pixmap.height() * 0.75))
        painter.end()
        return pixmap

    def draw_aircraft(self, aircraft : AircraftVehicle, scale : float) -> None:
        """Draws given aircraft vehicle"""
        yaw_angle : float = aircraft.yaw_angle
        size : float = aircraft.size * scale
        pixmap : QPixmap
        if not self.simulation_state.aircraft_pixmap.isNull():
            pixmap = self.simulation_state.aircraft_pixmap.scaled(
                size * abs(cos(radians(aircraft.roll_angle))),
                size * abs(cos(radians(aircraft.pitch_angle)))
            )
        else:
            pixmap = QPixmap(
                size * abs(cos(radians(aircraft.roll_angle))),
                size * abs(cos(radians(aircraft.pitch_angle))))
            pixmap.fill(Qt.GlobalColor.black)
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

    def draw_destinations(self, aircraft : AircraftVehicle, scale : float) -> None:
        """Draws destinations of given aircraft vehicle"""
        for idx, destination in enumerate(self.aircraft_fccs[aircraft.aircraft_id].destinations):
            self.draw_disk(destination, 2.5 / scale, scale)
            self.draw_text(destination, scale, f"Destination {idx} of Aircraft {aircraft.aircraft_id}")

    def draw_text(self, point : QVector3D, scale : float, text : str, color : QColor = QColor(0, 0, 0)) -> None:
        """Draws text at given coordinates"""
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        painter.setPen(color)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        if scale != 0:
            painter.drawText(
                QPointF(
                    ((point.x() + 10) * scale) + x_offset,
                    ((point.y() + 10) * scale) + y_offset),
                text)
        else:
            painter.drawText(
                QPointF(
                    point.x(),
                    point.y()),
                text)
        painter.end()

    def draw_circle(self, point : QVector3D, size : float, scale : float, color : QColor = QColor(0, 0, 0)) -> None:
        """Draws circle at given coordinates (empty)"""
        painter = QPainter(self)
        painter.setPen(color)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.drawEllipse(
            QPointF(
                point.x() * scale - (size * scale / 2) + x_offset,
                point.y() * scale - (size * scale / 2) + y_offset),
            float(size * scale),
            float(size * scale))
        painter.end()
    
    def draw_disk(self, point : QVector3D, size : float, scale : float, color : QColor = QColor(0, 0, 0)) -> None:
        """Draws disk at given coordinates (full)"""
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        painter.setPen(color)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.drawEllipse(
            QPointF(
                point.x() * scale - (size * scale / 2) + x_offset,
                point.y() * scale - (size * scale / 2) + y_offset),
            float(size * scale),
            float(size * scale))
        painter.end()

    def draw_line(self, point1 : QVector3D, point2 : QVector3D, scale : float, color : QColor = QColor(0, 0, 0)) -> None:
        """Draws line connecting given points"""
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        painter.setPen(color)
        x_offset = self.screen_offset_x * scale
        y_offset = self.screen_offset_y * scale
        painter.drawLine(
            int((point1.x() * scale) + x_offset),
            int((point1.y() * scale) + y_offset),
            int((point2.x() * scale) + x_offset),
            int((point2.y() * scale) + y_offset))
        painter.end()

    def draw_vector(self, point1 : QVector3D, point2 : QVector3D, scale : float, color : QColor = QColor(0, 0, 0)) -> None:
        """Draws vector pointing from first to second point"""
        self.draw_line(point1, point2, scale, color)
        painter = QPainter(self)
        painter.setBrush(Qt.BrushStyle.SolidPattern)
        painter.setPen(color)
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
            float((point2.x() * scale) + x_offset),
            float((point2.y() * scale) + y_offset)
        )
        painter.rotate(-angle)
        painter.translate(
            float((- point2.x() * scale) - x_offset),
            float((- point2.y() * scale) - y_offset)
        )
        painter.drawPolygon(polygon)
        painter.end()
    
    def draw_collision_detection(self, scale : float) -> None:
        """Draws collision detection elements for the aircrafts"""
        detected_conflict : bool = False
        predicted_collision : bool = False
        time_to_closest_approach : float = 0.0
        if self.simulation_state.collision:
            self.draw_text(QVector3D(self.window_width - 70, 10, 0), 0, "COLLISION", QColor(255, 0, 0))
            return
        for aircraft in self.aircraft_vehicles:
            relative_position = aircraft.position - self.aircraft_vehicles[1 - aircraft.aircraft_id].position
            speed_difference : QVector3D = aircraft.speed - self.aircraft_vehicles[1 - aircraft.aircraft_id].speed
            time_to_closest_approach = -(QVector3D.dotProduct(relative_position, speed_difference) / QVector3D.dotProduct(speed_difference, speed_difference))
            if time_to_closest_approach > 0:
                speed_difference_unit = speed_difference.normalized()
                miss_distance_vector : QVector3D = QVector3D.crossProduct(
                    speed_difference_unit,
                    QVector3D.crossProduct(relative_position, speed_difference_unit))
                collision_distance = aircraft.size / 2 + self.aircraft_vehicles[1 - aircraft.aircraft_id].size / 2
                unresolved_region = self.simulation_state.minimum_separation - miss_distance_vector.length()
                collision_region = collision_distance - miss_distance_vector.length()
                if miss_distance_vector.length() == 0:
                    self.draw_text(QVector3D(self.window_width - 200, 10, 0), 0, "DETECTED HEAD-ON COLLISION", QColor(255, 0, 255))
                    predicted_collision = True
                    detected_conflict = True
                elif collision_region > 0:
                    self.draw_text(QVector3D(self.window_width - 140, 10, 0), 0, "DETECTED COLLISION", QColor(255, 0, 0))
                    self.draw_vector(
                        self.aircraft_vehicles[1 - aircraft.aircraft_id].position,
                        self.aircraft_vehicles[1 - aircraft.aircraft_id].position + miss_distance_vector,
                        scale,
                        QColor(0, 0, 255))
                    predicted_collision = True
                    detected_conflict = True
                elif unresolved_region > 0:
                    self.draw_text(QVector3D(self.window_width - 140, 10, 0), 0, "DETECTED CONFLICT")
                    self.draw_vector(
                        self.aircraft_vehicles[1 - aircraft.aircraft_id].position,
                        self.aircraft_vehicles[1 - aircraft.aircraft_id].position + miss_distance_vector,
                        scale,
                        QColor(0, 0, 255))
                    detected_conflict = True
                if self.aircraft_fccs[aircraft.aircraft_id].vector_sharing_resolution is not None:
                    self.draw_vector(aircraft.position, aircraft.position + aircraft.speed * time_to_closest_approach, scale)
                    self.draw_vector(aircraft.position, aircraft.position + aircraft.speed * time_to_closest_approach + self.aircraft_fccs[aircraft.aircraft_id].vector_sharing_resolution, scale, QColor(30, 255, 30))
        if predicted_collision:
            aircraft = self.aircraft_vehicles[0]
            collision_location = aircraft.position + aircraft.speed * time_to_closest_approach
            self.draw_circle(collision_location, 2.5 / scale, scale, QColor(255, 0, 0))
        relative_distance = dist(self.aircraft_vehicles[0].position.toTuple(), self.aircraft_vehicles[1].position.toTuple())
        if relative_distance < self.simulation_state.minimum_separation:
            if detected_conflict:
                self.draw_text(QVector3D(self.window_width - 260, 30, 0), 0, f"MINIMUM SEPARATION EXCEEDED BY {int(self.simulation_state.minimum_separation - relative_distance)}", QColor(255, 0, 0))
            else:
                self.draw_text(QVector3D(self.window_width - 260, 10, 0), 0, f"MINIMUM SEPARATION EXCEEDED BY {int(self.simulation_state.minimum_separation - relative_distance)}", QColor(255, 0, 0))
    
    def draw_grid(self, x_offset : float, y_offset : float, scale : float) -> None:
        """Draws grid on the screen"""
        # todo: use offsets
        for x in range(0, int(self.window_width / scale - x_offset / 100), 100): # vertical lines
            self.draw_line(
                QVector3D(x - x_offset / 100, 0 - y_offset, 0),
                QVector3D(x - x_offset / 100, self.window_height / scale - y_offset, 0),
                scale,
                QColor(40, 40, 40))
        for y in range(0, int(self.window_height / scale), 100): # horizontal lines
            self.draw_line(
                QVector3D(- x_offset, y - y_offset / 100, 0),
                QVector3D(self.window_width / scale - x_offset, y - y_offset / 100, 0),
                scale,
                QColor(40, 40, 40))

    def update_moving_offsets(self) -> None:
        """Updates screen offsets based on current input"""
        scale : float = self.simulation_state.gui_scale
        if self.__moving_view_up:
            self.screen_offset_y += 10.0 / scale
        if self.__moving_view_down:
            self.screen_offset_y -= 10.0 / scale
        if self.__moving_view_left:
            self.screen_offset_x += 10.0 / scale
        if self.__moving_view_right:
            self.screen_offset_x -= 10.0 / scale

    def update_steering(self) -> None:
        """Updates aircraft steering based on current input"""
        if self.aircrafts[0] and (self.__steering_up or self.__steering_down or self.__steering_left or self.__steering_right):
            if sum([self.__steering_up, self.__steering_down, self.__steering_left, self.__steering_right]) >= 3:
                return
            self.aircraft_fccs[0].ignore_destinations = True
            target_yaw_angle : float | None = None
            if self.__steering_up and self.__steering_left:
                target_yaw_angle = -45.0
            elif self.__steering_up and self.__steering_right:
                target_yaw_angle = 45.0
            elif self.__steering_down and self.__steering_left:
                target_yaw_angle = -135.0
            elif self.__steering_down and self.__steering_right:
                target_yaw_angle = 135.0
            elif self.__steering_up:
                target_yaw_angle = 0.0
            elif self.__steering_down:
                target_yaw_angle = 180.0
            elif self.__steering_left:
                target_yaw_angle = -90.0
            elif self.__steering_right:
                target_yaw_angle = 90.0
            if target_yaw_angle is not None:
                self.aircraft_fccs[0].target_yaw_angle = target_yaw_angle

    def center_offsets(self) -> None:
        """Updates screen offsets centering on selected aircraft"""
        scale : float = self.simulation_state.gui_scale
        id = self.simulation_state.focus_aircraft_id
        self.screen_offset_x = (self.window_width / 2.0) / scale - self.aircraft_vehicles[id].position.x()
        self.screen_offset_y = (self.window_height / 2.0) / scale - self.aircraft_vehicles[id].position.y()

    def update_resolutions(self) -> None:
        """Updates bounding box resolution"""
        self.window_width = self.width()
        self.window_height = self.height()

    def zoom(self, factor : float) -> None:
        """Zooms in/out the simulation render"""
        if self.simulation_state.gui_scale + factor >= 2:
            self.simulation_state.gui_scale = 2
            return
        while factor > 0 and factor > 2 * self.simulation_state.gui_scale:
            factor /= 2
        while factor < 0 and self.simulation_state.gui_scale + factor <= 0:
            factor /= 2
        old_scale : float = self.simulation_state.gui_scale
        self.simulation_state.gui_scale += factor
        scale : float = self.simulation_state.gui_scale
        self.screen_offset_x = self.screen_offset_x * (old_scale / scale)
        self.screen_offset_y = self.screen_offset_y * (old_scale / scale)

    def paintEvent(self, event : QPaintEvent) -> None:
        """Qt method painting the aircrafts"""
        self.simulation_fps.count_frame()
        scale : float = self.simulation_state.gui_scale
        self.update_steering()
        if not self.simulation_state.follow_aircraft:
            self.update_moving_offsets()
        else:
            self.center_offsets()

        if self.simulation_state.draw_fps:
            self.draw_text(QVector3D(10, 10, 0), 0, "FPS: " + "{:.2f}".format(self.simulation_state.fps))
        if self.simulation_state.draw_grid:
            self.draw_grid(self.screen_offset_x, self.screen_offset_y, scale)

        if self.simulation_state.optimize_drawing:
            anything_to_draw : bool = False
            geometric_center : QVector3D = self.aircraft_vehicles[0].position + self.aircraft_vehicles[1].position / 2
            if (geometric_center.x() * scale + 300) + self.screen_offset_x * scale >= 0 and \
                (geometric_center.y() * scale + 200) + self.screen_offset_y * scale >= 0 and \
                (geometric_center.x() * scale - 300) + self.screen_offset_x * scale <= self.window_width and \
                (geometric_center.y() * scale - 200) + self.screen_offset_y * scale <= self.window_height:
                anything_to_draw = True
            if not anything_to_draw:
                for aircraft in self.aircraft_vehicles:
                    if (aircraft.position.x() * scale) + self.screen_offset_x * scale >= 0 and \
                        (aircraft.position.y() * scale) + self.screen_offset_y * scale >= 0 and \
                        (aircraft.position.x() * scale) + self.screen_offset_x * scale <= self.window_width and \
                        (aircraft.position.y() * scale) + self.screen_offset_y * scale <= self.window_height:
                        anything_to_draw = True
                        break
            if not anything_to_draw:
                return super().paintEvent(event)

        if self.simulation_state.draw_collision_detection:
            self.draw_collision_detection(scale)
        for aircraft in self.aircraft_vehicles:
            if self.simulation_state.draw_aircraft:
                self.draw_aircraft(aircraft, scale)
                self.draw_destinations(aircraft, scale)
            if self.simulation_state.draw_speed_vectors:
                self.draw_vector(aircraft.position, aircraft.position + aircraft.speed, scale)
        return super().paintEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling single click mouse input"""
        scale : float = self.simulation_state.gui_scale
        click_x : int = event.pos().x()
        click_y : int = event.pos().y()
        real_x : float = click_x / scale - self.screen_offset_x
        real_y : float = click_y / scale - self.screen_offset_y
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
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling mouse release input"""
        return super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        """Qt method controlling double click mouse input"""
        QApplication.beep()
        return super().mouseDoubleClickEvent(event)
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        """Qt method controlling mouse wheel input"""
        if event.angleDelta().y() > 0:
            self.zoom(0.03125)
        else:
            self.zoom(-0.03125)
        return super().wheelEvent(event)

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
            self.center_offsets()
        elif event.key() == Qt.Key.Key_Plus:
            self.zoom(0.0625)
        elif event.key() == Qt.Key.Key_Minus:
            self.zoom(-0.0625)
        elif event.key() == Qt.Key.Key_F1:
            self.simulation_state.toggle_adsb_report()
        elif event.key() == Qt.Key.Key_F2:
            self.aircraft_fccs[0].target_speed -= 10.0
        elif event.key() == Qt.Key.Key_F3:
            self.aircraft_fccs[0].target_speed += 10.0
        elif event.key() == Qt.Key.Key_O:
            self.simulation_state.toggle_first_causing_collision()
        elif event.key() == Qt.Key.Key_P:
            self.simulation_state.toggle_second_causing_collision()
        elif event.key() == Qt.Key.Key_T:
            self.simulation_state.avoid_collisions = not self.simulation_state.avoid_collisions
        elif event.key() == Qt.Key.Key_N:
            self.simulation_state.follow_aircraft = not self.simulation_state.follow_aircraft
        elif event.key() == Qt.Key.Key_M:
            self.simulation_state.focus_aircraft_id = int(not self.simulation_state.focus_aircraft_id)
        elif event.key() == Qt.Key.Key_Left:
            self.__moving_view_left = True
        elif event.key() == Qt.Key.Key_Right:
            self.__moving_view_right = True
        elif event.key() == Qt.Key.Key_Up:
            self.__moving_view_up = True
        elif event.key() == Qt.Key.Key_Down:
            self.__moving_view_down = True
        if self.aircrafts[0]:
            if event.key() == Qt.Key.Key_A:
                self.__steering_left = True
            elif event.key() == Qt.Key.Key_D:
                self.__steering_right = True
            elif event.key() == Qt.Key.Key_W:
                self.__steering_up = True
            elif event.key() == Qt.Key.Key_S:
                self.__steering_down = True
        return super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        """Qt method controlling keyboard input"""
        if event.key() == Qt.Key.Key_Slash and event.isAutoRepeat() and self.simulation_state.is_paused:
            self.simulation_state.toggle_pause()
        elif event.key() == Qt.Key.Key_Left:
            self.__moving_view_left = False
        elif event.key() == Qt.Key.Key_Right:
            self.__moving_view_right = False
        elif event.key() == Qt.Key.Key_Up:
            self.__moving_view_up = False
        elif event.key() == Qt.Key.Key_Down:
            self.__moving_view_down = False
        if self.aircrafts[0]:
            self.aircraft_fccs[0].ignore_destinations = False
            if event.key() == Qt.Key.Key_A:
                self.__steering_left = False
            elif event.key() == Qt.Key.Key_D:
                self.__steering_right = False
            elif event.key() == Qt.Key.Key_W:
                self.__steering_up = False
            elif event.key() == Qt.Key.Key_S:
                self.__steering_down = False
        return super().keyReleaseEvent(event)
    
    def resizeEvent(self, event: QPaintEvent) -> None:
        """Qt method controlling window resize event"""
        self.update_resolutions()
        return super().resizeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        self.stop_signal.emit("stop")
        event.accept()
        return super().closeEvent(event)
