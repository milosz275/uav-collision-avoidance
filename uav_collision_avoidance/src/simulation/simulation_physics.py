# simulation_physics.py

import sys
from typing import List

from PySide6.QtCore import QThread, QTime
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class SimulationPhysics(QThread):
    """Thread running simulation's physics"""

    def __init__(self, parent, aircrafts : List[AircraftVehicle], simulation_state : SimulationState) -> None:
        super(SimulationPhysics, self).__init__(parent)
        self.aircrafts = aircrafts
        self.simulation_state = simulation_state
        self.previous_timestamp = QTime.currentTime()
        return
        
    def run(self) -> None:
        """Runs physics simulation thread"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            if not self.simulation_state.is_paused:
                for aircraft in self.aircrafts:
                    # todo: calculate move deltas using previous and start timestamps
                    elapsed_time : float = self.previous_timestamp.msecsTo(start_timestamp)
                    delta_pos : QVector3D = QVector3D(
                        aircraft.speed.x() * elapsed_time,
                        aircraft.speed.y() * elapsed_time,
                        aircraft.speed.z() * elapsed_time,
                    )
                    aircraft.move(
                        delta_pos.x() / 1000.0,
                        delta_pos.y() / 1000.0,
                        delta_pos.z() / 1000.0,
                    )
                self.previous_timestamp = QTime.currentTime()
            self.msleep(max(0, (self.simulation_state.simulation_threshold) - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()
