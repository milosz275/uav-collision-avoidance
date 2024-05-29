"""Simulation ADS-B system simulation thread module"""

import logging
import numpy as np
from typing import List
from math import sqrt

from PySide6.QtCore import QThread, QTime
from PySide6.QtGui import QVector3D
from PySide6.QtWidgets import QMainWindow

from ..aircraft.aircraft import Aircraft
from ..aircraft.aircraft_vehicle import AircraftVehicle
from ..aircraft.aircraft_fcc import AircraftFCC
from .simulation_state import SimulationState

class SimulationADSB(QThread):
    """Thread running ADS-B system for collision detection and avoidance"""

    def __init__(self, parent : QMainWindow, aircrafts : List[Aircraft], simulation_state : SimulationState) -> None:
        super(SimulationADSB, self).__init__(parent)
        self.__aircrafts = aircrafts
        self.__aircraft_vehicles : List[AircraftVehicle] = [aircraft.vehicle for aircraft in self.aircrafts]
        self.__aircraft_fccs : List[AircraftFCC] = [aircraft.fcc for aircraft in self.aircrafts]
        self.__simulation_state = simulation_state
        self.__adsb_cycles : int = 0
        self.__minimal_relative_distance : float = float("inf")
        self.__is_silent : bool = True
        self.__miss_distance_at_closest_approach : float | np.nan = np.nan
        
    @property
    def aircrafts(self) -> List[Aircraft]:
        """Returns aircrafts"""
        return self.__aircrafts
    
    @property
    def aircraft_vehicles(self) -> List[AircraftVehicle]:
        """Returns aircraft vehicles"""
        self.__aircraft_vehicles = [aircraft.vehicle for aircraft in self.aircrafts]
        return self.__aircraft_vehicles
    
    @property
    def aircraft_fccs(self) -> List[AircraftFCC]:
        """Returns aircraft flight control computers"""
        self.__aircraft_fccs = [aircraft.fcc for aircraft in self.aircrafts]
        return self.__aircraft_fccs
    
    @property
    def simulation_state(self) -> SimulationState:
        """Returns simulation state"""
        return self.__simulation_state
    
    @property
    def adsb_cycles(self) -> int:
        """Returns ADS-B cycles count"""
        return self.__adsb_cycles
    
    def count_adsb_cycles(self) -> None:
        """Increments ADS-B cycle counter"""
        self.__adsb_cycles += 1
        self.simulation_state.adsb_cycles = self.adsb_cycles

    @property
    def minimal_relative_distance(self) -> float:
        """Returns minimal miss distance"""
        if self.__simulation_state.collision:
            return 0
        else:
            return self.__minimal_relative_distance
    
    @minimal_relative_distance.setter
    def minimal_relative_distance(self, minimal_relative_distance : float) -> None:
        """Sets minimal miss distance"""
        self.__minimal_relative_distance = minimal_relative_distance
        
    @property
    def is_silent(self) -> bool:
        """Returns silent mode flag"""
        return self.__is_silent
    
    @is_silent.setter
    def is_silent(self, is_silent : bool) -> None:
        """Sets silent mode flag"""
        self.__is_silent = is_silent
        
    @property
    def miss_distance_at_closest_approach(self) -> float:
        """Returns miss distance at closest approach"""
        return self.__miss_distance_at_closest_approach
    
    @miss_distance_at_closest_approach.setter
    def miss_distance_at_closest_approach(self, miss_distance_at_closest_approach : float) -> None:
        """Sets miss distance at closest approach"""
        self.__miss_distance_at_closest_approach = miss_distance_at_closest_approach

    @property
    def relative_distance(self) -> float:
        """Returns relative distance between aircrafts"""
        return (self.aircraft_vehicles[0].position - self.aircraft_vehicles[1].position).length()

    def run(self) -> None:
        """Runs ADS-B simulation thread with precise timeout"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            self.cycle()
            self.msleep(max(0, self.simulation_state.adsb_threshold - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()
    
    def cycle(self) -> None:
        """Executes ADS-B simulation cycle"""
        aircraft_vehicle_1 : AircraftVehicle = self.aircraft_vehicles[0]
        aircraft_vehicle_2 : AircraftVehicle = self.aircraft_vehicles[1]

        if not self.simulation_state.is_paused:
            self.count_adsb_cycles()
            self.simulation_state.update_adsb_settings()

            relative_position = aircraft_vehicle_1.position - aircraft_vehicle_2.position
            speed_difference = aircraft_vehicle_1.speed - aircraft_vehicle_2.speed
            time_to_closest_approach = -(QVector3D.dotProduct(relative_position, speed_difference) / QVector3D.dotProduct(speed_difference, speed_difference))
            if not self.is_silent:
                print("Time to closest approach: " + "{:.2f}".format(time_to_closest_approach) + "s")
            
            if relative_position.length() < self.__minimal_relative_distance:
                self.__minimal_relative_distance = relative_position.length()
            if not self.is_silent:
                print("Minimal relative distance: " + "{:.2f}".format(self.__minimal_relative_distance) + "m")
            
            fcc : AircraftFCC | None = None
            for aircraft in self.aircraft_vehicles:
                try:
                    fcc = self.aircraft_fccs[aircraft.aircraft_id]
                except IndexError:
                    logging.error("Aircraft flight control computer %d not found", aircraft.aircraft_id)
                    if not self.is_silent:
                        print(f"Aircraft flight control computer {aircraft.aircraft_id} not found")
                    if len(self.aircraft_fccs) == 2:
                        if aircraft.aircraft_id % 2 == 0:
                            fcc = self.aircraft_fccs[0]
                        else:
                            fcc = self.aircraft_fccs[1]

                # path
                fcc.append_visited()

                # console destination reach time
                if fcc.destination is not None and self.simulation_state.adsb_report:
                    time_to_reaching_destination : float = (QVector3D.dotProduct(fcc.destination - aircraft.position, aircraft.speed) / QVector3D.dotProduct(aircraft.speed, aircraft.speed))
                    if not self.is_silent:
                        print(f"Aircraft {aircraft.aircraft_id} will reach its destination in " + "{:.2f}".format(time_to_reaching_destination) + " (" + "{:.1f}".format(time_to_reaching_destination / 60) + " minutes or " + "{:.1f}".format(time_to_reaching_destination / 3600) + " hours)")
                        print("Collision avoidance: " + str(self.simulation_state.avoid_collisions))

                # console report output
                if self.simulation_state.adsb_report and aircraft.aircraft_id == self.__simulation_state.focused_aircraft_id and self.simulation_state.is_realtime:
                    if not self.is_silent:
                        self.print_adsb_report(aircraft)

                # safe zone occupancy check
                if relative_position.length() < self.simulation_state.minimum_separation:
                    if not fcc.safe_zone_occupied:
                        fcc.safe_zone_occupied = True
                        if not self.simulation_state.override_avoid_collisions:
                            self.simulation_state.avoid_collisions = True
                    if not self.is_silent:
                        print("Safe zone occupied")
                else:
                    if fcc.safe_zone_occupied:
                        fcc.safe_zone_occupied = False
                        self.simulation_state.avoid_collisions = False
                    if not self.is_silent:
                        print("Safe zone free")
                    continue

            if time_to_closest_approach > 0:
                # miss distance at closest approach
                speed_difference_unit = speed_difference.normalized()
                miss_distance_vector : QVector3D = QVector3D.crossProduct(
                    speed_difference_unit,
                    QVector3D.crossProduct(relative_position, speed_difference_unit))
                if not self.is_silent:
                    print("Miss distance at closest approach: " + "{:.2f}".format(miss_distance_vector.length()) + "m (" + "{:.2f}".format(self.aircraft_vehicles[0].size / 2 + self.aircraft_vehicles[1].size / 2) + "m is collision distance)")

                if miss_distance_vector.length() == 0 and self.simulation_state.avoid_collisions:
                    logging.info("Head-on collision detected")
                    if not self.is_silent:
                        print("Head-on collision detected")

                # resolve conflict condition
                unresolved_region : float = self.simulation_state.minimum_separation - abs(miss_distance_vector.length())
                if unresolved_region > 0.0:
                    if not self.is_silent:
                        print("Conflict condition detected")
                    if self.simulation_state.avoid_collisions and relative_position.length() < self.simulation_state.minimum_separation:
                        for aircraft in self.aircraft_fccs:
                            if not aircraft.evade_maneuver:
                                logging.info("Conflict condition resolution with relative distance: " + "{:.2f}".format(relative_position.length()) + "m")
                                self.miss_distance_at_closest_approach = miss_distance_vector.length()
                                aircraft.apply_evade_maneuver(
                                    opponent_speed = self.aircraft_vehicles[1 - aircraft.aircraft_id].speed,
                                    miss_distance_vector = miss_distance_vector,
                                    unresolved_region = unresolved_region,
                                    time_to_closest_approach = time_to_closest_approach)
                    if not self.is_silent:
                        print("Relative distance: "+ "{:.2f}".format(relative_position.length()) + "m")

                # probable collision
                collision_distance = aircraft_vehicle_1.size / 2 + aircraft_vehicle_2.size / 2
                collision_region = collision_distance - miss_distance_vector.length()
                if collision_region > 0 and not self.is_silent:
                        print("Collision detected")
            else:
                for aircraft in self.aircraft_fccs:
                    if aircraft.evade_maneuver and not aircraft.safe_zone_occupied:
                        aircraft.reset_evade_maneuver()

    def print_adsb_report(self, aircraft : AircraftVehicle) -> None:
        """Prints ADS-B report for the aircraft to the console"""
        fcc = self.aircraft_fccs[aircraft.aircraft_id]
        turning_direction = "Not turning"
        if fcc.is_turning_left:
            turning_direction = "Turning left"
        elif fcc.is_turning_right:
            turning_direction = "Turning right"
        print("- Aircraft id: " + str(aircraft.aircraft_id) +
            "; speed: " + "{:.2f}".format(aircraft.absolute_speed) +
            "; turning: " + turning_direction +
            "; roll angle: " + "{:.2f}".format(aircraft.roll_angle) +
            "; target roll angle: " + "{:.2f}".format(fcc.target_roll_angle) +
            "; yaw angle: " + "{:.2f}".format(aircraft.yaw_angle) +
            "; target yaw angle: " + "{:.2f}".format(fcc.target_yaw_angle) +
            "; x: " + "{:.2f}".format(aircraft.position.x()) +
            "; y: " + "{:.2f}".format(aircraft.position.y()) +
            "; z: " + "{:.2f}".format(aircraft.position.z()))
        if fcc.destination is not None:
            if self.simulation_state.is_realtime:
                print("target pitch angle: " + "{:.2f}".format(fcc.target_pitch_angle) +
                    "; pitch angle: " + "{:.2f}".format(aircraft.pitch_angle) +
                    "; dest x: " + "{:.2f}".format(fcc.destination.x()) +
                    "; dest y: " + "{:.2f}".format(fcc.destination.y()) +
                    "; dest z: " + "{:.2f}".format(fcc.destination.z()) +
                    "; distance covered: " + "{:.2f}".format(aircraft.distance_covered) +
                    "; fps: " + "{:.2f}".format(self.simulation_state.fps) +
                    "; t: " + str(self.adsb_cycles) +
                    "; phys: " + str(self.simulation_state.physics_cycles))
            else:
                print("target pitch angle: " + "{:.2f}".format(fcc.target_pitch_angle) +
                    "; pitch angle: " + "{:.2f}".format(aircraft.pitch_angle) +
                    "; dest x: " + "{:.2f}".format(fcc.destination.x()) +
                    "; dest y: " + "{:.2f}".format(fcc.destination.y()) +
                    "; dest z: " + "{:.2f}".format(fcc.destination.z()) +
                    "; distance covered: " + "{:.2f}".format(aircraft.distance_covered) +
                    "; t: " + str(self.adsb_cycles) +
                    "; phys: " + str(self.simulation_state.physics_cycles))
        else:
            if self.simulation_state.is_realtime:
                print("target pitch angle: " + "{:.2f}".format(fcc.target_pitch_angle) +
                    "; pitch angle: " + "{:.2f}".format(aircraft.pitch_angle) +
                    "; distance covered: " + "{:.2f}".format(aircraft.distance_covered) +
                    "; fps: " + "{:.2f}".format(self.simulation_state.fps) +
                    "; t: " + str(self.adsb_cycles) +
                    "; phys: " + str(self.simulation_state.physics_cycles) +
                    "; no destination")
            else:
                print("target pitch angle: " + "{:.2f}".format(fcc.target_pitch_angle) +
                    "; pitch angle: " + "{:.2f}".format(aircraft.pitch_angle) +
                    "; distance covered: " + "{:.2f}".format(aircraft.distance_covered) +
                    "; t: " + str(self.adsb_cycles) +
                    "; phys: " + str(self.simulation_state.physics_cycles) +
                    "; no destination")
        # speed check
        absolute_speed = sqrt(aircraft.speed.x() ** 2 + aircraft.speed.y() ** 2 + aircraft.speed.z() ** 2)
        horizontal_speed = sqrt(aircraft.speed.x() ** 2 + aircraft.speed.y() ** 2)
        vertical_speed = abs(aircraft.speed.z())
        geometrical_speed = sqrt(horizontal_speed ** 2 + vertical_speed ** 2)
        print("absolute speed: " + "{:.2f}".format(absolute_speed) +
            "; horizontal speed: " + "{:.2f}".format(horizontal_speed) +
            "; vertical speed: " + "{:.2f}".format(vertical_speed) +
            "; geometrical speed: " + "{:.2f}".format(geometrical_speed))

    def reset_destinations(self) -> None:
        """Resets destination for all aircrafts"""
        for aircraft in self.aircraft_fccs:
            aircraft.clear_destinations()
            aircraft.load_initial_destination()
