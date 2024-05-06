"""Aircraft class module"""

from copy import copy

from PySide6.QtCore import QObject, QMutex, QMutexLocker
from PySide6.QtGui import QVector3D

from .aircraft_vehicle import AircraftVehicle
from .aircraft_fcc import AircraftFCC

class Aircraft(QObject):
    """Main aircraft class"""

    def __init__(self, aircraft_id : int, position : QVector3D, speed : QVector3D, initial_target : QVector3D | None = None, initial_roll_angle : float = 0.0) -> None:
        super().__init__()
        self.__mutex : QMutex = QMutex()
        self.__aircraft_id = aircraft_id
        self.__vehicle = AircraftVehicle(self.__aircraft_id, position=position, speed=speed, initial_roll_angle=initial_roll_angle)
        self.__fcc = AircraftFCC(self.__aircraft_id, initial_target, self.__vehicle)
        self.__initial_position = copy(position)
        self.__initial_speed = copy(speed)
        self.__initial_roll_angle = initial_roll_angle
    
    @property
    def vehicle(self) -> AircraftVehicle:
        """Returns aircraft vehicle"""
        with QMutexLocker(self.__mutex):
            return self.__vehicle
    
    @property
    def fcc(self) -> AircraftFCC:
        """Returns aircraft fcc"""
        with QMutexLocker(self.__mutex):
            return self.__fcc
    
    @property
    def initial_position(self) -> QVector3D:
        """Returns initial position"""
        with QMutexLocker(self.__mutex):
            return self.__initial_position
    
    @property
    def initial_speed(self) -> QVector3D:
        """Returns initial speed"""
        with QMutexLocker(self.__mutex):
            return self.__initial_speed
        
    @property
    def initial_roll_angle(self) -> float:
        """Returns initial roll angle"""
        with QMutexLocker(self.__mutex):
            return self.__initial_roll_angle

    def reset(self) -> None:
        """Resets aircraft to initial state"""
        self.__vehicle.speed = copy(self.initial_speed)
        self.__vehicle.position = copy(self.initial_position)
        self.__vehicle.roll_angle = copy(self.initial_roll_angle)
        self.__vehicle.reset_distance_covered()
