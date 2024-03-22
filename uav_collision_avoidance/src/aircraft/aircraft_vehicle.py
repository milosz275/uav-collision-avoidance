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
        self.__course : float = self.yaw_angle
        self.__roll_angle = 0.0 # bank angle
        self.__distance_covered : float = 0.0

    @property
    def aircraft_id(self) -> int:
        """Returns aircraft id"""
        return self.__aircraft_id
    
    @property
    def position(self) -> QVector3D:
        """Returns position"""
        return self.__position
    
    @property
    def speed(self) -> QVector3D:
        """Returns speed"""
        return self.__speed
    
    @property
    def size(self) -> float:
        """Returns size"""
        return self.__size
    
    @property
    def roll_angle(self) -> float:
        """Returns roll angle"""
        return self.__roll_angle

    @roll_angle.setter
    def roll_angle(self, roll_angle_delta : float):
        self.__roll_angle += roll_angle_delta
    
    @property
    def distance_covered(self) -> float:
        """Returns covered distance"""
        return self.__distance_covered

    @distance_covered.setter
    def distance_covered(self, distance_covered_delta : float):
        """Appends delta to distance covered"""
        self.__distance_covered += distance_covered_delta
    
    def teleport(self, x : float, y : float, z : float = 0.0) -> None:
        """Teleports the vehicle"""
        with QMutexLocker(self.__mutex):
            self.__position.setX(x)
            self.__position.setY(y)
            self.__position.setZ(z)

    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        """Applies position deltas for the vehicle"""
        with QMutexLocker(self.__mutex):
            self.__position.setX(self.__position.x() + dx)
            self.__position.setY(self.__position.y() + dy)
            self.__position.setZ(self.__position.z() + dz)
    
    def accelerate(self, dx : float, dy : float, dz : float) -> None:
        """Applies speed deltas to the speed"""
        with QMutexLocker(self.__mutex):
            if self.__speed.x() + dx >= 0:
                self.__speed.setX(self.__speed.x() + dx)
            if self.__speed.y() + dy >= 0:
                self.__speed.setY(self.__speed.y() + dy)
            if self.__speed.z() + dz >= 0:
                self.__speed.setZ(self.__speed.z() + dz)
    
    def roll(self, dy) -> None:
        """Applies roll angle delta of the aircraft"""
        with QMutexLocker(self.__mutex):
            self.__roll_angle += dy
    
    @property
    def absolute_speed(self) -> float:
        """Returns absolute speed"""
        with QMutexLocker(self.__mutex):
            return self.__speed.length()
    
    @property
    def horizontal_speed(self) -> float:
        """Returns horizontal speed"""
        with QMutexLocker(self.__mutex):
            return QVector3D(self.__speed.x(), self.__speed.y(), 0).length()
    
    @property
    def vertical_speed(self) -> float:
        """Returns vertical speed"""
        with QMutexLocker(self.__mutex):
            return QVector3D(0, 0, self.__speed.z()).length()

    @property
    def yaw_angle(self, speed : QVector3D | None = None) -> float:
        """Returns yaw (heading) angle"""
        if speed is None:
            with QMutexLocker(self.__mutex):
                return degrees(atan2(self.__speed.x(), -self.__speed.y()))
        else:
            return degrees(atan2(speed.x(), -speed.y()))

    @property
    def pitch_angle(self) -> float:
        """Returns pitch angle"""
        with QMutexLocker(self.__mutex):
            return degrees(atan2(self.__speed.z(), sqrt(self.__speed.x() ** 2 + self.__speed.y() ** 2)))
