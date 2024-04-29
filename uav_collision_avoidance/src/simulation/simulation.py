"""Simulation module"""

import csv
import logging
import datetime
from copy import copy
from typing import List
from pathlib import Path

from PySide6.QtCore import QThread, QTime
from PySide6.QtGui import QCloseEvent, QVector3D
from PySide6.QtWidgets import QMainWindow

from ..aircraft.aircraft import Aircraft
from ..aircraft.aircraft_fcc import AircraftFCC
from ..simulation.simulation_settings import SimulationSettings
from ..simulation.simulation_physics import SimulationPhysics
from ..simulation.simulation_state import SimulationState
from ..simulation.simulation_render import SimulationRender
from ..simulation.simulation_widget import SimulationWidget
from ..simulation.simulation_adsb import SimulationADSB
from ..simulation.simulation_fps import SimulationFPS
from ..simulation.simulation_data import SimulationData

class Simulation(QMainWindow):
    """Main simulation App"""

    def __init__(self, headless : bool = False, tests : bool = False, simulation_time : int = 10_000_000) -> None: # 10_000_000 ms = 10_000 s = 2h 46m 40s
        super().__init__()
        SimulationSettings().__init__()
        self.__headless : bool = headless
        self.__tests : bool = tests
        self.__simulation_time : int = simulation_time
        self.__aircrafts : List[Aircraft] | None = None
        self.__state : SimulationState | None = None
        self.run()

    @property
    def headless(self) -> bool:
        """Returns headless flag"""
        return self.__headless
    
    @property
    def tests(self) -> bool:
        """Returns tests flag"""
        return self.__tests
    
    @property
    def simulation_time(self) -> int:
        """Returns simulation time"""
        return self.__simulation_time
    
    @property
    def aircrafts(self) -> List[Aircraft]:
        """Returns aircrafts list"""
        return self.__aircrafts
    
    @property
    def state(self) -> SimulationState:
        """Returns simulation state"""
        return self.__state
    
    @state.setter
    def state(self, state : SimulationState) -> None:
        """Sets simulation state"""
        self.__state = state
    
    def run(self) -> None:
        """Executes simulation"""
        if self.state is not None:
            print("Another instance already running")
            return
        if self.headless:
            if self.tests:
                self.run_tests()
            else:
                self.run_headless()
        else:
            self.run_gui()

    def run_gui(self) -> None:
        """Executes realtime simulation"""
        if self.aircrafts is None or self.aircrafts == []:
            self.setup_debug_aircrafts()
        logging.info("Starting realtime simulation")
        self.state = SimulationState(SimulationSettings(), is_realtime = True)
        self.simulation_physics = SimulationPhysics(self, self.aircrafts, self.state)
        self.simulation_adsb = SimulationADSB(self, self.aircrafts, self.state)
        self.simulation_fps = SimulationFPS(self, self.state)
        self.simulation_widget = SimulationWidget(self.aircrafts, self.simulation_fps, self.state)
        self.simulation_render = SimulationRender(self, self.simulation_widget, self.state)
        self.simulation_physics.start(priority = QThread.Priority.TimeCriticalPriority)
        self.simulation_adsb.start(priority = QThread.Priority.NormalPriority)
        self.simulation_fps.start(priority = QThread.Priority.NormalPriority)
        self.simulation_widget.show()
        self.simulation_render.start(priority = QThread.Priority.NormalPriority)
        self.simulation_widget.stop_signal.connect(self.stop)
    
    def run_headless(self, avoid_collisions : bool = False, aircrafts : List[Aircraft] | None = None) -> None:
        """Executes simulation without GUI"""
        logging.info("Starting headless simulation")
        if aircrafts is None or aircrafts == []:
            self.setup_debug_aircrafts()
        else:
            self.setup_aircrafts(aircrafts)
        simulation_data : SimulationData = SimulationData()
        simulation_data.aircraft_1_initial_position = copy(self.aircrafts[0].vehicle.position)
        simulation_data.aircraft_2_initial_position = copy(self.aircrafts[1].vehicle.position)
        simulation_data.aircraft_1_initial_roll_angle = copy(self.aircrafts[0].vehicle.roll_angle)
        simulation_data.aircraft_2_initial_roll_angle = copy(self.aircrafts[1].vehicle.roll_angle)
        simulation_data.collision = False

        self.state = SimulationState(SimulationSettings(), is_realtime = False, avoid_collisions = avoid_collisions)
        self.simulation_physics = SimulationPhysics(self, self.aircrafts, self.state)
        self.simulation_adsb = SimulationADSB(self, self.aircrafts, self.state)
        time_step : int = int(self.state.simulation_threshold)
        adsb_step : int = int(self.state.adsb_threshold)
        partial_time_counter : int = adsb_step
        for time in range(0, int(self.simulation_time / self.state.simulation_threshold), time_step):
            self.simulation_physics.cycle(time_step)
            if partial_time_counter >= adsb_step:
                self.simulation_adsb.cycle()
                partial_time_counter = 0
            partial_time_counter += time_step
            if self.state.collision:
                simulation_data.collision = True
                break
        simulation_data.minimal_miss_distance = copy(self.simulation_adsb.minimal_miss_distance)
        simulation_data.aircraft_1_final_position = copy(self.aircrafts[0].vehicle.position)
        simulation_data.aircraft_2_final_position = copy(self.aircrafts[1].vehicle.position)
        self.stop()
        return simulation_data
    
    def run_tests(self, test_number : int = 10) -> None:
        """Runs simulation tests"""
        if test_number < 1:
            test_number = 10
        logging.info("Running simulation tests")
        start_timestamp = QTime.currentTime()
        #list_of_aircrafts : List[List[Aircraft]] = self.generate_test_aircrafts(test_number) # todo
        export_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        try:
            Path("logs/data").mkdir(parents=True, exist_ok=True)
        except:
            return
        file = open(f"logs/data/simulation-{export_time}.csv", "w")
        writer = csv.writer(file)
        writer.writerow([
            "test_id",
            "aircraft_1_init_pos_x",
            "aircraft_1_init_pos_y",
            "aircraft_1_init_pos_z",
            "aircraft_2_init_pos_x",
            "aircraft_2_init_pos_y",
            "aircraft_2_init_pos_z",
            "aircraft_1_final_pos_x_if_no_avoidance",
            "aircraft_1_final_pos_y_if_no_avoidance",
            "aircraft_1_final_pos_z_if_no_avoidance",
            "aircraft_2_final_pos_x_if_no_avoidance",
            "aircraft_2_final_pos_y_if_no_avoidance",
            "aircraft_2_final_pos_z_if_no_avoidance",
            "aircraft_1_final_pos_x_if_avoidance",
            "aircraft_1_final_pos_y_if_avoidance",
            "aircraft_1_final_pos_z_if_avoidance",
            "aircraft_2_final_pos_x_if_avoidance",
            "aircraft_2_final_pos_y_if_avoidance",
            "aircraft_2_final_pos_z_if_avoidance",
            "collision_if_no_avoidance",
            "collision_if_avoidance",
            "minimal_miss_distance_if_no_avoidance",
            "minimal_miss_distance_if_avoidance"])
        for i in range(0, test_number, 1):
            logging.info("Test %d - no collision avoidance", i)
            # self.run_headless(avoid_collisions = True, aircrafts = list_of_aircrafts[i])
            simulation_data_no_avoidance : SimulationData = self.run_headless()
            self.state = None

            logging.info("Test %d - collision avoidance", i)
            # self.run_headless(avoid_collisions = True, aircrafts = list_of_aircrafts[i])
            simulation_data_avoidance : SimulationData = self.run_headless(avoid_collisions = True)
            self.state = None

            writer.writerow([
                i,
                simulation_data_no_avoidance.aircraft_1_initial_position.x(),
                simulation_data_no_avoidance.aircraft_1_initial_position.y(),
                simulation_data_no_avoidance.aircraft_1_initial_position.z(),
                simulation_data_no_avoidance.aircraft_2_initial_position.x(),
                simulation_data_no_avoidance.aircraft_2_initial_position.y(),
                simulation_data_no_avoidance.aircraft_2_initial_position.z(),
                simulation_data_no_avoidance.aircraft_1_final_position.x(),
                simulation_data_no_avoidance.aircraft_1_final_position.y(),
                simulation_data_no_avoidance.aircraft_1_final_position.z(),
                simulation_data_no_avoidance.aircraft_2_final_position.x(),
                simulation_data_no_avoidance.aircraft_2_final_position.y(),
                simulation_data_no_avoidance.aircraft_2_final_position.z(),
                simulation_data_avoidance.aircraft_1_final_position.x(),
                simulation_data_avoidance.aircraft_1_final_position.y(),
                simulation_data_avoidance.aircraft_1_final_position.z(),
                simulation_data_avoidance.aircraft_2_final_position.x(),
                simulation_data_avoidance.aircraft_2_final_position.y(),
                simulation_data_avoidance.aircraft_2_final_position.z(),
                simulation_data_no_avoidance.collision,
                simulation_data_avoidance.collision,
                simulation_data_no_avoidance.minimal_miss_distance,
                simulation_data_avoidance.minimal_miss_distance])
        file.close()
        real_time : float = start_timestamp.msecsTo(QTime.currentTime()) / 1000
        print("Total time elapsed: " + "{:.2f}".format(real_time) + "s")
        logging.info("Total time elapsed: %ss", "{:.2f}".format(real_time))
    
    def stop(self) -> None:
        """Stops simulation"""
        if self.headless:
            self.stop_headless_simulation()
        else:
            self.stop_realtime_simulation()
        self.state.reset()
        self.state.is_running = False

    def stop_realtime_simulation(self) -> None:
        """Finishes all active realtime simulation threads"""
        if not self.state.is_running:
            return
        logging.info("Stopping realtime simulation")
        self.simulation_physics.requestInterruption()
        self.simulation_adsb.requestInterruption()
        self.simulation_render.requestInterruption()
        self.simulation_fps.requestInterruption()
        self.simulation_physics.quit()
        self.simulation_physics.wait()

        if self.state.is_paused:
            self.state.append_paused_time()
        simulated_time : float = self.state.physics_cycles / (1000 / self.state.simulation_threshold)
        real_time_pauses : float = self.simulation_physics.global_start_timestamp.msecsTo(self.simulation_physics.global_stop_timestamp) / 1000
        real_time : float = real_time_pauses - (self.state.time_paused / 1000)
        print("Time simulated: " + "{:.2f}".format(simulated_time) + "s")
        if real_time == real_time_pauses:
            print("Time elapsed: " + "{:.2f}".format(real_time) + "s")
        else:
            print("Time elapsed: " + "{:.2f}".format(real_time) + "s (" + "{:.2f}".format(real_time_pauses) + "s with pauses)")
        if real_time != 0:
            print("Time efficiency: " + "{:.2f}".format(simulated_time / real_time * 100) + "%")
            logging.info("Calculated time efficiency: " + "{:.2f}".format(simulated_time / real_time * 100) + "%")

        self.export_visited_locations()
        self.simulation_adsb.quit()
        self.simulation_adsb.wait()
        self.simulation_render.quit()
        self.simulation_render.wait()
        self.simulation_fps.quit()
        self.simulation_fps.wait()
    
    def stop_headless_simulation(self) -> None:
        """Finishes headless simulation"""
        if not self.state.is_running:
            print("No simulation running")
            return
        logging.info("Stopping headless simulation")
        self.simulation_physics.reset_aircrafts()
        self.state.reset()

    def add_aircraft(self, aircraft : Aircraft) -> None:
        """Adds aircraft to simulation"""
        if self.aircrafts is None:
            self.__aircrafts = []
        self.aircrafts.append(aircraft)

    def remove_aircraft(self, aircraft : Aircraft) -> None:
        """Removes aircraft from simulation"""
        if self.aircrafts is not None:
            self.aircrafts.remove(aircraft)

    def setup_aircrafts(self, aircrafts : List[Aircraft]) -> None:
        """Sets up aircrafts list"""
        self.__aircrafts = aircrafts

    def setup_debug_aircrafts(self) -> None:
        """Sets up debug aircrafts list"""
        test_case : int = 3
        if test_case == 0:
            aircrafts : List[Aircraft] = [
                Aircraft( # detection test
                    position = QVector3D(-800, 4000, 1000),
                    speed = QVector3D(60, -60, 0),
                    initial_target = QVector3D(51_900, -50_000, 10000)),
                Aircraft(
                    position = QVector3D(4000, 6000, 1000),
                    speed = QVector3D(0, -85, 0),
                    initial_target = QVector3D(900, -1_001_300, 1000)),
            ]
        elif test_case == 1:
            aircrafts : List[Aircraft] = [
                Aircraft( # almost head on
                    position = QVector3D(-3000, 500, 1000),
                    speed = QVector3D(70, 0.1, 0)),
                Aircraft(
                    position = QVector3D(5000, 500, 1000),
                    speed = QVector3D(-50, 0, 0)),
            ]
        elif test_case == 2:
            aircrafts : List[Aircraft] = [
                Aircraft( # avoidance test slow
                    position = QVector3D(0, 0, 1000),
                    speed = QVector3D(30, -30, 0),
                    initial_target = QVector3D(75000, -75000, 1000)), # 75 km, -75 km
                Aircraft(
                    position = QVector3D(0, -100_000, 1000),
                    speed = QVector3D(30, 29, 0),
                    initial_target = QVector3D(75000, -27500, 1000)), # 75 km, -27.5 km
            ]
        elif test_case == 3:
            aircrafts : List[Aircraft] = [
                Aircraft( # avoidance test
                    position = QVector3D(0, 0, 1000),
                    speed = QVector3D(150, -150, 0),
                    initial_target = QVector3D(75000, -75000, 1000)), # 75 km, -75 km
                Aircraft(
                    position = QVector3D(0, -100_000, 1000),
                    speed = QVector3D(150, 145, 0),
                    initial_target = QVector3D(75000, -27500, 1000)), # 75 km, -27.5 km
            ]
        elif test_case == 4:
            aircrafts : List[Aircraft] = [
                Aircraft( # avoidance test fast
                    position = QVector3D(0, 0, 1000),
                    speed = QVector3D(300, -300, 0),
                    initial_target = QVector3D(75000, -75000, 1000)), # 75 km, -75 km
                Aircraft(
                    position = QVector3D(0, -100_000, 1000),
                    speed = QVector3D(300, 290, 0),
                    initial_target = QVector3D(75000, -27500, 1000)), # 75 km, -27.5 km
            ]
        self.setup_aircrafts(aircrafts)

    def export_visited_locations(self) -> None:
        """Exports aircrafts visited location lists"""
        export_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        aircraft_fccs : List[AircraftFCC] = [aircraft.fcc for aircraft in self.aircrafts]
        for aircraft in aircraft_fccs:
            try:
                Path("logs/visited").mkdir(parents=True, exist_ok=True)
            except:
                return
            file = open(f"logs/visited/visited-aircraft-{aircraft.aircraft_id}-{export_time}.csv", "w")
            writer = csv.writer(file)
            writer.writerow(["x","y","z"])
            for position in aircraft.visited:
                writer.writerow([("{:.2f}".format(position.x())),("{:.2f}".format(position.y())),("{:.2f}".format(position.z()))])
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        self.stop()
        event.accept()
        return super().closeEvent(event)
