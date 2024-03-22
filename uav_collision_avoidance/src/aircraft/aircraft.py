"""Aircraft class module"""

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_fcc import AircraftFCC
from src.simulation.simulation_state import SimulationState

class Aircraft(QObject):
    """Main aircraft class"""
    
    __current_id : int = 0

    def __init__(self, position : QVector3D, speed : QVector3D, initial_target : QVector3D, state : SimulationState) -> None:
        self.__aircraft_id = self.__obtain_id()
        self.__vehicle = AircraftVehicle(self.__aircraft_id, position=position, speed=speed, state=state)
        self.__fcc = AircraftFCC(self.__aircraft_id, initial_target, self.__vehicle)
    
    @property
    def vehicle(self) -> AircraftVehicle:
        """Returns aircraft vehicle"""
        return self.__vehicle
    
    @property
    def fcc(self) -> AircraftFCC:
        """Returns aircraft fcc"""
        return self.__fcc

    def __obtain_id(self) -> int:
        """Gets unique id for the aircraft"""
        aircraft_id = Aircraft.__current_id
        Aircraft.__current_id += 1
        return aircraft_id