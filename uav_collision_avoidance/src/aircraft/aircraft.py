# aircraft.py

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_render import AircraftRender
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class Aircraft(QObject):
    """Main aircraft class"""
    
    current_id : int = 0

    def __init__(self, x : float, y : float, height : float, color : str, state : SimulationState) -> None:
        self.aircraft_id = self.get_id()
        self.vehicle = AircraftVehicle(self.aircraft_id, position=QVector3D(x, y, height), speed=QVector3D(50, 50 , 0), state=state)
        self.render = AircraftRender(color=color, vehicle=self.vehicle, state=state)
        return

    def get_id(self):
        """Gets unique id for the aircraft"""
        aircraft_id = Aircraft.current_id
        Aircraft.current_id += 1
        return aircraft_id
