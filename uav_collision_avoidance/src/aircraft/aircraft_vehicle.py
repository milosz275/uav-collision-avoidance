"""Aircraft physical UAV class definition"""

from math import atan2, degrees, sqrt

from PySide6.QtCore import QObject, QMutex, QMutexLocker
from PySide6.QtGui import QVector3D

class AircraftVehicle(QObject):
    """Aircraft physical UAV"""

    roll_dynamic_delay : float = 1000 # ms
    pitch_dynamic_delay : float = 2000 # ms
    max_acceleration : float = 2.0 # m/s^2

    def __init__(self, aircraft_id : int, position : QVector3D, speed : QVector3D, initial_roll_angle : float) -> None:
        super().__init__()
        self.__mutex : QMutex = QMutex()
        
        self.__aircraft_id = aircraft_id
        self.__position = position
        if self.__position.z() < 0:
            self.__position.setZ(0)
        self.__speed = speed

        self.__size : float = 20.0
        self.__roll_angle = initial_roll_angle
        self.__initial_roll_angle = self.__roll_angle
        self.__distance_covered : float = 0.0

    @property
    def aircraft_id(self) -> int:
        """Returns aircraft id"""
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id
    
    @property
    def position(self) -> QVector3D:
        """Returns position"""
        with QMutexLocker(self.__mutex):
            return self.__position
    
    @position.setter
    def position(self, position : QVector3D) -> None:
        """Sets position"""
        del self.__position
        with QMutexLocker(self.__mutex):
            self.__position = position
    
    @property
    def speed(self) -> QVector3D:
        """Returns speed"""
        with QMutexLocker(self.__mutex):
            return self.__speed
    
    @speed.setter
    def speed(self, speed : QVector3D) -> None:
        """Sets speed"""
        with QMutexLocker(self.__mutex):
            self.__speed = speed
    
    @property
    def size(self) -> float:
        """Returns size"""
        with QMutexLocker(self.__mutex):
            return self.__size
    
    @property
    def roll_angle(self) -> float:
        """Returns roll angle"""
        with QMutexLocker(self.__mutex):
            return self.__roll_angle

    @roll_angle.setter
    def roll_angle(self, roll_angle_delta : float) -> None:
        """Adds roll angle delta"""
        with QMutexLocker(self.__mutex):
            self.__roll_angle += roll_angle_delta

    @property
    def initial_roll_angle(self) -> float:
        """Returns initial roll angle"""
        with QMutexLocker(self.__mutex):
            return self.__initial_roll_angle
    
    @property
    def distance_covered(self) -> float:
        """Returns covered distance"""
        with QMutexLocker(self.__mutex):
            return self.__distance_covered

    @distance_covered.setter
    def distance_covered(self, distance_covered_delta : float) -> None:
        """Appends delta to distance covered"""
        with QMutexLocker(self.__mutex):
            self.__distance_covered += distance_covered_delta

    def reset_distance_covered(self) -> None:
        """Resets distance covered"""
        with QMutexLocker(self.__mutex):
            self.__distance_covered = 0.0
    
    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        """Applies position deltas for the vehicle"""
        with QMutexLocker(self.__mutex):
            self.__position.setX(self.__position.x() + dx)
            self.__position.setY(self.__position.y() + dy)
            self.__position.setZ(self.__position.z() + dz)
    
    def roll(self, d_angle) -> None:
        """Applies roll angle delta of the aircraft"""
        with QMutexLocker(self.__mutex):
            self.__roll_angle += d_angle
    
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
    def yaw_angle(self) -> float:
        """Returns yaw (heading) angle"""
        with QMutexLocker(self.__mutex):
            return degrees(atan2(self.__speed.x(), -self.__speed.y()))
        
    @yaw_angle.getter
    def yaw_angle(self, speed : QVector3D | None = None) -> float:
        """Returns yaw (heading) angle of given speed vector"""
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

    def __str__(self) -> str:
        with QMutexLocker(self.__mutex):
            return f"Vehicle {self.__aircraft_id} at {self.__position} with speed {self.__speed} and roll angle {self.__roll_angle} degrees"
        
    def __repr__(self) -> str:
        with QMutexLocker(self.__mutex):
            return f"Vehicle {self.__aircraft_id} at {self.__position} with speed {self.__speed} and roll angle {self.__roll_angle} degrees"
        
    def __eq__(self, other) -> bool:
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id == other.__aircraft_id
        
    def __ne__(self, other) -> bool:
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id != other.__aircraft_id
        
    def __lt__(self, other) -> bool:
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id < other.__aircraft_id
        
    def __le__(self, other) -> bool:
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id <= other.__aircraft_id
        
    def __gt__(self, other) -> bool:
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id > other.__aircraft_id
        
    def __ge__(self, other) -> bool:
        with QMutexLocker(self.__mutex):
            return self.__aircraft_id >= other.__aircraft_id
        
    def __copy__(self):
        with QMutexLocker(self.__mutex):
            return AircraftVehicle(self.__aircraft_id, self.__position, self.__speed, self.__initial_roll_angle)

    def __deepcopy__(self, memo):
        with QMutexLocker(self.__mutex):
            return AircraftVehicle(self.__aircraft_id, self.__position, self.__speed, self.__initial_roll_angle)
        
    def __del__(self):
        with QMutexLocker(self.__mutex):
            del self.__position
            del self.__speed
            del self.__roll_angle
            del self.__initial_roll_angle
            del self.__distance_covered
            del self.__size
            del self.__aircraft_id
            del self.__mutex
            del self
