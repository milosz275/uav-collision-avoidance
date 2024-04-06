"""Simulation physics thread module"""

import logging
from copy import copy
from math import sin, cos, dist, tan, radians
from typing import List

from PySide6.QtCore import QThread, QTime
from PySide6.QtGui import QVector3D
from PySide6.QtWidgets import QApplication, QMainWindow

from ..aircraft.aircraft import Aircraft
from ..aircraft.aircraft_vehicle import AircraftVehicle
from ..aircraft.aircraft_fcc import AircraftFCC
from .simulation_state import SimulationState

class SimulationPhysics(QThread):
    """Thread running simulation's physics"""

    def __init__(self, parent : QMainWindow, aircrafts : List[Aircraft], simulation_state : SimulationState) -> None:
        super(SimulationPhysics, self).__init__(parent)
        self.aircrafts = aircrafts
        self.aircraft_vehicles : List[AircraftVehicle] = [aircraft.vehicle for aircraft in self.aircrafts]
        self.aircraft_fccs : List[AircraftFCC] = [aircraft.fcc for aircraft in self.aircrafts]
        self.simulation_state = simulation_state
        self.cycles : int = 0
        self.global_start_timestamp : QTime | None = None
        self.global_stop_timestamp : QTime | None = None

    def run(self) -> None:
        """Runs physics simulation thread"""
        self.mark_start_time()
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            self.cycle(self.simulation_state.simulation_threshold)
            self.msleep(max(0, (self.simulation_state.simulation_threshold) - start_timestamp.msecsTo(QTime.currentTime())))
        self.mark_stop_time()
        return super().run()
    
    def mark_start_time(self) -> None:
        """Marks start time of the simulation"""
        self.global_start_timestamp = QTime.currentTime()

    def mark_stop_time(self) -> None:
        """Marks stop time of the simulation"""
        self.global_stop_timestamp = QTime.currentTime()
    
    def cycle(self, elapsed_time : float) -> None:
        """Executes physics simulation cycle"""
        if self.simulation_state.reset_demanded:
            self.reset_aircrafts()
        if not self.simulation_state.is_paused:
            self.count_cycles()
            self.simulation_state.update_simulation_settings()
            self.update_aircrafts_speed_angles(elapsed_time)
            if self.update_aircrafts_position(elapsed_time):
                logging.warn("Aircrafts collided at coordinates: " + str(self.aircraft_vehicles[0].position.toTuple()) + " and " + str(self.aircraft_vehicles[1].position.toTuple()))
                QApplication.beep()
                self.simulation_state.register_collision()
                if self.isRunning():
                    self.requestInterruption()

    def reset_aircrafts(self) -> None:
        """Resets aircrafts to initial state"""
        self.aircrafts[0].reset()
        self.aircrafts[1].reset()
        self.aircraft_fccs[0].reset()
        self.aircraft_fccs[1].reset()
        self.simulation_state.apply_reset()

    def update_aircrafts_position(self, elapsed_time : float) -> bool:
        """Updates aircrafts position, returns true on collision"""
        for aircraft in self.aircraft_vehicles:
            relative_distance : float = dist(aircraft.position.toTuple(), self.aircraft_vehicles[1 - aircraft.aircraft_id].position.toTuple())
            if relative_distance <= aircraft.size:
                print("Collision")
                return True
            old_pos : QVector3D = copy(aircraft.position)
            aircraft.move(
                aircraft.speed.x() * elapsed_time / 1000.0,
                aircraft.speed.y() * elapsed_time / 1000.0,
                aircraft.speed.z() * elapsed_time / 1000.0)
            aircraft.distance_covered = dist(old_pos.toTuple(), aircraft.position.toTuple())
        return False
    
    def update_aircrafts_speed_angles(self, elapsed_time : float) -> None:
        """Updates aircrafts movement speed and angles"""
        assert elapsed_time > 0.0
        for aircraft in self.aircraft_vehicles:
            # flight control computer
            id : int = aircraft.aircraft_id
            fcc : AircraftFCC = self.aircraft_fccs[id]
            cause_collision = self.simulation_state.first_cause_collision if id == 0 else self.simulation_state.second_cause_collision
            fcc.update() if not cause_collision else fcc.update_target(self.aircraft_vehicles[1 - id].position + self.aircraft_vehicles[1 - id].speed)
            
            # speed
            current_speed = aircraft.absolute_speed
            target_speed = fcc.target_speed
            speed_difference = abs(current_speed - target_speed)
            if speed_difference > 0.001 and target_speed > 20.0:
                max_speed_delta = aircraft.max_acceleration / elapsed_time
                if speed_difference < max_speed_delta:
                    pass # become target
                elif current_speed < target_speed:
                    target_speed = current_speed + max_speed_delta
                else:
                    target_speed = current_speed - max_speed_delta
                speed_scale_factor : float = target_speed / current_speed
                aircraft.speed = QVector3D(
                    aircraft.speed.x() * speed_scale_factor,
                    aircraft.speed.y() * speed_scale_factor,
                    aircraft.speed.z() * speed_scale_factor)

            # roll angle
            aircraft.roll_angle = (1.0 / (aircraft.roll_dynamic_delay / elapsed_time)) * (fcc.target_roll_angle - aircraft.roll_angle)

            # pitch angle

            # yaw angle
            roll_angle : float = aircraft.roll_angle

            if roll_angle == 0.0:
                continue
            elif fcc.target_roll_angle > 0.0 and roll_angle < 0.0:
                continue
            elif fcc.target_roll_angle < 0.0 and roll_angle > 0.0:
                continue

            current_yaw_angle : float = aircraft.yaw_angle
            target_yaw_angle : float = fcc.target_yaw_angle
            if abs(current_yaw_angle - target_yaw_angle) < 0.001:
                continue
            current_horizontal_speed : float = aircraft.horizontal_speed
            max_delta_yaw_angle : float = self.simulation_state.g_acceleration * tan(radians(roll_angle)) / (current_horizontal_speed / elapsed_time)
            max_delta_yaw_angle = abs(max_delta_yaw_angle)
            if roll_angle < 0.0:
                max_delta_yaw_angle = -max_delta_yaw_angle

            new_yaw_angle : float = 0.0
            if abs(current_yaw_angle - target_yaw_angle) < abs(max_delta_yaw_angle):
                new_yaw_angle = target_yaw_angle
            else:
                new_yaw_angle = current_yaw_angle + max_delta_yaw_angle

            aircraft.speed.setX(sin(radians(new_yaw_angle)) * current_horizontal_speed)
            aircraft.speed.setY(-cos(radians(new_yaw_angle)) * current_horizontal_speed)

    def count_cycles(self) -> None:
        """Increments physics cycle counter"""
        self.cycles += 1
        self.simulation_state.physics_cycles = self.cycles
