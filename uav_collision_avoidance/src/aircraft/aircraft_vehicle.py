# aircraft_vehicle.py

from math import atan2, degrees
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QVector3D

from src.simulation.simulation_state import SimulationState

class AircraftVehicle(QObject):
    """Aircraft physical UAV"""

    positionChanged = Signal(float, float, float)

    def __init__(self, aircraft_id : int, position : QVector3D, speed : QVector3D, state : SimulationState) -> None:
        super().__init__()
        self.aircraft_id = aircraft_id
        self.position = position
        if self.position.z() < 0:
            self.position.setZ(0)
        self.speed = speed
        self.state = state

        self.size : float = 20.0
        self.safezone_occupied : bool = False

        return

    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        """Applies delta position change for the vehicle"""
        self.position.setX(self.position.x() + dx)
        self.position.setY(self.position.y() + dy)
        self.position.setZ(self.position.z() + dz)
        self.positionChanged.emit(self.position.x(), self.position.y(), self.position.z())
        return
    
    def absolute_speed(self) -> float:
        """Returns absolute speed"""
        return self.speed.length()
    
    def horizontal_speed(self) -> float:
        """Returns horizontal speed"""
        return QVector3D(self.speed.x(), self.speed.y(), 0).length()
    
    def vertical_speed(self) -> float:
        """Returns vertical speed"""
        return QVector3D(0, 0, self.speed.z()).length()

    def yaw_angle(self) -> float:
        """Returns yaw angle"""
        return degrees(atan2(self.speed.y(), self.speed.x()))
