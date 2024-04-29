"""Aircraft Flight Control Computer"""

import logging
from copy import copy
from typing import List
from collections import deque
from math import dist, atan2, degrees

from PySide6.QtCore import QObject, QMutex, QMutexLocker
from PySide6.QtGui import QVector3D

from .aircraft_vehicle import AircraftVehicle

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""
    
    def __init__(self, aircraft_id : int, initial_target : QVector3D | None, aircraft : AircraftVehicle) -> None:
        super().__init__()
        self.__mutex : QMutex = QMutex()
        self.__aircraft_id = aircraft_id
        self.__aircraft = aircraft
        self.__destinations : deque[QVector3D] = deque()
        self.__destinations_history : List[QVector3D] = []
        self.__visited : List[QVector3D] = []
        self.__autopilot : bool = True
        self.__ignore_destinations : bool = False
        self.__initial_target : QVector3D | None = initial_target
        self.__target_yaw_angle : float = 0.0
        if initial_target is None:
            self.__target_yaw_angle = aircraft.yaw_angle
            self.__autopilot = False
        else:
            self.__target_yaw_angle = self.find_best_yaw_angle(aircraft.position, initial_target)
            self.add_first_destination(initial_target)
        self.__target_roll_angle : float = 0.0
        self.__target_pitch_angle : float = 0.0
        self.__target_speed : float = self.aircraft.absolute_speed
        self.__is_turning_right : bool = False
        self.__is_turning_left : bool = False
        self.__safe_zone_occupied : bool = False
        self.__evade_maneuver : bool = False
        self.__vector_sharing_resolution : QVector3D | None = None

    @property
    def aircraft_id(self) -> int:
        """Returns aircraft id"""
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id
    
    @property
    def aircraft(self) -> AircraftVehicle:
        """Returns aircraft vehicle"""
        with QMutexLocker(self.__mutex):
            return self.__aircraft
    
    @property
    def destinations(self) -> deque[QVector3D]:
        """Returns destinations list"""
        with QMutexLocker(self.__mutex):
            return self.__destinations
    
    @property
    def destinations_history(self) -> List[QVector3D]:
        """Returns destinations history list"""
        with QMutexLocker(self.__mutex):
            return self.__destinations_history
    
    @property
    def visited(self) -> List[QVector3D]:
        """Returns visited list"""
        with QMutexLocker(self.__mutex):
            return self.__visited
    
    @property
    def autopilot(self) -> bool:
        """Returns autopilot state"""
        with QMutexLocker(self.__mutex):
            return self.__autopilot
    
    def toggle_autopilot(self) -> None:
        """Toggles autopilot state"""
        with QMutexLocker(self.__mutex):
            self.__autopilot = not self.__autopilot

    @property
    def ignore_destinations(self) -> bool:
        """Returns ignore destinations state"""
        with QMutexLocker(self.__mutex):
            return self.__ignore_destinations
    
    @ignore_destinations.setter
    def ignore_destinations(self, value : bool) -> None:
        """Sets ignore destinations state"""
        with QMutexLocker(self.__mutex):
            self.__ignore_destinations = value

    @property
    def initial_target(self) -> QVector3D | None:
        """Returns initial target"""
        with QMutexLocker(self.__mutex):
            return self.__initial_target

    @property
    def target_yaw_angle(self) -> float:
        """Returns target yaw angle"""
        with QMutexLocker(self.__mutex):
            return self.__target_yaw_angle
    
    @target_yaw_angle.setter
    def target_yaw_angle(self, angle : float) -> None:
        """Sets target yaw angle"""
        with QMutexLocker(self.__mutex):
            self.__target_yaw_angle = angle

    @property
    def target_roll_angle(self) -> float:
        """Returns target roll angle"""
        with QMutexLocker(self.__mutex):
            return self.__target_roll_angle
    
    @target_roll_angle.setter
    def target_roll_angle(self, angle : float) -> None:
        """Sets target roll angle"""
        with QMutexLocker(self.__mutex):
            self.__target_roll_angle = angle

    @property
    def target_pitch_angle(self) -> float:
        """Returns target pitch angle"""
        with QMutexLocker(self.__mutex):
            return self.__target_pitch_angle
    
    @target_pitch_angle.setter
    def target_pitch_angle(self, angle : float) -> None:
        """Sets target pitch angle"""
        with QMutexLocker(self.__mutex):
            self.__target_pitch_angle = angle
    
    @property
    def target_speed(self) -> float:
        """Returns target speed"""
        with QMutexLocker(self.__mutex):
            return self.__target_speed
    
    @target_speed.setter
    def target_speed(self, speed : float) -> None:
        """Sets target speed"""
        if speed > 0:
            with QMutexLocker(self.__mutex):
                self.__target_speed = speed

    def accelerate(self, acceleration : float) -> None:
        """Accelerates aircraft's targeted speed"""
        with QMutexLocker(self.__mutex):
            if self.__target_speed + acceleration <= 0:
                return
            self.__target_speed += acceleration
    
    @property
    def is_turning_right(self) -> bool:
        """Returns turning right state"""
        with QMutexLocker(self.__mutex):
            return self.__is_turning_right
    
    @is_turning_right.setter
    def is_turning_right(self, value : bool) -> None:
        """Sets turning right state"""
        with QMutexLocker(self.__mutex):
            self.__is_turning_right = value

    @property
    def is_turning_left(self) -> bool:
        """Returns turning left state"""
        with QMutexLocker(self.__mutex):
            return self.__is_turning_left
    
    @is_turning_left.setter
    def is_turning_left(self, value : bool) -> None:
        """Sets turning left state"""
        with QMutexLocker(self.__mutex):
            self.__is_turning_left = value

    def check_new_destination(self, destination : QVector3D, first : bool) -> QVector3D | None:
        """Checks if the given destination is already in the destinations list"""
        if not all(isinstance(coord, (int, float)) for coord in (destination.x(), destination.y(), destination.z())):
            raise TypeError("Destination coordinates must be int or float.")
        if len(self.destinations) > 0 and first:
            if dist(destination.toTuple(), self.destinations[0].toTuple()) < 1.0:
                print("Attempted to stack same destination")
                logging.warning(f"Attempted to stack same destination: {destination}")
                return None
        elif len(self.destinations) > 0 and not first:
            if dist(destination.toTuple(), self.destinations[len(self.destinations) - 1].toTuple()) < 1.0:
                print("Attempted to stack same destination")
                logging.warning(f"Attempted to stack same destination: {destination}")
                return None
        if destination.z() < 500:
            if destination.z() < 0:
                print("Attempted to set destination below ground")
                logging.warning(f"Attempted to set destination below ground: {destination}")
            else:
                print("Attempted to set destination too low")
                logging.warning(f"Attempted to set destination too low: {destination}")
            destination = QVector3D(destination.x(), destination.y(), 500)
        elif destination.z() > 10000:
            print("Attempted to set destination too high")
            logging.warning(f"Attempted to set destination too high: {destination}")
            destination = QVector3D(destination.x(), destination.y(), 10000)
        return destination

    def add_last_destination(self, destination : QVector3D) -> None:
        """Appends the given location (QVector3D) to the end of the destinations list."""
        destination : QVector3D = self.check_new_destination(destination, False)
        if destination is not None:
            with QMutexLocker(self.__mutex):
                self.__destinations.append(destination)
                logging.info("Aircraft %s added new last destination: %s", self.__aircraft.aircraft_id, destination.toTuple())

    def add_first_destination(self, destination : QVector3D) -> None:
        """Pushes given location to the top of destinations list"""
        destination : QVector3D = self.check_new_destination(destination, True)
        if destination is not None:
            with QMutexLocker(self.__mutex):
                self.__destinations.appendleft(destination)
                logging.info("Aircraft %s added new first destination: %s", self.__aircraft.aircraft_id, destination.toTuple())

    @property
    def destination(self) -> QVector3D | None:
        """Returns current destination"""
        with QMutexLocker(self.__mutex):
            if len(self.__destinations) > 0:
                return self.__destinations[0]
            else:
                return None

    def append_visited(self) -> None:
        """Appends current location to visited list"""
        self.visited.append(copy(self.aircraft.position))

    def normalize_angle(self, angle : float) -> float:
        """Normalizes -180-180 angle into 360 domain"""
        angle = angle % 360
        return angle if angle >= 0 else angle + 360

    def format_yaw_angle(self, angle : float) -> float:
        """Formats angle into -180-180 domain"""
        angle = self.normalize_angle(angle)
        return angle if angle <= 180 else -180 + (angle - 180)
    
    @property
    def vector_sharing_resolution(self) -> QVector3D | None:
        """Returns vector sharing resolution"""
        with QMutexLocker(self.__mutex):
            return self.__vector_sharing_resolution
    
    @vector_sharing_resolution.setter
    def vector_sharing_resolution(self, value : QVector3D | None) -> None:
        """Sets vector sharing resolution"""
        with QMutexLocker(self.__mutex):
            self.__vector_sharing_resolution = value

    @property
    def safe_zone_occupied(self) -> bool:
        """Returns safe zone occupied state"""
        with QMutexLocker(self.__mutex):
            return self.__safe_zone_occupied
    
    @safe_zone_occupied.setter
    def safe_zone_occupied(self, value : bool) -> None:
        """Sets safe zone occupied state"""
        with QMutexLocker(self.__mutex):
            if self.__safe_zone_occupied and value:
                print("Safe zone already occupied")
                logging.warning("Safe zone already occupied")
            if not self.__safe_zone_occupied and not value:
                print("Safe zone already free")
                logging.warning("Safe zone already free")
            self.__safe_zone_occupied = value
    
    @property
    def evade_maneuver(self) -> bool:
        """Returns evade maneuver state"""
        with QMutexLocker(self.__mutex):
            return self.__evade_maneuver

    def apply_evade_maneuver(self, opponent_speed : QVector3D, miss_distance_vector : QVector3D, unresolved_region : float, time_to_closest_approach : float) -> None:
        """Applies evade maneuver"""
        print(str(self.aircraft.aircraft_id) + ": opponent speed: " + "{:.2f}".format(opponent_speed.x()) + " " + "{:.2f}".format(opponent_speed.y()) + " " + "{:.2f}".format(opponent_speed.z()))
        print(str(self.aircraft.aircraft_id) + ": miss distance vector: " + "{:.2f}".format(miss_distance_vector.x()) + " " + "{:.2f}".format(miss_distance_vector.y()) + " " + "{:.2f}".format(miss_distance_vector.z()))
        print(str(self.aircraft.aircraft_id) + ": unresolved region: " + "{:.2f}".format(unresolved_region))
        print(str(self.aircraft.aircraft_id) + ": time to closest approach: " + "{:.2f}".format(time_to_closest_approach))

        if self.__evade_maneuver:
            logging.warning("Another evade maneuver in progress")
        else:
            print(f"Aircraft {self.aircraft.aircraft_id} applying evade maneuver")
            logging.info("Aircraft %s applying evade maneuver", self.aircraft.aircraft_id)
            self.__evade_maneuver = True

            # this is temporal solution of the problem below
            if miss_distance_vector.length() == 0:
                miss_distance_vector = QVector3D(0.01, 0.01, 0.0)

            target_avoiding : QVector3D = QVector3D()
            if miss_distance_vector.length() == 0:
                # todo: fix or just change height
                # modified_speed_vector : QVector3D = self.aircraft.speed + 0.01 * (self.aircraft.speed.normalized().z() * self.aircraft.speed)
                # modified_speed_vector : QVector3D = self.aircraft.speed + 0.01 * QVector3D.crossProduct(self.aircraft.speed.normalized(), self.aircraft.speed)
                # modified_speed_vector : QVector3D = self.aircraft.speed + (QVector3D.crossProduct(QVector3D(0, 0, self.aircraft.speed.normalized().z()), self.aircraft.speed))
                # print("Modified speed vector: " + "{:.2f}".format(modified_speed_vector.x()) + " " + "{:.2f}".format(modified_speed_vector.y()) + " " + "{:.2f}".format(modified_speed_vector.z()))
                # unit_vector : QVector3D = modified_speed_vector.normalized()
                # print("Unit vector: " + "{:.2f}".format(unit_vector.x()) + " " + "{:.2f}".format(unit_vector.y()) + " " + "{:.2f}".format(unit_vector.z()))
                # target_avoiding = self.aircraft.position + (unit_vector * modified_speed_vector.length())
                pass
            else:
                self.vector_sharing_resolution : QVector3D | None = None
                if self.aircraft_id == 0:
                    self.vector_sharing_resolution = (opponent_speed.length() * unresolved_region * -(miss_distance_vector)) / ((self.aircraft.speed.length() + opponent_speed.length()) * miss_distance_vector.length())
                elif self.aircraft_id == 1:
                    self.vector_sharing_resolution = (opponent_speed.length() * unresolved_region * miss_distance_vector) / ((opponent_speed.length() + self.aircraft.speed.length()) * miss_distance_vector.length())
                print("Vector sharing resolution: " + "{:.2f}".format(self.vector_sharing_resolution.x()) + " " + "{:.2f}".format(self.vector_sharing_resolution.y()) + " " + "{:.2f}".format(self.vector_sharing_resolution.z()))
                modified_speed_vector : QVector3D = (self.aircraft.speed * time_to_closest_approach + self.vector_sharing_resolution)
                unit_vector : QVector3D = modified_speed_vector.normalized()
                target_avoiding = self.aircraft.position + (unit_vector * modified_speed_vector.length())
            
            print("Set target avoiding collision: " + "{:.2f}".format(target_avoiding.x()) + " " + "{:.2f}".format(target_avoiding.y()) + " " + "{:.2f}".format(target_avoiding.z()))
            self.add_first_destination(target_avoiding)

    def reset_evade_maneuver(self) -> None:
        """Resets evade maneuver"""
        with QMutexLocker(self.__mutex):
            if self.__evade_maneuver:
                logging.info("Aircraft %s reset evade maneuver", self.__aircraft.aircraft_id)
                self.__evade_maneuver = False
                #self.vector_sharing_resolution = None

    def find_best_roll_angle(self, current_yaw_angle: float, target_yaw_angle: float) -> float:
        """Finds best roll angle for the targeted yaw angle"""
        difference = (target_yaw_angle - current_yaw_angle + 180) % 360 - 180
        if abs(difference) < 0.001:
            self.is_turning_right = False
            self.is_turning_left = False
            return 0.0
        elif difference > 0:
            self.is_turning_right = True
            self.is_turning_left = False
            if difference > 90:
                return 30.0
            elif difference > 45:
                return 20.0
            elif difference > 20:
                return 10.0
            else:
                return 5.0
        elif difference < 0:
            self.is_turning_left = True
            self.is_turning_right = False
            if difference < -90:
                return -30.0
            elif difference < -45:
                return -20.0
            elif difference < -20:
                return -10.0
            else:
                return -5.0
        else:
            return 0.0
        
    def find_best_yaw_angle(self, position : QVector3D, destination : QVector3D) -> float:
        """Finds best yaw angle for the given destination"""
        target_yaw_angle : float  = degrees(atan2(
            destination.y() - position.y(),
            destination.x() - position.x()))
        target_yaw_angle += 90
        return self.format_yaw_angle(target_yaw_angle)
    
    def find_best_pitch_angle(self, position : QVector3D, destination : QVector3D) -> float:
        """Finds best pitch angle for the given destination"""
        target_pitch_angle : float = degrees(atan2(
            destination.z() - position.z(),
            dist(position.toTuple(), destination.toTuple())))
        return target_pitch_angle

    def update_target_yaw_pitch_angles(self) -> None:
        """Updates current yaw angle"""
        if self.destinations and self.autopilot and not self.ignore_destinations:
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
            self.target_pitch_angle = self.find_best_pitch_angle(
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
        self.update_target_yaw_pitch_angles()
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
        if self.initial_target is not None:
            self.add_first_destination(self.initial_target)
        self.__target_yaw_angle = 0.0
        self.__target_roll_angle = 0.0
        self.__target_pitch_angle = 0.0
        self.__evade_maneuver = False
        self.__vector_sharing_resolution = None
        self.__safe_zone_occupied = False
        self.__autopilot = True
        self.__ignore_destinations = False
        self.__is_turning_right = False
        self.__is_turning_left = False

    def __str__(self) -> str:
        return f"AircraftFCC: {self.aircraft_id}"
    
    def __repr__(self) -> str:
        return f"AircraftFCC: {self.aircraft_id}"
    
    def __del__(self) -> None:
        with QMutexLocker(self.__mutex):
            del self.__aircraft_id
            del self.__aircraft
            del self.__destinations
            del self.__destinations_history
            del self.__visited
            del self.__autopilot
            del self.__ignore_destinations
            del self.__initial_target
            del self.__target_yaw_angle
            del self.__target_roll_angle
            del self.__target_pitch_angle
            del self.__target_speed
            del self.__is_turning_right
            del self.__is_turning_left
            del self.__safe_zone_occupied
            del self.__evade_maneuver
            del self.__vector_sharing_resolution
            del self.__mutex
            del self
