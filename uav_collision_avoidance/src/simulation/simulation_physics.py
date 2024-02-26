# simulation_physics.py

from copy import copy
from math import sin, cos, dist
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

        # global dynamics
        self.roll_dynamic_delay : float = 300 # ms
        self.pitch_dynamic_delay : float = 400 # ms
        return
        
    def run(self) -> None:
        """Runs physics simulation thread"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            if not self.simulation_state.is_paused:
                elapsed_time : float = self.previous_timestamp.msecsTo(start_timestamp) * self.simulation_state.time_scale
                for aircraft in self.aircrafts:
                    aircraft.adjust_roll_angle((1.0 / self.roll_dynamic_delay) * (aircraft.fcc.target_roll_angle - aircraft.roll_angle))
                    delta_pos : QVector3D = QVector3D( # m/ms
                        aircraft.speed.x() * elapsed_time,
                        aircraft.speed.y() * elapsed_time,
                        aircraft.speed.z() * elapsed_time,
                    )
                    old_pos : QVector3D = copy(aircraft.position)
                    aircraft.move( # m/s
                        delta_pos.x() / 1000.0,
                        delta_pos.y() / 1000.0,
                        delta_pos.z() / 1000.0,
                    )
                    aircraft.distance_covered += dist(old_pos.toTuple(), aircraft.position.toTuple())
            self.previous_timestamp = QTime.currentTime()
            self.msleep(max(0, (self.simulation_state.simulation_threshold) - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()
