"""Simulation data module"""

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D


class SimulationData(QObject):
    """Simulation data class"""

    def __init__(self) -> None:
        super().__init__()
        self.__aircraft_1_initial_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_initial_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_final_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_final_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_initial_roll_angle : float = 0.0
        self.__aircraft_2_initial_roll_angle : float = 0.0
        self.__collision : bool | None = None
        self.__minimal_miss_distance : float | None = None

    @property
    def aircraft_1_initial_position(self) -> QVector3D:
        """Returns aircraft 1 initial position"""
        return self.__aircraft_1_initial_position
    
    @aircraft_1_initial_position.setter
    def aircraft_1_initial_position(self, position : QVector3D) -> None:
        """Sets aircraft 1 initial position"""
        self.__aircraft_1_initial_position = position

    @property
    def aircraft_2_initial_position(self) -> QVector3D:
        """Returns aircraft 2 initial position"""
        return self.__aircraft_2_initial_position
    
    @aircraft_2_initial_position.setter
    def aircraft_2_initial_position(self, position : QVector3D) -> None:
        """Sets aircraft 2 initial position"""
        self.__aircraft_2_initial_position = position

    @property
    def aircraft_1_final_position(self) -> QVector3D:
        """Returns aircraft 1 final position"""
        return self.__aircraft_1_final_position
    
    @aircraft_1_final_position.setter
    def aircraft_1_final_position(self, position : QVector3D) -> None:
        """Sets aircraft 1 final position"""
        self.__aircraft_1_final_position = position

    @property
    def aircraft_2_final_position(self) -> QVector3D:
        """Returns aircraft 2 final position"""
        return self.__aircraft_2_final_position
    
    @aircraft_2_final_position.setter
    def aircraft_2_final_position(self, position : QVector3D) -> None:
        """Sets aircraft 2 final position"""
        self.__aircraft_2_final_position = position

    @property
    def aircraft_1_initial_roll_angle(self) -> float:
        """Returns aircraft 1 initial roll angle"""
        return self.__aircraft_1_initial_roll_angle
    
    @aircraft_1_initial_roll_angle.setter
    def aircraft_1_initial_roll_angle(self, roll_angle : float) -> None:
        """Sets aircraft 1 initial roll angle"""
        self.__aircraft_1_initial_roll_angle = roll_angle

    @property
    def aircraft_2_initial_roll_angle(self) -> float:
        """Returns aircraft 2 initial roll angle"""
        return self.__aircraft_2_initial_roll_angle
    
    @aircraft_2_initial_roll_angle.setter
    def aircraft_2_initial_roll_angle(self, roll_angle : float) -> None:
        """Sets aircraft 2 initial roll angle"""
        self.__aircraft_2_initial_roll_angle = roll_angle

    @property
    def collision(self) -> bool | None:
        """Returns collision"""
        return self.__collision
    
    @collision.setter
    def collision(self, collision : bool) -> None:
        """Sets collision"""
        self.__collision = collision

    @property
    def minimal_miss_distance(self) -> float | None:
        """Returns minimal miss distance"""
        return self.__minimal_miss_distance
    
    @minimal_miss_distance.setter
    def minimal_miss_distance(self, distance : float) -> None:
        """Sets minimal miss distance"""
        self.__minimal_miss_distance = distance

    def reset(self) -> None:
        """Resets simulation data"""
        self.__aircraft_1_initial_position = QVector3D(0, 0, 0)
        self.__aircraft_2_initial_position = QVector3D(0, 0, 0)
        self.__aircraft_1_final_position = QVector3D(0, 0, 0)
        self.__aircraft_2_final_position = QVector3D(0, 0, 0)
        self.__aircraft_1_initial_roll_angle = 0.0
        self.__aircraft_2_initial_roll_angle = 0.0
        self.__collision = False
        self.__minimal_miss_distance = 0.0
