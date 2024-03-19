"""Simulation physics thread module"""

import logging
from copy import copy
from math import sin, cos, dist, tan, radians, degrees
from typing import List

from PySide6.QtCore import QThread, QTime
from PySide6.QtGui import QVector3D
from PySide6.QtWidgets import QApplication

from src.aircraft.aircraft import Aircraft
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_fcc import AircraftFCC
from src.simulation.simulation_state import SimulationState

class SimulationPhysics(QThread):
    """Thread running simulation's physics"""

    def __init__(self, parent, aircrafts : List[Aircraft], simulation_state : SimulationState) -> None:
        super(SimulationPhysics, self).__init__(parent)
        self.aircrafts = aircrafts
        self.aircraft_vehicles : List[AircraftVehicle] = [aircraft.vehicle() for aircraft in self.aircrafts]
        self.aircraft_fccs : List[AircraftFCC] = [aircraft.fcc() for aircraft in self.aircrafts]
        self.simulation_state = simulation_state
        self.cycles : int = 0
        self.global_start_timestamp : QTime = None
        self.global_stop_timestamp : QTime = None
        return

    def run(self) -> None:
        """Runs physics simulation thread"""
        self.global_start_timestamp = QTime.currentTime()
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            if self.simulation_state.reset_demanded:
                self.simulation_state.apply_reset()
                self.aircraft_vehicles[0].teleport(10, 10, 1000)
                self.aircraft_vehicles[1].teleport(100, 100, 1000)
            if not self.simulation_state.is_paused:
                self.count_cycles()
                self.simulation_state.update_simulation_settings()
                elapsed_time : float = self.simulation_state.simulation_threshold # * self.simulation_state.time_scale
                self.update_aircrafts_speed_angles(elapsed_time)
                if self.update_aircrafts_position(elapsed_time):
                    logging.info("Aircrafts collided")
                    QApplication.beep()
                    self.requestInterruption()
            self.msleep(max(0, (self.simulation_state.simulation_threshold) - start_timestamp.msecsTo(QTime.currentTime())))
        self.global_stop_timestamp = QTime.currentTime()
        return super().run()

    def update_aircrafts_position(self, elapsed_time : float) -> bool:
        """Updates aircrafts position, returns true on collision"""
        for aircraft in self.aircraft_vehicles:
            miss_distance : float = dist(aircraft.position().toTuple(), self.aircraft_vehicles[1 - aircraft.aircraft_id()].position().toTuple())
            fcc : AircraftFCC = self.aircraft_fccs[aircraft.aircraft_id()]
            
            # safezone occupancy
            if miss_distance <= (fcc.safezone_size() / 2):
                if not fcc.safezone_occupied():
                    fcc.safezone_occupied(True)
                    print("Aircraft " + str(1 - aircraft.aircraft_id()) + " entered safezone of Aircraft " + str(aircraft.aircraft_id()))
            else:
                if fcc.safezone_occupied():
                    fcc.safezone_occupied(False)
                    print("Aircraft " + str(1 - aircraft.aircraft_id()) + " left safezone of Aircraft " + str(aircraft.aircraft_id()))

            # collision
            if miss_distance <= aircraft.size():
                print("Collision")
                return True
                
            # covered distance and position
            old_pos : QVector3D = copy(aircraft.position())
            aircraft.move(
                aircraft.speed().x() * elapsed_time / 1000.0,
                aircraft.speed().y() * elapsed_time / 1000.0,
                aircraft.speed().z() * elapsed_time / 1000.0)
            aircraft.distance_covered(dist(old_pos.toTuple(), aircraft.position().toTuple()))
        return False
    
    def update_aircrafts_speed_angles(self, elapsed_time : float) -> None:
        """Updates aircrafts movement speed and angles"""
        if elapsed_time == 0.0:
            return
        for aircraft in self.aircraft_vehicles:
            fcc : AircraftFCC = self.aircraft_fccs[aircraft.aircraft_id()]
            
            # flight control computer
            fcc.update()

            # roll angle
            aircraft.roll_angle((1.0 / (aircraft.roll_dynamic_delay / elapsed_time)) * (fcc.target_roll_angle - aircraft.roll_angle()))

            # pitch angle

            # yaw angle
            roll_angle : float = aircraft.roll_angle()

            if roll_angle == 0.0:
                continue
            elif fcc.target_roll_angle > 0.0 and roll_angle < 0.0:
                continue
            elif fcc.target_roll_angle < 0.0 and roll_angle > 0.0:
                continue

            current_yaw_angle : float = aircraft.yaw_angle()
            target_yaw_angle : float = fcc.target_yaw_angle
            if abs(current_yaw_angle - target_yaw_angle) < 0.001:
                continue
            current_horizontal_speed : float = aircraft.horizontal_speed()
            max_delta_yaw_angle : float = self.simulation_state.g_acceleration * tan(radians(roll_angle)) / (current_horizontal_speed / elapsed_time)
            max_delta_yaw_angle = abs(max_delta_yaw_angle)
            if roll_angle < 0.0:
                max_delta_yaw_angle = -max_delta_yaw_angle

            new_yaw_angle : float = 0.0
            if abs(current_yaw_angle - target_yaw_angle) < abs(max_delta_yaw_angle):
                new_yaw_angle = target_yaw_angle
            else:
                new_yaw_angle = current_yaw_angle + max_delta_yaw_angle

            aircraft.speed().setX(sin(radians(new_yaw_angle)) * current_horizontal_speed)
            aircraft.speed().setY(-cos(radians(new_yaw_angle)) * current_horizontal_speed)
        return

    def count_cycles(self) -> None:
        """Increments physics cycle counter"""
        self.cycles += 1
        self.simulation_state.physics_cycles = self.cycles
        return
