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
        self.aircraft_id = self.get_id()
        self.fcc = AircraftFCC()
        self.vehicle = AircraftVehicle(self.aircraft_id, position=QVector3D(x, y, height), speed=QVector3D(60, 60, 0), fcc=self.fcc, state=state)
        self.render = AircraftRender(self.aircraft_id, vehicle=self.vehicle, fcc=self.fcc, state=state)
        return

    def get_id(self):
        """Gets unique id for the aircraft"""
        aircraft_id = Aircraft.current_id
        Aircraft.current_id += 1
        return aircraft_id
