"""Aircraft class module"""

from copy import copy

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from .aircraft_vehicle import AircraftVehicle
from .aircraft_fcc import AircraftFCC

class Aircraft(QObject):
    """Main aircraft class"""
    
    __current_id : int = 0

    def __init__(self, position : QVector3D, speed : QVector3D, initial_target : QVector3D | None = None) -> None:
        super().__init__()
        self.__aircraft_id = self.__obtain_id()
        self.__vehicle = AircraftVehicle(self.__aircraft_id, position=position, speed=speed)
        self.__fcc = AircraftFCC(self.__aircraft_id, initial_target, self.__vehicle)
        self.__initial_position = copy(position)
        self.__initial_speed = copy(speed)
    
    @property
    def vehicle(self) -> AircraftVehicle:
        """Returns aircraft vehicle"""
        return self.__vehicle
    
    @property
    def fcc(self) -> AircraftFCC:
        """Returns aircraft fcc"""
        return self.__fcc
    
    @property
    def initial_position(self) -> QVector3D:
        """Returns initial position"""
        return self.__initial_position
    
    @property
    def initial_speed(self) -> QVector3D:
        """Returns initial speed"""
        return self.__initial_speed

    def __obtain_id(self) -> int:
        """Gets unique id for the aircraft"""
        aircraft_id = Aircraft.__current_id
        Aircraft.__current_id += 1
        return aircraft_id
    
    def reset(self) -> None:
        """Resets aircraft to initial state"""
        self.__vehicle.speed = copy(self.initial_speed)
        self.__vehicle.position = copy(self.initial_position)
