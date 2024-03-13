# aircraft.py

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_render import AircraftRender
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_fcc import AircraftFCC
from src.simulation.simulation_state import SimulationState

class Aircraft(QObject):
    """Main aircraft class"""
    
    current_id : int = 0

    def __init__(self, position : QVector3D, speed : QVector3D, state : SimulationState) -> None:
        self.__aircraft_id = self.__obtain_id__()
        self.__vehicle = AircraftVehicle(self.__aircraft_id, position=position, speed=speed, state=state)
        self.__fcc = AircraftFCC(self.__aircraft_id, self.__vehicle)
        self.__render = AircraftRender(self.__aircraft_id, vehicle=self.__vehicle, fcc=self.__fcc, state=state)
        return
    
    def vehicle(self) -> AircraftVehicle:
        """Returns aircraft vehicle"""
        return self.__vehicle
    
    def fcc(self) -> AircraftFCC:
        """Returns aircraft fcc"""
        return self.__fcc
    
    def render(self) -> AircraftRender:
        """Returns aircraft render"""
        return self.__render

    def __obtain_id__(self) -> int:
        """Gets unique id for the aircraft"""
        aircraft_id = Aircraft.current_id
        Aircraft.current_id += 1
        return aircraft_id
