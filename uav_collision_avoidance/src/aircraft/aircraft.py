# aircraft.py

from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_render import AircraftRender
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class Aircraft():
    """Main aircraft class"""
    
    def __init__(self, x : float, y : float, height : float, color : str, state : SimulationState) -> None:
        self.vehicle = AircraftVehicle(position=QVector3D(x, y, height), speed=QVector3D(50, 0 , 50), state=state)
        self.render = AircraftRender(color=color, vehicle=self.vehicle, state=state)
        return
