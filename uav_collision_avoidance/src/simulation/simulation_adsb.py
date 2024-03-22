"""Simulation ADS-B system simulation thread module"""

from typing import List

from PySide6.QtCore import QThread, QTime

from src.aircraft.aircraft import Aircraft
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_fcc import AircraftFCC
from src.simulation.simulation_state import SimulationState

class SimulationADSB(QThread):
    """Thread running ADS-B system for collision detection and avoidance"""

    def __init__(self, parent, aircrafts : List[Aircraft], simulation_state : SimulationState) -> None:
        super(SimulationADSB, self).__init__(parent)
        self.aircrafts = aircrafts
        self.aircraft_vehicles : List[AircraftVehicle] = [aircraft.vehicle for aircraft in self.aircrafts]
        self.aircraft_fccs : List[AircraftFCC] = [aircraft.fcc for aircraft in self.aircrafts]
        self.simulation_state = simulation_state
        self.adsb_cycles : int = 0
        return
        
    def run(self) -> None:
        """Runs ADS-B simulation thread with precise timeout"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            if not self.simulation_state.is_paused and self.simulation_state.adsb_report:
                self.adsb_cycles += 1
                self.simulation_state.update_adsb_settings()
                for aircraft in self.aircraft_vehicles:
                    self.aircraft_fccs[aircraft.aircraft_id].append_visited()
                    if aircraft.aircraft_id == 0:
                        print("Aircraft id: " + str(aircraft.aircraft_id) +
                            "; speed: " + "{:.2f}".format(aircraft.absolute_speed) +
                            "; x: " + "{:.2f}".format(aircraft.position.x()) +
                            "; y: " + "{:.2f}".format(aircraft.position.y()) +
                            "; yaw angle: " + "{:.2f}".format(aircraft.yaw_angle) +
                            "; target yaw angle: " + "{:.2f}".format(self.aircraft_fccs[aircraft.aircraft_id].target_yaw_angle) +
                            "; pitch angle: " + "{:.2f}".format(aircraft.pitch_angle) +
                            "; roll angle: " + "{:.2f}".format(aircraft.roll_angle) +
                            "; target roll angle: " + "{:.2f}".format(self.aircraft_fccs[aircraft.aircraft_id].target_roll_angle) +
                            "; distance covered: " + "{:.2f}".format(aircraft.distance_covered) +
                            "; fps: " + "{:.2f}".format(self.simulation_state.fps) +
                            "; t: " + str(self.adsb_cycles) +
                            "; phys: " + str(self.simulation_state.physics_cycles))
            self.msleep(max(0, self.simulation_state.adsb_threshold - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()
