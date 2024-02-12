# simulator.py
from PySide6.QtCore import Qt, QPointF, QElapsedTimer
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PySide6.QtGui import QPen, QKeySequence, QPixmap, QTransform, QVector2D, QPolygonF, QIcon
from src.aircraft import Aircraft
from src.settings import Settings
from src.fps_counter import FPSCounter
from src.threads.flight_controller import FlightController
from src.threads.gui_render import GuiRenderer
from src.threads.physics_simulator import PhysicsSimulator
from math import radians, sin, cos, atan2, degrees, dist, sqrt
from copy import copy

class Simulator(QMainWindow):
    """Main simulation App"""

    def __init__(self) -> None:
        super().__init__()
        Settings().__init__()

        self.resolution = Settings.resolution
        self.bounding_box_resolution = [Settings.resolution[0], Settings.resolution[1]]
        self.refresh_rate = Settings.refresh_rate

        self.setWindowTitle("UAV Collision Avoidance")
        self.setGeometry(0, 0, self.resolution[0] + 10, self.resolution[1] + 10)

        self.aircraft_image = QPixmap()
        self.aircraft_image.load("src/assets/aircraft.png")

        self.icon = QIcon()
        self.icon.addPixmap(self.aircraft_image, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.aircrafts : list(Aircraft) = []
        self.reset_simulation()

        self.debug : bool = True
        self.display_aircraft_info : int = 1 # 0 - not displayed; 1 - displayed top left; 2 - displayed below aircraft
        self.display_program_info : bool = True
        self.display_course_trajectory : bool = False
        self.display_yaw_trajectory : bool = False
        self.display_safezone : bool = True
        self.display_paths : bool = True
        self.cause_crash_second : bool = False
        self.display_hitboxes : bool = True
        self.display_speed_vectors : bool = True

        self.simulation_paused = False

        self.gui_scale : float = 5.0 # divides real coordinates by this factor for gui representation
        self.frame_time : float = 1000 // self.refresh_rate # in miliseconds
        self.simulation_threshold : float = 10 # in miliseconds, 100x a second

        self.gui_fps_counter = FPSCounter()
        self.simulation_fps_counter = FPSCounter()

        self.current_simulation_fps : float = 0.0
    
        self.aircraft_size : float = self.resolution[1] * 0.04
        self.graphical_spacing : float = self.resolution[1] * 0.01

        self.is_stopped : bool = False
        self.is_finished : bool = False

        self.flight_controller = FlightController(self)
        self.gui_renderer = GuiRenderer(self)
        self.physics_simulator = PhysicsSimulator(self)

        self.flight_controller.start()
        self.gui_renderer.start()
        self.physics_simulator.start()
        
        self.show()
        return
    
    def update_simulation(self) -> None:
        """Updates simulation looping through aircrafts, checks collisions with another objects and with simulation boundaries"""
        self.current_simulation_fps = self.simulation_fps_counter.count_frame()
        for aircraft in self.aircrafts:
            aircraft.update_position()

        self.check_safezones()

        self.is_stopped = self.check_collision()
        if self.is_stopped:
            return
        
        self.is_stopped = self.check_offscreen()
        if self.is_stopped:
            return
        
        if self.cause_crash_second:
            self.cause_collision()
        return

    def avoid_aircraft_collision(self, aircraft_id : int) -> None:
        """Detects and schedules avoid maneuver for given aircraft. Assumes two aircrafts"""
        if not len(self.aircrafts) >= 1:
            print("Collision avoidance method called but there are no possible collisions.")
            return
        elif not len(self.aircrafts) <= 2:
            print("Collision avoidance method called but there are three or more aircrafts with possible collisions.")
            return
        aircraft = self.aircrafts[aircraft_id]
        if not aircraft.aircraft_id == aircraft_id:
            raise Exception("Aircraft ids are not the same. Closing...")
        
        # conflict detection
        relative_distance = dist(self.aircrafts[aircraft_id].position.toTuple(), self.aircrafts[1 - aircraft_id].position.toTuple())
        relative_distance_vector = QVector2D(
            self.aircrafts[aircraft_id].position.x() - self.aircrafts[1 - aircraft_id].position.x(),
            self.aircrafts[aircraft_id].position.y() - self.aircrafts[1 - aircraft_id].position.y())
        print(f"Relative distance: {relative_distance:.2f}")
        print(f"Relative distance vector: {relative_distance_vector.toPoint().x():.2f}, {relative_distance_vector.toPoint().y():.2f}")

        # conflict resolution
        
        return

    def reset_simulation(self) -> None:
        """Resets drawn paths and resets aircrafts"""
        for aircraft in self.aircrafts:
            aircraft.path.clear()
        self.aircrafts.clear() 
        self.aircrafts = [
            Aircraft(0, position=QPointF(500, 3500), yaw_angle=315, speed=2.5),
            Aircraft(1, position=QPointF(3500, 4000), yaw_angle=270, speed=2.0)
        ]
        self.is_finished = False
        return

    def start_simulation(self) -> None:
        """Set on the flag used in physics simulation thread"""
        if not self.simulation_paused:
            print("Physics simulator already running!")
        else:
            self.simulation_paused = False
        return
    
    def stop_simulation(self) -> None:
        """Set off the flag used in physics simulation thread"""
        if self.simulation_paused:
            print("Physics simulator already stopped!")
        else:
            self.simulation_paused = True
        self.current_simulation_fps = 0.0
        return

    def check_safezones(self) -> None:
        """Checks if safezones are entered by another aircrafts"""
        for i in range(len(self.aircrafts) - 1):
            for j in range(i + 1, len(self.aircrafts)):
                distance = dist(self.aircrafts[i].position.toTuple(), self.aircrafts[j].position.toTuple())
                if distance <= self.aircrafts[i].safezone_size / 2:
                    if not self.aircrafts[i].safezone_occupied:
                        self.aircrafts[i].safezone_occupied = True
                        self.avoid_aircraft_collision(self.aircrafts[i].aircraft_id)
                        print("Some object entered safezone of Aircraft ", self.aircrafts[i].aircraft_id)
                else:
                    if self.aircrafts[i].safezone_occupied:
                        self.aircrafts[i].safezone_occupied = False
                        print("Some object left safezone of Aircraft ", self.aircrafts[i].aircraft_id)
                if distance <= self.aircrafts[j].safezone_size / 2:
                    if not self.aircrafts[j].safezone_occupied:
                        self.aircrafts[j].safezone_occupied = True
                        self.avoid_aircraft_collision(self.aircrafts[j].aircraft_id)
                        print("Some object entered safezone of Aircraft ", self.aircrafts[j].aircraft_id)
                else:
                    if self.aircrafts[j].safezone_occupied:
                        self.aircrafts[j].safezone_occupied = False
                        print("Some object left safezone of Aircraft ", self.aircrafts[j].aircraft_id)
        return

    def check_collision(self) -> bool:
        """Checks and returns if any of the aircrafts collided with each other"""
        for i in range(len(self.aircrafts) - 1):
            for j in range(i + 1, len(self.aircrafts)):
                distance = dist(self.aircrafts[i].position.toTuple(), self.aircrafts[j].position.toTuple())
                if distance <= ((self.aircrafts[i].size + self.aircrafts[j].size) / 2):
                    self.stop_simulation()
                    self.is_finished = True
                    print("Aircrafts collided. Simulation stopped")
                    return True
        return False

    def check_offscreen(self) -> bool:
        """Checks and returns if any of the aircrafts collided with simulation boundaries"""
        for aircraft in self.aircrafts:
            x_within_bounds = 0 + aircraft.size / (2 * self.gui_scale) <= aircraft.position.x() / self.gui_scale <= self.resolution[0] - aircraft.size / (2 * self.gui_scale)
            y_within_bounds = 0 + aircraft.size / (2 * self.gui_scale) <= aircraft.position.y() / self.gui_scale <= self.resolution[1] - aircraft.size / (2 * self.gui_scale)
            if not (x_within_bounds and y_within_bounds):
                self.stop_simulation()
                self.is_finished = True
                print("Aircraft left simulation boundaries. Simulation stopped")
                return True
        return False
    
    def cause_collision(self) -> None:
        """Test method allowing to crash second aircraft into the first"""
        if len(self.aircrafts) >= 2:
            aircraft = self.aircrafts[1]
            target_aircraft = self.aircrafts[0]
            delta_x = target_aircraft.position.x() + target_aircraft.get_speed_vector().x() * target_aircraft.size - aircraft.position.x()
            delta_y = target_aircraft.position.y() + target_aircraft.get_speed_vector().y() * target_aircraft.size - aircraft.position.y()
            angle_rad = atan2(delta_y, delta_x)
            angle_deg = degrees(angle_rad)
            angle_deg %= 360
            aircraft.course = angle_deg
            return

    def render_scene(self) -> None:
        """Render the scene with aircrafts as circles, bounding box and ruler marks"""
        fps : float = self.gui_fps_counter.count_frame()
        self.scene.clear()

        bounding_box = QGraphicsRectItem(0, 0, self.bounding_box_resolution[0], self.bounding_box_resolution[1])
        self.scene.addItem(bounding_box)

        for x in range(100, self.resolution[0], 100):
            ruler_mark = QGraphicsLineItem(x, 0, x, self.graphical_spacing)
            self.scene.addItem(ruler_mark)
            text_item = QGraphicsSimpleTextItem(str(x * 10) + str(" m"))
            text_item.setPos(x - self.graphical_spacing, -2.5 * self.graphical_spacing)
            self.scene.addItem(text_item)

        for y in range(100, self.resolution[1], 100):
            ruler_mark = QGraphicsLineItem(0, y, self.graphical_spacing, y)
            self.scene.addItem(ruler_mark)
            text_item = QGraphicsSimpleTextItem(str(y * 10) + str(" m"))
            text_item.setPos(-5 * self.graphical_spacing, y - self.graphical_spacing)
            self.scene.addItem(text_item)

        # draw green light between aircrafts when their safezones are occupied
        if len(self.aircrafts) == 2 and self.aircrafts[0].safezone_occupied or self.aircrafts[1].safezone_occupied:
            relative_line = QGraphicsLineItem(
                self.aircrafts[0].position.x() / self.gui_scale,
                self.aircrafts[0].position.y() / self.gui_scale,
                self.aircrafts[1].position.x() / self.gui_scale,
                self.aircrafts[1].position.y() / self.gui_scale)
            relative_line.setPen(QPen(Qt.GlobalColor.green))
            self.scene.addItem(relative_line)

        for aircraft in self.aircrafts:
            # aircraft representation
            aircraft_pixmap = QGraphicsPixmapItem(self.aircraft_image.scaled(aircraft.size / self.gui_scale, aircraft.size / self.gui_scale))
            aircraft_pixmap.setPos(
                aircraft.position.x() / self.gui_scale,
                aircraft.position.y() / self.gui_scale)
            aircraft_pixmap.setScale(1)

            transform = QTransform()
            transform.rotate(aircraft.yaw_angle + 90)
            transform.translate(-1/2 * (aircraft.size / self.gui_scale), -1/2 * (aircraft.size / self.gui_scale))
            aircraft_pixmap.setTransform(transform)

            if aircraft.safezone_occupied:
                aircraft_pixmap.setOpacity(0.6)
            self.scene.addItem(aircraft_pixmap)

            if self.debug:
                # version label
                version_item = QGraphicsSimpleTextItem("DEBUG")
                version_item.setPos(30, 30)
                self.scene.addItem(version_item)

                # gui fps
                gui_fps_text = "Gui FPS: {:.2f}".format(fps)
                gui_fps_item = QGraphicsSimpleTextItem(gui_fps_text)
                gui_fps_item.setPos(self.bounding_box_resolution[0] - 80, self.bounding_box_resolution[1] - 40)
                self.scene.addItem(gui_fps_item)

                # simulation fps
                simulation_fps_text = "Sim FPS: {:.2f}".format(self.current_simulation_fps)
                simulation_fps_item = QGraphicsSimpleTextItem(simulation_fps_text)
                simulation_fps_item.setPos(self.bounding_box_resolution[0] - 80, self.bounding_box_resolution[1] - 20)
                self.scene.addItem(simulation_fps_item)

                # toggled values labels
                text_label = "Cause collision: {}".format("Yes" if self.cause_crash_second else "No")
                collision_text_item = QGraphicsSimpleTextItem(text_label)
                collision_text_item.setPos(self.bounding_box_resolution[0] - 110, 30)
                self.scene.addItem(collision_text_item)
                if self.is_stopped:
                    text_label = "Simulation stopped"
                    simulation_label = QGraphicsSimpleTextItem(text_label)
                    simulation_label.setPos(self.bounding_box_resolution[0] - 110, 50)
                    self.scene.addItem(simulation_label)

                # hitbox representation
                if self.display_hitboxes:
                    aircraft_circle = QGraphicsEllipseItem(
                        aircraft.position.x() / self.gui_scale - aircraft.size / (2 * self.gui_scale),
                        aircraft.position.y() / self.gui_scale - aircraft.size / (2 * self.gui_scale),
                        aircraft.size / self.gui_scale,
                        aircraft.size / self.gui_scale)
                    self.scene.addItem(aircraft_circle)

                # info label
                if self.display_aircraft_info:
                    turn_direction = ""
                    if aircraft.is_turning:
                        turn_direction = "\nturning: right" if aircraft.is_turning_right else "\nturning: left"
                    info_text = f"id: {aircraft.aircraft_id}\nx: {aircraft.position.x():.2f}\ny: {aircraft.position.y():.2f} \
                        \nspeed: {aircraft.speed:.2f}\ndistance: {aircraft.distance_covered:.1f} \
                        \ncourse: {aircraft.course:.1f}\nyaw: {aircraft.yaw_angle:.1f}\nis turning: {aircraft.is_turning}{turn_direction}"
                    text_item = QGraphicsSimpleTextItem(info_text)
                    if self.display_aircraft_info == 1:
                        text_item.setPos(-80 + 110 * (aircraft.aircraft_id + 1), 60)
                    elif self.display_aircraft_info == 2:
                        text_item.setPos(aircraft.position.x() / self.gui_scale - 100, aircraft.position.y() / self.gui_scale - 100)
                    self.scene.addItem(text_item)

                # travelled path
                if self.display_paths:
                    length = len(aircraft.path)
                    if length > 1:
                        for i in range(length - 1)[::-1]: # loop backwards
                            # prevent lag
                            if length - i > 100:
                                break
                            point1 = aircraft.path[i]
                            point2 = aircraft.path[i + 1]
                            path_line = QGraphicsLineItem(point1.x(), point1.y(), point2.x(), point2.y())
                            pen : QPen
                            if aircraft.aircraft_id == 0:
                                pen = QPen(Qt.GlobalColor.magenta)
                            elif aircraft.aircraft_id == 1:
                                pen = QPen(Qt.GlobalColor.blue)
                            else:
                                pen = QPen(Qt.GlobalColor.cyan)
                            pen.setWidth(1)
                            path_line.setPen(pen)
                            self.scene.addItem(path_line)

                # safezone around the aircraft
                if self.display_safezone:
                    aircraft_safezone_circle = QGraphicsEllipseItem(
                        aircraft.position.x() / self.gui_scale - aircraft.safezone_size / (2 * self.gui_scale),
                        aircraft.position.y() / self.gui_scale - aircraft.safezone_size / (2 * self.gui_scale),
                        aircraft.safezone_size / self.gui_scale,
                        aircraft.safezone_size / self.gui_scale)
                    self.scene.addItem(aircraft_safezone_circle)

                # speed vector
                if self.display_speed_vectors:
                    speed_vector = aircraft.get_speed_vector()
                    speed_vector_end = QPointF(
                        aircraft.position.x() / self.gui_scale + speed_vector.x() * aircraft.size / 2,
                        aircraft.position.y() / self.gui_scale + speed_vector.y() * aircraft.size / 2)
                    speed_vector_line = QGraphicsLineItem(
                        aircraft.position.x() / self.gui_scale,
                        aircraft.position.y() / self.gui_scale,
                        speed_vector_end.x(),
                        speed_vector_end.y()
                    )
                    speed_vector_line.setPen(QPen(Qt.GlobalColor.blue))
                    self.scene.addItem(speed_vector_line)

                    # arrowhead
                    arrowhead_size = aircraft.size / (3 * self.gui_scale)
                    arrowhead_height = arrowhead_size * sqrt(3) / 2
                    polygon = QPolygonF()
                    polygon.append(
                        QPointF(
                            speed_vector_end.x() -arrowhead_size / 2,
                            speed_vector_end.y() + arrowhead_height / 3
                            )
                    )
                    polygon.append(
                        QPointF(
                            speed_vector_end.x() + arrowhead_size / 2,
                            speed_vector_end.y() + arrowhead_height / 3
                        )
                    )
                    polygon.append(
                        QPointF(
                            speed_vector_end.x(),
                            speed_vector_end.y() - 2 * arrowhead_height / 3
                        )
                    )
                    arrowhead = QGraphicsPolygonItem(polygon)
                    transform = QTransform()
                    transform.translate(
                        speed_vector_end.x(),
                        speed_vector_end.y()
                    )
                    transform.rotate(aircraft.yaw_angle + 90)
                    transform.translate(
                        -speed_vector_end.x(),
                        -speed_vector_end.y()
                    )
                    arrowhead.setTransform(transform)
                    self.scene.addItem(arrowhead)

                    # negative opponent's speed vector
                    if len(self.aircrafts) == 2:
                        opponent_speed_vector : QVector2D = self.aircrafts[1 - aircraft.aircraft_id].get_speed_vector()
                        opponent_speed_vector_negative = QVector2D(-opponent_speed_vector.x(), -opponent_speed_vector.y())
                        opponent_speed_vector_negative_end = QPointF(
                            speed_vector_end.x() + opponent_speed_vector_negative.x() * aircraft.size / 2,
                            speed_vector_end.y() + opponent_speed_vector_negative.y() * aircraft.size / 2 
                        )
                        opponent_speed_vector_negative_line = QGraphicsLineItem(
                            speed_vector_end.x(),
                            speed_vector_end.y(),
                            opponent_speed_vector_negative_end.x(),
                            opponent_speed_vector_negative_end.y()
                        )
                        opponent_speed_vector_negative_line.setPen(QPen(Qt.GlobalColor.red))
                        self.scene.addItem(opponent_speed_vector_negative_line)
                
                # turn circle
                if aircraft.is_turning:
                    point1 = copy(aircraft.previous_position)
                    point2 = copy(aircraft.rendered_position)
                    length = dist(point1.toTuple(), point2.toTuple())
                    
                    center_x = 1
                    center_y = 2
                    radius = 3

                # angles of movement
                if self.display_yaw_trajectory:
                    yaw_angle_line = QGraphicsLineItem(
                        aircraft.position.x() / self.gui_scale,
                        aircraft.position.y() / self.gui_scale,
                        aircraft.position.x() / self.gui_scale + 1000 * cos(radians(aircraft.yaw_angle)),
                        aircraft.position.y() / self.gui_scale + 1000 * sin(radians(aircraft.yaw_angle)))
                    yaw_angle_line.setPen(QPen(Qt.GlobalColor.red))
                    self.scene.addItem(yaw_angle_line)
                if self.display_course_trajectory:
                    course_line = QGraphicsLineItem(
                        aircraft.position.x() / self.gui_scale,
                        aircraft.position.y() / self.gui_scale,
                        aircraft.position.x() / self.gui_scale + 1000 * cos(radians(aircraft.course)),
                        aircraft.position.y() / self.gui_scale + 1000 * sin(radians(aircraft.course)))
                    if aircraft.course % 45 == 0 and not aircraft.course % 90 == 0:
                        course_line.setPen(QPen(Qt.GlobalColor.green))
                    self.scene.addItem(course_line)
            else:
                version_item = QGraphicsSimpleTextItem("RELEASE")
                version_item.setPos(30, 30)
                self.scene.addItem(version_item)

        self.view.setScene(self.scene)
        self.view.setSceneRect(0, 0, *self.resolution)
        return

    def closeEvent(self, event):
        """Qt method handling Simulator close event"""

        self.flight_controller.requestInterruption()
        self.flight_controller.quit()
        self.flight_controller.wait()

        self.gui_renderer.requestInterruption()
        self.gui_renderer.quit()
        self.gui_renderer.wait()

        self.physics_simulator.requestInterruption()
        self.physics_simulator.quit()
        self.physics_simulator.wait()

        event.accept()
    
    def keyPressEvent(self, event) -> None:
        """Qt method handling keypress events for steering the aircrafts and simulation state"""
        
        if QKeySequence(event.key()).toString() == "`":
            self.debug ^= 1
        
        # ctrl + button
        if event.modifiers() and Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_C:
                self.close()
        if event.key() == Qt.Key.Key_Escape:
            self.close()

        if not self.debug:
            return super().keyPressEvent(event)
        
        # first aircraft steering
        if len(self.aircrafts) >= 1:
            if event.key() == Qt.Key.Key_D:
                self.aircrafts[0].course = 0
            elif event.key() == Qt.Key.Key_S:
                self.aircrafts[0].course = 90
            elif event.key() == Qt.Key.Key_A:
                self.aircrafts[0].course = 180
            elif event.key() == Qt.Key.Key_W:
                self.aircrafts[0].course = 270
            elif event.key() == Qt.Key.Key_F2:
                if self.aircrafts[0].set_speed >= 2:
                    self.aircrafts[0].set_speed -= 1
            elif event.key() == Qt.Key.Key_F3:
                self.aircrafts[0].set_speed += 1
            elif event.key() == Qt.Key.Key_Y:
                course = self.aircrafts[0].course
                course -= self.aircrafts[0].max_course_change * 2
                if course < 0:
                    course += 360
                self.aircrafts[0].course = course
            elif event.key() == Qt.Key.Key_U:
                course = self.aircrafts[0].course
                course += self.aircrafts[0].max_course_change * 2
                if course >= 360:
                    course -= 360
                self.aircrafts[0].course = course
        
        # second aircraft steering
        if len(self.aircrafts) >= 2:
            if event.key() == Qt.Key.Key_L:
                self.aircrafts[1].course = 0
            elif event.key() == Qt.Key.Key_K:
                self.aircrafts[1].course = 90
            elif event.key() == Qt.Key.Key_J:
                self.aircrafts[1].course = 180
            elif event.key() == Qt.Key.Key_I:
                self.aircrafts[1].course = 270
            elif event.key() == Qt.Key.Key_F6:
                if self.aircrafts[1].set_speed >= 2:
                    self.aircrafts[1].set_speed -= 1
            elif event.key() == Qt.Key.Key_F7:
                self.aircrafts[1].set_speed += 1
            elif event.key() == Qt.Key.Key_O:
                course = self.aircrafts[1].course
                course -= self.aircrafts[1].max_course_change * 2
                if course < 0:
                    course += 360
                self.aircrafts[1].course = course
            elif event.key() == Qt.Key.Key_P:
                course = self.aircrafts[1].course
                course += self.aircrafts[1].max_course_change * 2
                if course >= 360:
                    course -= 360
                self.aircrafts[1].course = course
        
        # shortcuts for every case
        if event.key() == Qt.Key.Key_R:
            self.stop_simulation()
            self.reset_simulation()
            self.start_simulation()
        elif event.key() == Qt.Key.Key_T:
            self.reset_flags()
        elif event.key() == Qt.Key.Key_Slash:
            if not self.is_finished:
                if self.is_stopped:
                    self.start_simulation()
                else:
                    self.stop_simulation()
            else:
                self.reset_simulation()
                self.start_simulation()
        elif event.key() == Qt.Key.Key_1:
            value = self.display_aircraft_info + 1
            if value > 2:
                value = 0
            self.display_aircraft_info = value
        elif event.key() == Qt.Key.Key_2:
            self.display_program_info ^= 1
        elif event.key() == Qt.Key.Key_3:
            self.display_course_trajectory ^= 1
        elif event.key() == Qt.Key.Key_4:
            self.display_yaw_trajectory ^= 1
        elif event.key() == Qt.Key.Key_5:
            self.display_safezone ^= 1
        elif event.key() == Qt.Key.Key_6:
            self.display_paths ^= 1
        elif event.key() == Qt.Key.Key_7:
            self.cause_crash_second ^= 1
        elif event.key() == Qt.Key.Key_8:
            self.display_hitboxes ^= 1
        elif event.key() == Qt.Key.Key_9:
            self.display_speed_vectors ^= 1

        return super().keyPressEvent(event)
