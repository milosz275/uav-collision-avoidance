"""Simulation data module"""

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

class SimulationData(QObject):
    """Simulation data class"""

    def __init__(self) -> None:
        super().__init__()
        self.__aircraft_angle : float = 0.0
        self.__aircraft_1_initial_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_initial_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_final_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_final_position : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_initial_speed : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_initial_speed : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_final_speed : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_final_speed : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_initial_target : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_2_initial_target : QVector3D = QVector3D(0, 0, 0)
        self.__aircraft_1_initial_roll_angle : float = 0.0
        self.__aircraft_2_initial_roll_angle : float = 0.0
        self.__collision : bool | None = None
        self.__minimal_relative_distance : float | None = None
        self.__miss_distance_at_closest_approach : float | None = None

    @property
    def aircraft_angle(self) -> float:
        """Returns initial angle between aircrafts"""
        return self.__aircraft_angle
    
    @aircraft_angle.setter
    def aircraft_angle(self, angle : float) -> None:
        """Sets initial angle between aircrafts"""
        self.__aircraft_angle = angle

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
    def aircraft_1_initial_speed(self) -> QVector3D:
        """Returns aircraft 1 initial speed"""
        return self.__aircraft_1_initial_speed
    
    @aircraft_1_initial_speed.setter
    def aircraft_1_initial_speed(self, speed : QVector3D) -> None:
        """Sets aircraft 1 initial speed"""
        self.__aircraft_1_initial_speed = speed

    @property
    def aircraft_2_initial_speed(self) -> QVector3D:
        """Returns aircraft 2 initial speed"""
        return self.__aircraft_2_initial_speed
    
    @aircraft_2_initial_speed.setter
    def aircraft_2_initial_speed(self, speed : QVector3D) -> None:
        """Sets aircraft 2 initial speed"""
        self.__aircraft_2_initial_speed = speed

    @property
    def aircraft_1_final_speed(self) -> QVector3D:
        """Returns aircraft 1 final speed"""
        return self.__aircraft_1_final_speed
    
    @aircraft_1_final_speed.setter
    def aircraft_1_final_speed(self, speed : QVector3D) -> None:
        """Sets aircraft 1 final speed"""
        self.__aircraft_1_final_speed = speed

    @property
    def aircraft_2_final_speed(self) -> QVector3D:
        """Returns aircraft 2 final speed"""
        return self.__aircraft_2_final_speed
    
    @aircraft_2_final_speed.setter
    def aircraft_2_final_speed(self, speed : QVector3D) -> None:
        """Sets aircraft 2 final speed"""
        self.__aircraft_2_final_speed = speed

    @property
    def aircraft_1_initial_target(self) -> QVector3D:
        """Returns aircraft 1 initial target"""
        return self.__aircraft_1_initial_target
    
    @aircraft_1_initial_target.setter
    def aircraft_1_initial_target(self, target : QVector3D) -> None:
        """Sets aircraft 1 initial target"""
        self.__aircraft_1_initial_target = target

    @property
    def aircraft_2_initial_target(self) -> QVector3D:
        """Returns aircraft 2 initial target"""
        return self.__aircraft_2_initial_target
    
    @aircraft_2_initial_target.setter
    def aircraft_2_initial_target(self, target : QVector3D) -> None:
        """Sets aircraft 2 initial target"""
        self.__aircraft_2_initial_target = target

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
    def minimal_relative_distance(self) -> float | None:
        """Returns minimal miss distance"""
        return self.__minimal_relative_distance
    
    @minimal_relative_distance.setter
    def minimal_relative_distance(self, distance : float) -> None:
        """Sets minimal miss distance"""
        self.__minimal_relative_distance = distance
        
    @property
    def miss_distance_at_closest_approach(self) -> float | None:
        """Returns miss distance at closest approach"""
        return self.__miss_distance_at_closest_approach
    
    @miss_distance_at_closest_approach.setter
    def miss_distance_at_closest_approach(self, distance : float) -> None:
        """Sets miss distance at closest approach"""
        self.__miss_distance_at_closest_approach = distance

    def reset(self) -> None:
        """Resets simulation data"""
        self.__aircraft_1_initial_position = QVector3D(0, 0, 0)
        self.__aircraft_2_initial_position = QVector3D(0, 0, 0)
        self.__aircraft_1_final_position = QVector3D(0, 0, 0)
        self.__aircraft_2_final_position = QVector3D(0, 0, 0)
        self.__aircraft_1_initial_roll_angle = 0.0
        self.__aircraft_2_initial_roll_angle = 0.0
        self.__collision = False
        self.__minimal_relative_distance = 0.0
