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

    def __init__(self, x : float, y : float, height : float, state : SimulationState) -> None:
        self.__aircraft_id = self.obtain_id()
        self.__fcc = AircraftFCC()
        self.__vehicle = AircraftVehicle(self.__aircraft_id, position=QVector3D(x, y, height), speed=QVector3D(100, 0, 0), fcc=self.__fcc, state=state)
        self.__render = AircraftRender(self.__aircraft_id, vehicle=self.__vehicle, fcc=self.__fcc, state=state)
        return
    
    def vehicle(self):
        return self.__vehicle
    
    def render(self):
        return self.__render

    def obtain_id(self):
        """Gets unique id for the aircraft"""
        aircraft_id = Aircraft.current_id
        Aircraft.current_id += 1
        return aircraft_id
