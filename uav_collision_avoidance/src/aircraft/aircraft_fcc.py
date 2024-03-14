# aircraft_fcc.py

import logging
from copy import copy
from typing import List
from math import dist, atan2, degrees, radians, pi

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""

    def __init__(self, aircraft_id : int, aircraft : AircraftVehicle) -> None:
        super().__init__()
        self.aircraft_id = aircraft_id
        self.aircraft = aircraft

        self.__safezone_occupied : bool = False
        self.__safezone_size : float = 200.0

        self.target_yaw_angle : float = 0.0
        self.target_roll_angle : float = 0.0
        self.target_pitch_angle : float = 0.0
        # self.target_speed : float = 100.0

        self.destinations : List[QVector3D] = [
            QVector3D(1100, 850, 1000),
            # QVector3D(100, 100, 1000),
        ]
        self.destinations_history : List[QVector3D] = []

        self.visited : List[QVector3D] = []
        return

    def safezone_size(self) -> float:
        """Returns safezone size"""
        return self.__safezone_size
    
    def safezone_occupied(self, occupied=None) -> bool:
        """Gets and/or sets safezone state"""
        if occupied is not None:
            self.__safezone_occupied = occupied
        return self.__safezone_occupied
    
    def append_visited(self) -> None:
        """Appends current location to visited list"""
        self.visited.append(copy(self.aircraft.position()))
        return

    def update(self) -> None:
        """Updates current targetted movement angles"""
        if not self.destinations:
            return
        destination = self.destinations[0]
        distance = dist(self.aircraft.position().toTuple(), destination.toTuple())
        if distance < self.aircraft.size():
            self.destinations_history.append(self.destinations.pop(0))
            if self.destinations:
                destination = self.destinations[0]
                logging.info(f"Aircraft {self.aircraft.aircraft_id()} visited destination and took next one")
                print(f"Aircraft {self.aircraft.aircraft_id()} visited destination and took next one")
            else:
                logging.info(f"Aircraft {self.aircraft.aircraft_id()} visited destination and is free now")
                print(f"Aircraft {self.aircraft.aircraft_id()} visited destination and is free now")
                return
        new_yaw_angle = degrees(atan2(
            destination.y() - self.aircraft.position().y(),
            destination.x() - self.aircraft.position().x()))
        new_yaw_angle += 90
        if new_yaw_angle > 180:
            new_yaw_angle = new_yaw_angle - 180
            new_yaw_angle *= -1
        self.target_yaw_angle = new_yaw_angle

        target_yaw_rad : float = radians(new_yaw_angle)
        current_yaw_rad : float = radians(self.aircraft.yaw_angle())
        yaw_difference_rad = target_yaw_rad - current_yaw_rad
        yaw_difference_rad = (yaw_difference_rad + pi) % (2 * pi) - pi
        if yaw_difference_rad >= 0.0:
            self.target_roll_angle = 30.0
        elif yaw_difference_rad < 0.0:
            self.target_roll_angle = -30.0
        if abs(degrees(yaw_difference_rad)) < 5.0:
            self.target_roll_angle = 0.0
        return
