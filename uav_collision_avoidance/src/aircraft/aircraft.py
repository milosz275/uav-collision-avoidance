# aircraft.py

from src.aircraft.aircraft_render import AircraftRender
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class Aircraft():
    """Main aircraft class"""
    
    def __init__(self, x : float, y : float, color : str, state : SimulationState) -> None:
        self.vehicle = AircraftVehicle(x=x, y=y, speed=100, state=state)
        self.render = AircraftRender(color=color, vehicle=self.vehicle, state=state)
        return
