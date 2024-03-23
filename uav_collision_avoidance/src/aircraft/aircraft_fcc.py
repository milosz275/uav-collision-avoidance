"""Aircraft Flight Control Computer"""

import logging
from copy import copy
from typing import List
from collections import deque
from math import dist, atan2, degrees

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""

    def __init__(self, aircraft_id : int, initial_target : QVector3D, aircraft : AircraftVehicle) -> None:
        super().__init__()
        self.aircraft_id = aircraft_id
        self.aircraft = aircraft

        self.__safezone_occupied : bool = False
        self.__safezone_size : float = 200.0

        self.target_yaw_angle : float = self.find_best_yaw_angle(aircraft.position, initial_target)
        self.target_roll_angle : float = 0.0
        self.target_pitch_angle : float = 0.0
        self.target_speed : float = self.aircraft.absolute_speed

        self.__evade_maneuver : bool = False

        self.destinations : deque[QVector3D] = deque()
        self.destinations_history : List[QVector3D] = []
        self.visited : List[QVector3D] = []

    @property
    def safezone_size(self) -> float:
        """Returns safezone size"""
        return self.__safezone_size

    @property
    def safezone_occupied(self) -> bool:
        """Returns safezone state"""
        return self.__safezone_occupied

    @safezone_occupied.setter
    def safezone_occupied(self, occupied : bool) -> None:
        """Sets safezone state"""
        self.__safezone_occupied = occupied

    def add_last_destination(self, destination : QVector3D) -> None:
        """Appends given location to the end of destinations list"""
        self.destinations.append(destination)

    def add_first_destination(self, destination : QVector3D) -> None:
        """Pushes given location to the top of destinations list"""
        self.destinations.appendleft(destination)

    def append_visited(self) -> None:
        """Appends current location to visited list"""
        self.visited.append(copy(self.aircraft.position))

    def apply_evade_maneuver(self) -> None:
        """Applies evade maneuver"""
        if self.__evade_maneuver:
            logging.warning("Another evade maneuver in progress")
        else:
            self.__evade_maneuver = True
            # todo: calculate turn radius, apply roll angle,
            # add corner enter position,
            # add maneuver end position, 
            # check if original destination is restored,
            # reset evade maneuver flag

    def normalize_angle(self, angle : float) -> float:
        """Normalizes -180-180 angle into 360 domain"""
        angle = angle % 360
        return angle if angle >= 0 else angle + 360

    def format_angle(self, angle : float) -> float:
        """Formats angle into -180-180 domain"""
        angle = self.normalize_angle(angle)
        return angle if angle <= 180 else -180 + (angle - 180)

    def find_best_roll_angle(self, current_yaw_angle : float, target_yaw_angle : float) -> float:
        """Finds best roll angle for the targeted yaw angle"""
        difference = (target_yaw_angle - current_yaw_angle + 180) % 360 - 180
        return 0.0 if abs(difference) < 0.01 else 30.0 if difference > 0 else -30.0

    def find_best_yaw_angle(self, position : QVector3D, destination : QVector3D) -> float:
        """Finds best yaw angle for the given destination"""
        target_yaw_angle : float  = degrees(atan2(
            destination.y() - position.y(),
            destination.x() - position.x()))
        target_yaw_angle += 90
        return self.format_angle(target_yaw_angle)

    def update(self) -> None:
        """Updates current targeted movement angles"""
        if self.destinations:
            destination = self.destinations[0]
            distance = dist(self.aircraft.position.toTuple(), destination.toTuple())
            if distance < self.aircraft.size / 2:
                self.destinations_history.append(self.destinations.popleft())
                if self.destinations:
                    destination = self.destinations[0]
                    logging.info("Aircraft %s visited destination and took next one", self.aircraft.aircraft_id)
                    print(f"Aircraft {self.aircraft.aircraft_id} visited destination and took next one")
                else:
                    logging.info("Aircraft %s visited destination and is free now", self.aircraft.aircraft_id)
                    print(f"Aircraft {self.aircraft.aircraft_id} visited destination and is free now")
                    return
            self.target_yaw_angle = self.find_best_yaw_angle(
                self.aircraft.position,
                destination)
        
        current_yaw_angle = self.normalize_angle(self.aircraft.yaw_angle)
        target_yaw_angle = self.normalize_angle(self.target_yaw_angle)
        self.target_roll_angle = self.find_best_roll_angle(current_yaw_angle, target_yaw_angle)

        if len(self.destinations) > 1:
            difference = (target_yaw_angle - current_yaw_angle + 180) % 360 - 180
            if abs(difference) < 0.01:
                next_position = destination
                next_destination = self.destinations[1]
                next_target_yaw_angle : float = self.find_best_yaw_angle(next_position, next_destination)
                self.target_roll_angle = self.find_best_roll_angle(current_yaw_angle, next_target_yaw_angle)
