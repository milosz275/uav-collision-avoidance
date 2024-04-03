"""Aircraft Flight Control Computer"""

import logging
from copy import copy
from typing import List
from collections import deque
from math import dist, atan2, degrees

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from .aircraft_vehicle import AircraftVehicle

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""

    def __init__(self, aircraft_id : int, initial_target : QVector3D | None, aircraft : AircraftVehicle) -> None:
        super().__init__()
        self.aircraft_id = aircraft_id
        self.aircraft = aircraft

        self.destinations : deque[QVector3D] = deque()

        if initial_target is None:
            self.target_yaw_angle : float = aircraft.yaw_angle
        else:
            self.target_yaw_angle : float = self.find_best_yaw_angle(aircraft.position, initial_target)
            self.add_first_destination(initial_target)

        self.initial_course : float = copy(self.target_yaw_angle)
        self.target_roll_angle : float = 0.0
        self.target_pitch_angle : float = 0.0
        self.__target_speed : float = self.aircraft.absolute_speed

        self.__evade_maneuver : bool = False
        self.vector_sharing_resolution : QVector3D | None = None

        self.destinations_history : List[QVector3D] = []
        self.visited : List[QVector3D] = []
    
    @property
    def target_speed(self) -> float:
        """Returns target speed"""
        return self.__target_speed
    
    @target_speed.setter
    def target_speed(self, speed : float) -> None:
        """Sets target speed"""
        if speed > 0:
            self.__target_speed = speed

    def add_last_destination(self, destination : QVector3D) -> None:
        """Appends given location to the end of destinations list"""
        self.destinations.append(destination)

    def add_first_destination(self, destination : QVector3D) -> None:
        """Pushes given location to the top of destinations list"""
        if len(self.destinations) > 0 and dist(destination.toTuple(), self.destinations[0].toTuple()) < 1:
            print("Attempted to stack same destination")
            logging.warning("Attempted to stack same destination")
            return

        self.destinations.appendleft(destination)
        logging.info("Aircraft %s added new first destination: %s", self.aircraft.aircraft_id, destination.toTuple())

    def append_visited(self) -> None:
        """Appends current location to visited list"""
        self.visited.append(copy(self.aircraft.position))

    def normalize_angle(self, angle : float) -> float:
        """Normalizes -180-180 angle into 360 domain"""
        angle = angle % 360
        return angle if angle >= 0 else angle + 360

    def format_angle(self, angle : float) -> float:
        """Formats angle into -180-180 domain"""
        angle = self.normalize_angle(angle)
        return angle if angle <= 180 else -180 + (angle - 180)
    
    @property
    def evade_maneuver(self) -> bool:
        """Returns evade maneuver state"""
        return self.__evade_maneuver

    def apply_evade_maneuver(self, opponent_speed : QVector3D, miss_distance_vector : QVector3D, unresolved_region : float, time_to_closest_approach : float) -> None:
        """Applies evade maneuver"""
        if self.__evade_maneuver:
            logging.warning("Another evade maneuver in progress")
        else:
            logging.info("Aircraft %s applying evade maneuver", self.aircraft.aircraft_id)
            self.__evade_maneuver = True
            self.vector_sharing_resolution : QVector3D | None = None
            if self.aircraft_id == 0:
                self.vector_sharing_resolution = (opponent_speed.length() * unresolved_region * -(miss_distance_vector)) / ((self.aircraft.speed.length() + opponent_speed.length()) * miss_distance_vector.length())
            else:
                self.vector_sharing_resolution = (opponent_speed.length() * unresolved_region * miss_distance_vector) / ((opponent_speed.length() + self.aircraft.speed.length()) * miss_distance_vector.length())
            print("Vector sharing resolution: ", self.vector_sharing_resolution)
            # unit_vector : QVector3D = self.aircraft.speed * time_to_closest_approach
            # unit_vector += self.vector_sharing_resolution
            # unit_vector.normalize()
                
            self.vector_sharing_resolution *= self.aircraft.size # default not working

            target_avoiding : QVector3D = self.aircraft.position + (self.aircraft.speed * time_to_closest_approach + self.vector_sharing_resolution)
            #self.add_first_destination(target_avoiding)

    def reset_evade_maneuver(self) -> None:
        """Resets evade maneuver"""
        if self.__evade_maneuver:
            logging.info("Aircraft %s reset evade maneuver", self.aircraft.aircraft_id)
            self.__evade_maneuver = False
            #self.vector_sharing_resolution = None

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

    def update_target_yaw_angle(self) -> None:
        """Updates current yaw angle"""
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
            
    def update_target_roll_angle(self) -> None:
        """Updates target roll angle"""
        current_yaw_angle = self.normalize_angle(self.aircraft.yaw_angle)
        target_yaw_angle = self.normalize_angle(self.target_yaw_angle)
        self.target_roll_angle = self.find_best_roll_angle(current_yaw_angle, target_yaw_angle)

        if len(self.destinations) > 1 and dist(self.aircraft.position.toTuple(), self.destinations[0].toTuple()) < self.aircraft.speed.length():
            difference = (target_yaw_angle - current_yaw_angle + 180) % 360 - 180
            if abs(difference) < 0.01:
                next_position = self.destinations[0]
                next_destination = self.destinations[1]
                next_target_yaw_angle : float = self.find_best_yaw_angle(next_position, next_destination)
                self.target_roll_angle = self.find_best_roll_angle(current_yaw_angle, next_target_yaw_angle)

    def update(self) -> None:
        """Updates current targeted movement angles"""
        self.update_target_yaw_angle()
        self.update_target_roll_angle()

    def update_target(self, target : QVector3D) -> None:
        """Updates target position"""
        self.target_yaw_angle = self.find_best_yaw_angle(self.aircraft.position, target)
        self.update_target_roll_angle()    

    def reset(self) -> None:
        """Resets aircraft flight control computer"""
        self.destinations.clear()
        self.destinations_history.clear()
        self.visited.clear()
        self.target_yaw_angle = self.initial_course
        self.target_roll_angle = 0.0
        self.target_pitch_angle = 0.0
        self.__evade_maneuver = False
