# simulation_physics.py

from copy import copy
from math import sin, cos, dist, tan, radians, degrees
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
        self.cycles : int = 0
        return

    def run(self) -> None:
        """Runs physics simulation thread"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            if not self.simulation_state.is_paused:
                self.count_cycles()
                elapsed_time : float = self.simulation_state.simulation_threshold # * self.simulation_state.time_scale
                self.update_aircrafts(elapsed_time)
                for aircraft in self.aircrafts:
                    old_pos : QVector3D = copy(aircraft.position)
                    aircraft.move(
                        aircraft.speed.x() * elapsed_time / 1000.0,
                        aircraft.speed.y() * elapsed_time / 1000.0,
                        aircraft.speed.z() * elapsed_time / 1000.0)
                    aircraft.distance_covered += dist(old_pos.toTuple(), aircraft.position.toTuple())
            self.msleep(max(0, (self.simulation_state.simulation_threshold) - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()

    def update_aircrafts(self, elapsed_time : float) -> None:
        """"""
        if elapsed_time == 0.0:
            return
        for aircraft in self.aircrafts:
            # flight control computer
            aircraft.fcc().update()

            # roll angle
            aircraft.roll_angle(aircraft.roll_angle() + ((1.0 / (aircraft.roll_dynamic_delay / elapsed_time)) * (aircraft.fcc().target_roll_angle - aircraft.roll_angle)))

            # pitch angle

            # yaw angle
            if aircraft.roll_angle == 0.0:
                return
            current_yaw_angle : float = aircraft.yaw_angle()
            current_horizontal_speed : float = aircraft.horizontal_speed()
            delta_yaw_angle : float = self.simulation_state.g_acceleration * tan(radians(aircraft.roll_angle)) / (current_horizontal_speed / elapsed_time)

            new_yaw_angle_radians : float = radians(current_yaw_angle)
            new_yaw_angle_radians += radians(delta_yaw_angle)
            new_yaw_angle : float = degrees(new_yaw_angle_radians)

            aircraft.speed.setX(sin(radians(new_yaw_angle)) * current_horizontal_speed)
            aircraft.speed.setY(-cos(radians(new_yaw_angle)) * current_horizontal_speed)
        return

    def count_cycles(self) -> None:
        """"""
        self.cycles += 1
        self.simulation_state.physics_cycles = self.cycles
        return
