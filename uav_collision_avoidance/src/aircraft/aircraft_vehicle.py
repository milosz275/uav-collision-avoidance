"""Aircraft physical UAV class definition"""

from math import atan2, degrees, sqrt

from PySide6.QtCore import QObject, QMutex, QMutexLocker
from PySide6.QtGui import QVector3D

from src.simulation.simulation_state import SimulationState

class AircraftVehicle(QObject):
    """Aircraft physical UAV"""

    roll_dynamic_delay : float = 1000 # ms
    pitch_dynamic_delay : float = 2000 # ms

    def __init__(self, aircraft_id : int, position : QVector3D, speed : QVector3D, state : SimulationState) -> None:
        super().__init__()
        self.__mutex : QMutex = QMutex()
        
        self.__aircraft_id = aircraft_id
        self.__position = position
        if self.__position.z() < 0:
            self.__position.setZ(0)
        self.__speed = speed

        self.__state = state

        self.__size : float = 20.0
        self.__course : float = self.yaw_angle()
        self.__roll_angle = 0.0 # bank angle
        self.__distance_covered : float = 0.0
        return
    
    def aircraft_id(self) -> int:
        """Returns aircraft id"""
        return self.__aircraft_id
    
    def position(self) -> QVector3D:
        """Returns position"""
        return self.__position
    
    def speed(self) -> QVector3D:
        """Returns speed"""
        return self.__speed
    
    def size(self) -> float:
        """Returns size"""
        return self.__size
    
    def roll_angle(self, roll_angle_delta : float = 0.0) -> float:
        """Returns roll angle"""
        self.__roll_angle += roll_angle_delta
        return self.__roll_angle
    
    def distance_covered(self, distance_covered_delta : float = 0.0) -> float:
        """Returns covered distance"""
        self.__distance_covered += distance_covered_delta
        return self.__distance_covered
    
    def teleport(self, x : float, y : float, z : float = 0.0) -> None:
        """Teleports the vehicle"""
        QMutexLocker(self.__mutex)
        self.__position.setX(x)
        self.__position.setY(y)
        self.__position.setZ(z)
        return

    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        """Applies position deltas for the vehicle"""
        QMutexLocker(self.__mutex)
        self.__position.setX(self.__position.x() + dx)
        self.__position.setY(self.__position.y() + dy)
        self.__position.setZ(self.__position.z() + dz)
        return
    
    def accelerate(self, dx : float, dy : float, dz : float) -> None:
        """Applies speed deltas to the speed"""
        QMutexLocker(self.__mutex)
        if self.__position.x() + dx >= 0:
            self.__position.setX(self.__position.x() + dx)
        if self.__position.y() + dy >= 0:
            self.__position.setY(self.__position.y() + dy)
        if self.__position.z() + dz >= 0:
            self.__position.setZ(self.__position.z() + dz)
        return
    
    def roll(self, dy) -> None:
        """Applies roll angle delta of the aircraft"""
        QMutexLocker(self.__mutex)
        self.__roll_angle += dy
        return
    
    def absolute_speed(self) -> float:
        """Returns absolute speed"""
        QMutexLocker(self.__mutex)
        return self.__speed.length()
    
    def horizontal_speed(self) -> float:
        """Returns horizontal speed"""
        QMutexLocker(self.__mutex)
        return QVector3D(self.__speed.x(), self.__speed.y(), 0).length()
    
    def vertical_speed(self) -> float:
        """Returns vertical speed"""
        QMutexLocker(self.__mutex)
        return QVector3D(0, 0, self.__speed.z()).length()

    def yaw_angle(self) -> float:
        """Returns yaw (heading) angle"""
        QMutexLocker(self.__mutex)
        return degrees(atan2(self.__speed.x(), -self.__speed.y()))

    def pitch_angle(self) -> float:
        """Returns pitch angle"""
        QMutexLocker(self.__mutex)
        return degrees(atan2(self.__speed.z(), sqrt(self.__speed.x() ** 2 + self.__speed.y() ** 2)))
