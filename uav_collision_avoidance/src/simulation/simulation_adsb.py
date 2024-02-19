# simulation_adsb.py

from typing import List

from PySide6.QtCore import QThread, QTime

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class SimulationADSB(QThread):
    """Thread running ADSB system for collision detection and avoidance"""

    def __init__(self, parent, aircrafts : List[AircraftVehicle], simulation_state : SimulationState) -> None:
        super(SimulationADSB, self).__init__(parent)
        self.aircrafts = aircrafts
        self.simulation_state = simulation_state
        return
        
    def run(self) -> None:
        """Runs ADS-B simulation thread with precise 1000ms timeout"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            if not self.simulation_state.is_paused:
                for aircraft in self.aircrafts:
                    print(str(aircraft.aircraft_id) + "- speed: " + str(aircraft.absolute_speed()))
            self.msleep(max(0, 1000 - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()
