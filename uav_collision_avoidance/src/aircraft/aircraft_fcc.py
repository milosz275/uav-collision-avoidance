# aircraft_fcc.py

import logging
from copy import copy
from typing import List
from math import dist, atan2, degrees

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
            QVector3D(600, 900, 1000),
            QVector3D(-10, -10, 1000),
        ]
        self.destinations_history : List[QVector3D] = []

        self.visited : List[QVector3D] = []
        return

    def safezone_size(self) -> float:
        """"""
        return self.__safezone_size
    
    def safezone_occupied(self, occupied=None) -> bool:
        """"""
        if occupied is not None:
            self.__safezone_occupied = occupied
        return self.__safezone_occupied
    
    def append_visited(self) -> None:
        """"""
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
            else:
                logging.info(f"Aircraft {self.aircraft.aircraft_id()} visited destination and is free now")
                return
        new_yaw_angle = degrees(atan2(
            destination.y() - self.aircraft.position().y(),
            destination.x() - self.aircraft.position().x()))
        new_yaw_angle += 90
        if new_yaw_angle > 180:
            new_yaw_angle = new_yaw_angle - 180
            new_yaw_angle *= -1
        self.target_yaw_angle = new_yaw_angle

        current_yaw_angle = self.aircraft.yaw_angle()
        if abs(current_yaw_angle - new_yaw_angle) < 0.5:
            self.target_roll_angle = 0.0
        else:
            current_yaw_angle = (current_yaw_angle + 180) % 360 - 180
            target_yaw_angle = (self.target_yaw_angle + 180) % 360 - 180
            yaw_difference = target_yaw_angle - current_yaw_angle
            if yaw_difference > 0:
                self.target_roll_angle = 30.0
            else:
                self.target_roll_angle = -30.0

        return
