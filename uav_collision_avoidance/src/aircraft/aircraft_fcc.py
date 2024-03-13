# aircraft_fcc.py

from copy import copy
from typing import List
from math import dist, atan2, degrees

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""

    def __init__(self, aircraft : AircraftVehicle) -> None:
        super().__init__()
        
        self.aircraft = aircraft

        self.__safezone_occupied : bool = False
        self.__safezone_size : float = 200.0

        self.target_yaw_angle : float = 0.0
        self.target_roll_angle : float = 0.0
        self.target_pitch_angle : float = 0.0
        # self.target_speed : float = 100.0

        self.destinations : List[QVector3D] = [
            QVector3D(1000, 1000, 1000),
            QVector3D(-100000, -100000, 1000),
        ]
        return

    def safezone_size(self) -> float:
        """"""
        return self.__safezone_size
    
    def safezone_occupied(self, occupied=None) -> bool:
        """"""
        if occupied is not None:
            self.__safezone_occupied = occupied
        return self.__safezone_occupied

    def update(self) -> None:
        """Updates current targetted movement angles"""
        destination = self.destinations[0]
        distance = dist(self.aircraft.position().toTuple(), destination.toTuple())
        if distance < self.aircraft.size():
            self.destinations.pop(0)
            destination = self.destinations[0]

        direction : QVector3D = destination - self.aircraft.position()
        angle = degrees(atan2(direction.x(), direction.y()))
        if angle < 0:
            angle += 360
        angle = 90 + angle
        angle %= 360
        self.target_yaw_angle = angle
        return
