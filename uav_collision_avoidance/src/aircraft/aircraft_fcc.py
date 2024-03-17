""""""

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

        self.destinations : List[QVector3D] = []
        self.destinations_history : List[QVector3D] = []
        self.visited : List[QVector3D] = []
        return

    def safezone_size(self) -> float:
        """Returns safezone size"""
        return self.__safezone_size
    
    def safezone_occupied(self, occupied : bool = None) -> bool:
        """Gets and/or sets safezone state"""
        if occupied is not None:
            self.__safezone_occupied = occupied
        return self.__safezone_occupied
    
    def append_destination(self, destination : QVector3D) -> None:
        """Appends given location to the end of destinations list"""
        self.destinations.append(destination)
        return
    
    def push_destination_top(self, destination : QVector3D) -> None:
        """Pushes given location to the top of destinations list"""
        new_list : List[QVector3D] = [destination]
        for destination in self.destinations:
            new_list.append(destination)
        self.destinations = new_list
        return
    
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

        if distance < self.aircraft.size() / 2:
            self.destinations_history.append(self.destinations.pop(0))
            if self.destinations:
                destination = self.destinations[0]
                logging.info("Aircraft %s visited destination and took next one", self.aircraft.aircraft_id())
                print(f"Aircraft {self.aircraft.aircraft_id()} visited destination and took next one")
            else:
                logging.info("Aircraft %s visited destination and is free now", self.aircraft.aircraft_id())
                print(f"Aircraft {self.aircraft.aircraft_id()} visited destination and is free now")
                return
            
        target_yaw_angle : float  = degrees(atan2(
            destination.y() - self.aircraft.position().y(),
            destination.x() - self.aircraft.position().x()))
        target_yaw_angle += 90
        if target_yaw_angle > 180:
            target_yaw_angle = -180 + (target_yaw_angle - 180)
        self.target_yaw_angle = target_yaw_angle

        current_yaw_angle : float = self.aircraft.yaw_angle()
        if target_yaw_angle < 0:
            target_yaw_angle += 360
        if current_yaw_angle < 0:
            current_yaw_angle += 360
        
        difference = target_yaw_angle - current_yaw_angle
        if abs(difference) < 4.0:
            self.target_roll_angle = 0.0
            return
        if difference > 0 and difference <= 180:
            self.target_roll_angle = 30.0
        else:
            self.target_roll_angle = -30.0

        return
