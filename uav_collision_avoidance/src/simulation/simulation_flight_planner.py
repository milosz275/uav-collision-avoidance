# simulation_flight_planner.py

from typing import List

from PySide6.QtCore import QThread

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class SimulationFlightPlanner(QThread):
    """Thread running UAVs' internal flight planner"""

    def __init__(self, parent, aircrafts : List[AircraftVehicle], simulation_state : SimulationState) -> None:
        super(SimulationFlightPlanner, self).__init__(parent)
        self.aircrafts = aircrafts
        self.simulation_state = simulation_state
        return
        
    def run(self) -> None:
        """Runs flight controller simulation thread"""
        while not self.isInterruptionRequested():
            if not self.simulation_state.is_paused:
                for aircraft in self.aircrafts:
                    pass
            self.msleep(self.simulation_state.simulation_threshold)
        return super().run()
