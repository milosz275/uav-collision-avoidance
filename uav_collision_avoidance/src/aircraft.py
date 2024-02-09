# aircraft.py
from PySide6.QtCore import QPointF
from PySide6.QtGui import QVector2D
from typing import List
from math import cos, sin, radians, dist, asin, degrees, tan
from copy import copy

class Aircraft:
    """Aircraft"""
    aircraft_id: int
    yaw_angle : float
    pitch_angle : float
    roll_angle : float
    set_speed : float # speed set to be achieved
    speed : float # actual speed in m/s
    minimal_speed : float = 5.0 # minimal airspeed in m/s
    course : float # set course in degrees (0-360)
    position : QPointF # point x,y in meters
    distance_covered : float # distance in meters
    size : float # size in meters
    max_course_change : float = 1.5 # angle step
    speedstep : float = 0.05 # m/s change in simulation iteration
    safezone_size : float = 1000.0 # meters
    safezone_occupied: bool
    path: List[QPointF]
    
    def __init__(self, aircraft_id, position, yaw_angle, speed) -> None:
        """Initializes the aircraft"""
        self.aircraft_id = aircraft_id
        self.yaw_angle = yaw_angle
        self.pitch_angle = 0.0
        self.roll_angle = 45.0
        self.speed = speed
        self.vertical_speed = 0.0
        self.set_speed = speed
        self.course = self.yaw_angle
        self.position = position
        self.rendered_position = QPointF(self.position.x(), self.position.y())
        self.size = 50.0
        self.previous_position = copy(position)
        self.distance_covered = 0.0
        #self.max_course_change = 0.0
        self.safezone_occupied = False # todo: change to int
        self.is_turning = False
        self.is_turning_right = False
        self.path = []

    def update_course(self) -> None:
        """Applies gradual change to yaw angle respecting set course"""
        # todo: replace with algorithm
        abs_course = self.course
        while abs_course >= 360:
            abs_course -= 360
        while abs_course < 0:
            abs_course += 360
        abs_course %= 360
        
        if (abs_course == self.yaw_angle):
            self.is_turning = False
            return
        else:
            self.is_turning = True

        if (abs_course - self.yaw_angle) < 0:
            abs_course += 360
        new_yaw_angle = self.yaw_angle

        # self.calculate_turn_radius()
        # self.calculate_max_course_change()

        if (abs_course - self.yaw_angle) <= 180:
            self.is_turning_right = True
            if abs_course < (self.yaw_angle + self.max_course_change):
                new_yaw_angle = abs_course
            else:
                new_yaw_angle += self.max_course_change
        else:
            self.is_turning_right = False
            if abs_course < (self.yaw_angle - self.max_course_change):
                new_yaw_angle = abs_course
            else:
                new_yaw_angle -= self.max_course_change
        new_yaw_angle %= 360
        self.yaw_angle = new_yaw_angle
        return
    
    def update_speed(self) -> None:
        """Updates speed to the set one"""
        if self.set_speed < self.minimal_speed or self.speed < self.minimal_speed:
            self.set_speed = self.minimal_speed
            self.speed = self.minimal_speed
            return
        if self.set_speed == self.speed:
            return
        elif self.set_speed > self.speed:
            if self.set_speed - self.speed <= self.speedstep:
                self.speed = self.set_speed
            else:
                self.speed += self.speedstep
        else: # deceleration
            if self.speed - self.set_speed <= self.speedstep:
                self.speed = self.set_speed
            else:
                self.speed -= self.speedstep
        return

    def update_position(self) -> None:
        """Updates position of the aircraft, applies smooth course adjustment"""
        self.update_speed()
        self.update_course()

        # todo: change to matrix
        self.previous_position = copy(self.position)
        speed_vector = self.get_speed_vector()
        self.position.setX(self.position.x() + speed_vector.x())
        self.position.setY(self.position.y() + speed_vector.y())
        self.rendered_position.setX(self.position.x() / 10)
        self.rendered_position.setY(self.position.y() / 10)
        
        # distance covered
        distance = dist(self.previous_position.toTuple(), self.position.toTuple())
        self.distance_covered += distance
        
        # path
        self.path.append(copy(self.position))
        return

    def get_speed_vector(self) -> QVector2D:
        """Returns speed vector of the aircraft"""
        return QVector2D(self.speed * cos(radians(self.yaw_angle)), self.speed * sin(radians(self.yaw_angle)))
