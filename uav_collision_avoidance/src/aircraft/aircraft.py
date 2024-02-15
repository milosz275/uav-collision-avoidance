# aircraft.py

from src.aircraft.aircraft_render import AircraftRender
from src.aircraft.aircraft_vehicle import AircraftVehicle

class Aircraft():
    """Aircraft"""
    
    def __init__(self, x : float, y : float, color : str) -> None:
        self.vehicle = AircraftVehicle(x=x, y=y, speed=100)
        self.render = AircraftRender(color=color, vehicle=self.vehicle)
