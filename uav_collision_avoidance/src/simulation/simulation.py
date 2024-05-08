"""Simulation module"""

import csv
import logging
import datetime
from copy import copy
from typing import List
from pathlib import Path
from numpy import random, ndarray
from math import dist, sin, cos, radians

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

    def __init__(self, headless : bool = False, tests : bool = False, simulation_time : int = 100_000_000) -> None: # 100_000_000 ms = 100_000 s = 27.78 h
        super().__init__()
        SimulationSettings().__init__()
        self.__headless : bool = headless
        self.__tests : bool = tests
        self.__simulation_time : int = simulation_time
        self.__aircrafts : List[Aircraft] | None = None
        self.__state : SimulationState | None = None
        self.__imported_from_data : bool = False
        self.__simulation_data : SimulationData | None = None

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

    @property
    def imported_from_data(self) -> bool:
        """Returns imported from data flag"""
        return self.__imported_from_data
    
    @imported_from_data.setter
    def imported_from_data(self, imported : bool) -> None:
        """Sets imported from data flag"""
        self.__imported_from_data = imported

    @property
    def simulation_data(self) -> SimulationData:
        """Returns simulation data"""
        return self.__simulation_data
    
    @simulation_data.setter
    def simulation_data(self, data : SimulationData) -> None:
        """Sets simulation data"""
        self.__simulation_data = data
    
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

    def run_gui(self, avoid_collisions : bool = False, load_lastest_data_file : bool = True) -> None:
        """Executes realtime simulation"""
        if load_lastest_data_file:
            self.load_latest_simulation_data_file()
        if self.aircrafts is None or self.aircrafts == []:
            self.setup_debug_aircrafts()
        logging.info("Starting realtime simulation")
        self.state = SimulationState(SimulationSettings(), is_realtime = True, avoid_collisions = avoid_collisions)
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
    
    def run_headless(self, avoid_collisions : bool = False, aircrafts : List[Aircraft] | None = None) -> SimulationData:
        """Executes simulation without GUI"""
        logging.info("Starting headless simulation")
        if aircrafts is not None:
            self.setup_aircrafts(aircrafts)
        elif self.aircrafts is None or self.aircrafts == []:
            self.setup_debug_aircrafts()
        else:
            assert len(self.aircrafts) > 0
        simulation_data : SimulationData = SimulationData()
        simulation_data.aircraft_1_initial_position = copy(self.aircrafts[0].vehicle.position)
        simulation_data.aircraft_2_initial_position = copy(self.aircrafts[1].vehicle.position)
        simulation_data.aircraft_1_initial_speed = copy(self.aircrafts[0].vehicle.speed)
        simulation_data.aircraft_2_initial_speed = copy(self.aircrafts[1].vehicle.speed)
        simulation_data.aircraft_1_initial_target = copy(self.aircrafts[0].fcc.destination)
        simulation_data.aircraft_2_initial_target = copy(self.aircrafts[1].fcc.destination)
        simulation_data.aircraft_1_initial_roll_angle = copy(self.aircrafts[0].vehicle.roll_angle)
        simulation_data.aircraft_2_initial_roll_angle = copy(self.aircrafts[1].vehicle.roll_angle)
        simulation_data.collision = False

        self.state = SimulationState(SimulationSettings(), is_realtime = False, avoid_collisions = avoid_collisions)
        self.simulation_physics = SimulationPhysics(self, self.aircrafts, self.state)
        self.simulation_adsb = SimulationADSB(self, self.aircrafts, self.state)
        self.simulation_adsb.reset_destinations()
        time_step : int = int(self.state.simulation_threshold)
        adsb_step : int = int(self.state.adsb_threshold)
        partial_time_counter : int = adsb_step
        for time in range(0, int(self.simulation_time / self.state.simulation_threshold), time_step):
            self.simulation_physics.cycle(time_step)
            if partial_time_counter >= adsb_step:
                self.simulation_adsb.cycle()
                partial_time_counter = 0
            partial_time_counter += time_step
            if not self.aircrafts[0].fcc.destination and not self.aircrafts[1].fcc.destination:
                logging.info("Headless simulation stopping due to no other destinations set")
                break
            if self.state.collision:
                logging.info("Headless simulation stopping due to collision detected")
                simulation_data.collision = True
                break
        simulation_data.minimal_relative_distance = copy(self.simulation_adsb.minimal_relative_distance)
        simulation_data.aircraft_1_final_position = copy(self.aircrafts[0].vehicle.position)
        simulation_data.aircraft_2_final_position = copy(self.aircrafts[1].vehicle.position)
        simulation_data.aircraft_1_final_speed = copy(self.aircrafts[0].vehicle.speed)
        simulation_data.aircraft_2_final_speed = copy(self.aircrafts[1].vehicle.speed)
        if self.imported_from_data:
            self.check_simulation_data_correctness()
        self.export_visited_locations()
        self.stop()
        return simulation_data
    
    def generate_test_aircrafts(self) -> List[List[Aircraft]]:
        """Generates test cases"""
        logging.info("Generating test cases")
        list_of_lists : List[List[Aircraft]] = []
        test_average_aircraft_size : int = 20

        # head-on testing
        list_of_lists.append([ # chase test
            Aircraft(
                aircraft_id = 0,
                position = QVector3D(0, -20000, 1000),
                speed = QVector3D(0, 100, 0),
                initial_target = QVector3D(0, 0, 1000)),
            Aircraft(
                aircraft_id = 1,
                position = QVector3D(0, -10000, 1000),
                speed = QVector3D(0, 50, 0),
                initial_target = QVector3D(0, 0, 1000))
        ])
        list_of_lists.append([ # full angle collision, equal speeds
            Aircraft(
                aircraft_id = 0,
                position = QVector3D(0, -5000, 1000),
                speed = QVector3D(0, 50, 0),
                initial_target = QVector3D(0, 0, 1000)),
            Aircraft(
                aircraft_id = 1,
                position = QVector3D(0, 5000, 1000),
                speed = QVector3D(0, -50, 0),
                initial_target = QVector3D(0, 0, 1000))
        ])
        list_of_lists.append([ # full angle collision
            Aircraft(
                aircraft_id = 0,
                position = QVector3D(0, -5000, 1000),
                speed = QVector3D(0, 50, 0),
                initial_target = QVector3D(0, 0, 1000)),
            Aircraft(
                aircraft_id = 1,
                position = QVector3D(0, 10000, 1000),
                speed = QVector3D(0, -100, 0),
                initial_target = QVector3D(0, 0, 1000))
        ])

        # collision testing
        list_of_lists.append([ # chase test
            Aircraft(
                aircraft_id = 0,
                position = QVector3D(0, -20000, 1000),
                speed = QVector3D(0, 100, 0),
                initial_target = QVector3D(test_average_aircraft_size / 4.0, test_average_aircraft_size / 4.0, 1000)),
            Aircraft(
                aircraft_id = 1,
                position = QVector3D(0, -10000, 1000),
                speed = QVector3D(0, 50, 0),
                initial_target = QVector3D(-test_average_aircraft_size / 4.0, -test_average_aircraft_size / 4.0, 1000))
        ])
        list_of_lists.append([ # full angle collision, equal speeds
            Aircraft(
                aircraft_id = 0,
                position = QVector3D(0, -5000, 1000),
                speed = QVector3D(0, 50, 0),
                initial_target = QVector3D(test_average_aircraft_size / 4.0, test_average_aircraft_size / 4.0, 1000)),
            Aircraft(
                aircraft_id = 1,
                position = QVector3D(0, 5000, 1000),
                speed = QVector3D(0, -50, 0),
                initial_target = QVector3D(-test_average_aircraft_size / 4.0, -test_average_aircraft_size / 4.0, 1000))
        ])
        list_of_lists.append([ # full angle collision
            Aircraft(
                aircraft_id = 0,
                position = QVector3D(0, -5000, 1000),
                speed = QVector3D(0, 50, 0),
                initial_target = QVector3D(test_average_aircraft_size / 4.0, test_average_aircraft_size / 4.0, 1000)),
            Aircraft(
                aircraft_id = 1,
                position = QVector3D(0, 10000, 1000),
                speed = QVector3D(0, -100, 0),
                initial_target = QVector3D(-test_average_aircraft_size / 4.0, -test_average_aircraft_size / 4.0, 1000))
        ])

        test_minimal_altitude : int = 1000
        test_maximal_altitude : int = 7000
        test_minimal_speed : int = 30
        test_maximal_speed : int = 100
        test_start_aircrafts_relative_distance : int = 10_000 # distance between aircrafts headed to test collision target
        test_minimal_course_difference : float = 1.0
        test_maximal_course_difference : float = 179.0
        # test_minimal_target_pitch_angle : int = -30
        # test_maximal_target_pitch_angle : int = 30
        test_minimal_trigonometric_value : float = 0.00001
        test_course_difference_count : int = 50
        test_random_collision_course_differences : List[float] = random.uniform(test_minimal_course_difference, test_maximal_course_difference, test_course_difference_count).tolist()
        test_random_collision_course_differences.sort(reverse = False)

        # equal speeds and heights
        for angle in test_random_collision_course_differences:
            aircraft_height : float = random.uniform(test_minimal_altitude, test_maximal_altitude)
            test_collision_target : QVector3D = QVector3D(0, 0, aircraft_height)
            aircraft_absolute_speed : float = random.uniform(test_minimal_speed, test_maximal_speed)
            sin_value : float = sin(radians(angle))
            cos_value : float = cos(radians(angle))
            if abs(sin_value) < test_minimal_trigonometric_value:
                continue
            if abs(cos_value) < test_minimal_trigonometric_value:
                continue
            distance_to_collision : float = test_start_aircrafts_relative_distance / sin_value

            aircraft_1_position : QVector3D = QVector3D(0, -distance_to_collision, aircraft_height)
            aircraft_1_speed : QVector3D = QVector3D(0, aircraft_absolute_speed, 0)
            assert abs(aircraft_1_position.distanceToPoint(test_collision_target) - distance_to_collision) < 0.1
            assert abs(aircraft_1_speed.length() - aircraft_absolute_speed) < 0.1
            
            # rotate angle to get circle equation
            sin_value = sin(radians(90 - angle))
            cos_value = cos(radians(90 - angle))
            aircraft_2_position : QVector3D = QVector3D(
                distance_to_collision * cos_value,
                -distance_to_collision * sin_value,
                aircraft_1_position.z())
            aircraft_2_speed : QVector3D = QVector3D(
                -aircraft_absolute_speed * cos_value,
                aircraft_absolute_speed * sin_value,
                aircraft_1_speed.z())

            assert abs(aircraft_2_position.distanceToPoint(test_collision_target) - distance_to_collision) < 0.05
            assert abs(aircraft_2_speed.length() - aircraft_absolute_speed) < 0.001

            aircrafts : List[Aircraft] = [
                Aircraft(
                    aircraft_id = 0,
                    position = aircraft_1_position,
                    speed = aircraft_1_speed,
                    initial_target = test_collision_target),
                Aircraft(
                    aircraft_id = 1,
                    position = aircraft_2_position,
                    speed = aircraft_2_speed,
                    initial_target = test_collision_target)
            ]
            list_of_lists.append(aircrafts)

        # todo: generate more random parameters for test cases

        if len(list_of_lists) == 0:
            for i in range (0, 30, 1):
                list_of_aircrafts : List[Aircraft] = []
                aircraft : Aircraft = Aircraft( # detection test
                    aircraft_id = 0,
                    position = QVector3D(-800, 4000, 1000),
                    speed = QVector3D(60, -60, 0),
                    initial_target = QVector3D(51_900, -50_000, 10000)) # 51.9 km, -50 km
                list_of_aircrafts.append(aircraft)
                aircraft = Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(4000, 6000, 1000),
                    speed = QVector3D(0, -85, 0),
                    initial_target = QVector3D(900, -1_001_300, 1000)) # 0.9 km, -1001.3 km
                list_of_aircrafts.append(aircraft)
                list_of_lists.append(list_of_aircrafts)

        return list_of_lists
    
    def run_tests(self, test_number : int = 10) -> None:
        """Runs simulation tests"""
        if test_number < 3:
            logging.info("Changing simulation tests to 3 test cases due to too low test number")
            test_number = 3
        elif test_number > 100:
            logging.info("Changing simulation tests to 100 test cases due to too high test number")
            test_number = 100
        logging.info("Running simulation tests")
        list_of_lists : List[List[Aircraft]] = self.generate_test_aircrafts()
        lists_count : int = len(list_of_lists)

        if lists_count > test_number:
            random_indices : ndarray = random.choice(lists_count, test_number, replace = False)
            random_indices : List[int] = random_indices.tolist()
            random_indices_set : set = set(random_indices)
            random_indices = []
            while random_indices_set:
                random_indices.append(random_indices_set.pop())
            random_indices.sort(reverse = False)
            assert len(random_indices) <= test_number
            print("Selected indices: ", random_indices)
            print("Indices count: ", len(random_indices))
            list_of_lists = [list_of_lists[i] for i in random_indices]
            lists_count = len(list_of_lists)

        print("Generated and selected aircrafts pairs: ", lists_count)
        test_number = lists_count

        start_timestamp = QTime.currentTime()
        export_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        try:
            Path("data").mkdir(parents=True, exist_ok=True)
        except:
            logging.error("Failed to create data directory")
            return
        file = None
        filename_iterator : int = 1
        if Path(f"data/simulation-{export_time}.csv").exists():
            while Path(f"data/simulation-{export_time}-{filename_iterator}.csv").exists():
                filename_iterator += 1
            file = open(f"data/simulation-{export_time}-{filename_iterator}.csv", "w")
        else:
            file = open(f"data/simulation-{export_time}.csv", "w")
        writer = csv.writer(file)
        writer.writerow([
            "test_id",
            "aircraft_1_init_pos_x",
            "aircraft_1_init_pos_y",
            "aircraft_1_init_pos_z",
            "aircraft_2_init_pos_x",
            "aircraft_2_init_pos_y",
            "aircraft_2_init_pos_z",
            "aircraft_1_init_speed_x",
            "aircraft_1_init_speed_y",
            "aircraft_1_init_speed_z",
            "aircraft_2_init_speed_x",
            "aircraft_2_init_speed_y",
            "aircraft_2_init_speed_z",
            "aircraft_1_init_target_x",
            "aircraft_1_init_target_y",
            "aircraft_1_init_target_z",
            "aircraft_2_init_target_x",
            "aircraft_2_init_target_y",
            "aircraft_2_init_target_z",
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
            "aircraft_1_final_speed_x_if_no_avoidance",
            "aircraft_1_final_speed_y_if_no_avoidance",
            "aircraft_1_final_speed_z_if_no_avoidance",
            "aircraft_2_final_speed_x_if_no_avoidance",
            "aircraft_2_final_speed_y_if_no_avoidance",
            "aircraft_2_final_speed_z_if_no_avoidance",
            "aircraft_1_final_speed_x_if_avoidance",
            "aircraft_1_final_speed_y_if_avoidance",
            "aircraft_1_final_speed_z_if_avoidance",
            "aircraft_2_final_speed_x_if_avoidance",
            "aircraft_2_final_speed_y_if_avoidance",
            "aircraft_2_final_speed_z_if_avoidance",
            "collision_if_no_avoidance",
            "collision_if_avoidance",
            "minimal_relative_distance_if_no_avoidance",
            "minimal_relative_distance_if_avoidance"])
        file.close()
        file = open(f"data/simulation-{export_time}.csv", "a")
        writer = csv.writer(file)
        
        for i in range(0, test_number, 1):
            logging.info("Test %d - no collision avoidance", i)
            aircrafts : List[Aircraft] = list_of_lists[i]
            print("Current test pair aircrafts count: ", len(aircrafts))
            simulation_data_no_avoidance : SimulationData = self.run_headless(
                avoid_collisions = False,
                aircrafts = aircrafts)
            self.state = None

            logging.info("Test %d - collision avoidance", i)
            simulation_data_avoidance : SimulationData = self.run_headless(
                avoid_collisions = True,
                aircrafts = aircrafts)
            self.state = None

            writer.writerow([
                i,
                simulation_data_no_avoidance.aircraft_1_initial_position.x(),
                simulation_data_no_avoidance.aircraft_1_initial_position.y(),
                simulation_data_no_avoidance.aircraft_1_initial_position.z(),
                simulation_data_no_avoidance.aircraft_2_initial_position.x(),
                simulation_data_no_avoidance.aircraft_2_initial_position.y(),
                simulation_data_no_avoidance.aircraft_2_initial_position.z(),
                simulation_data_no_avoidance.aircraft_1_initial_speed.x(),
                simulation_data_no_avoidance.aircraft_1_initial_speed.y(),
                simulation_data_no_avoidance.aircraft_1_initial_speed.z(),
                simulation_data_no_avoidance.aircraft_2_initial_speed.x(),
                simulation_data_no_avoidance.aircraft_2_initial_speed.y(),
                simulation_data_no_avoidance.aircraft_2_initial_speed.z(),
                simulation_data_no_avoidance.aircraft_1_initial_target.x(),
                simulation_data_no_avoidance.aircraft_1_initial_target.y(),
                simulation_data_no_avoidance.aircraft_1_initial_target.z(),
                simulation_data_no_avoidance.aircraft_2_initial_target.x(),
                simulation_data_no_avoidance.aircraft_2_initial_target.y(),
                simulation_data_no_avoidance.aircraft_2_initial_target.z(),
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
                simulation_data_no_avoidance.aircraft_1_final_speed.x(),
                simulation_data_no_avoidance.aircraft_1_final_speed.y(),
                simulation_data_no_avoidance.aircraft_1_final_speed.z(),
                simulation_data_no_avoidance.aircraft_2_final_speed.x(),
                simulation_data_no_avoidance.aircraft_2_final_speed.y(),
                simulation_data_no_avoidance.aircraft_2_final_speed.z(),
                simulation_data_avoidance.aircraft_1_final_speed.x(),
                simulation_data_avoidance.aircraft_1_final_speed.y(),
                simulation_data_avoidance.aircraft_1_final_speed.z(),
                simulation_data_avoidance.aircraft_2_final_speed.x(),
                simulation_data_avoidance.aircraft_2_final_speed.y(),
                simulation_data_avoidance.aircraft_2_final_speed.z(),
                simulation_data_no_avoidance.collision,
                simulation_data_avoidance.collision,
                simulation_data_no_avoidance.minimal_relative_distance,
                simulation_data_avoidance.minimal_relative_distance])
            file.close()
            file = open(f"data/simulation-{export_time}.csv", "a")
            writer = csv.writer(file)
        file.close()
        real_time : float = start_timestamp.msecsTo(QTime.currentTime()) / 1000
        print("Total time elapsed: " + "{:.2f}".format(real_time) + "s")
        logging.info("Total time elapsed: %ss", "{:.2f}".format(real_time))

    def load_latest_simulation_data_file(self) -> bool:
        """Loads latest simulation data from file"""
        logging.info("Loading latest simulation data")
        found_good_file : bool = False
        latest_file_path : str | None = None
        list_of_paths : List[Path] | None = None
        list_length : int | None = None
        try:
            latest_file_path = max(Path("data").iterdir(), key = lambda p: p.stat().st_ctime)
            list_of_paths = list(Path("data").iterdir())
            list_of_paths.sort(key = lambda x: x.stat().st_ctime, reverse = False)
            list_length = len(list_of_paths)
        except:
            logging.error("Failed to load latest simulation data")
            return False
        iterator : int = 1
        while not found_good_file:
            try:
                file = open(latest_file_path, "r")
                reader = csv.reader(file)
                lines_count : int = 0
                for line in reader:
                    lines_count += 1
                if lines_count > 1:
                    found_good_file = True
                    break
            except:
                pass
            latest_file_path = list_of_paths[list_length - 1 - iterator]
            iterator += 1
        if found_good_file:
            return self.load_simulation_data_from_file(latest_file_path)
        else:
            return False

    def load_simulation_data_from_file(self, file_path : str, test_id : int = 0, avoid_collisions : bool = False) -> bool:
        """Loads simulation data from file"""
        logging.info("Loading simulation data from file %s", file_path)
        self.__aircrafts = []
        try:
            file = open(file_path, "r")
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == test_id + 1:
                    simulation_data : SimulationData = SimulationData()
                    assert len(row) == 47
                    assert row[0] == str(test_id)
                    simulation_data.aircraft_1_initial_position = QVector3D(float(row[1]), float(row[2]), float(row[3]))
                    simulation_data.aircraft_2_initial_position = QVector3D(float(row[4]), float(row[5]), float(row[6]))
                    simulation_data.aircraft_1_initial_speed = QVector3D(float(row[7]), float(row[8]), float(row[9]))
                    simulation_data.aircraft_2_initial_speed = QVector3D(float(row[10]), float(row[11]), float(row[12]))
                    simulation_data.aircraft_1_initial_target = QVector3D(float(row[13]), float(row[14]), float(row[15]))
                    simulation_data.aircraft_2_initial_target = QVector3D(float(row[16]), float(row[17]), float(row[18]))
                    if not avoid_collisions:
                        simulation_data.aircraft_1_final_position = QVector3D(float(row[19]), float(row[20]), float(row[21]))
                        simulation_data.aircraft_2_final_position = QVector3D(float(row[22]), float(row[23]), float(row[24]))
                        simulation_data.aircraft_1_final_speed = QVector3D(float(row[31]), float(row[32]), float(row[33]))
                        simulation_data.aircraft_2_final_speed = QVector3D(float(row[34]), float(row[35]), float(row[36]))
                        simulation_data.collision = row[43] == "True"
                        simulation_data.minimal_relative_distance = float(row[45])
                    else:
                        simulation_data.aircraft_1_final_position = QVector3D(float(row[25]), float(row[26]), float(row[27]))
                        simulation_data.aircraft_2_final_position = QVector3D(float(row[28]), float(row[29]), float(row[30]))
                        simulation_data.aircraft_1_final_speed = QVector3D(float(row[37]), float(row[38]), float(row[39]))
                        simulation_data.aircraft_2_final_speed = QVector3D(float(row[40]), float(row[41]), float(row[42]))
                        simulation_data.collision = row[44] == "True"
                        simulation_data.minimal_relative_distance = float(row[46])
                    self.import_simulation_data(simulation_data)
                    return True
        except:
            logging.error("Failed to load simulation data from file")
            return False
    
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

    def setup_debug_aircrafts(self, test_case : int = 0) -> None:
        """Sets up debug aircrafts list"""
        if test_case == 0:
            aircrafts : List[Aircraft] = [
                Aircraft( # detection test
                    aircraft_id = 0,
                    position = QVector3D(-800, 4000, 1000),
                    speed = QVector3D(60, -60, 0),
                    initial_target = QVector3D(51_900, -50_000, 10000)),
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(4000, 6000, 1000),
                    speed = QVector3D(0, -85, 0),
                    initial_target = QVector3D(900, -1_001_300, 1000)),
            ]
        elif test_case == 1:
            aircrafts : List[Aircraft] = [
                Aircraft( # almost head on
                    aircraft_id = 0,
                    position = QVector3D(-3000, 500, 1000),
                    speed = QVector3D(70, 0.1, 0)),
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(5000, 500, 1000),
                    speed = QVector3D(-50, 0, 0)),
            ]
        elif test_case == 2:
            aircrafts : List[Aircraft] = [
                Aircraft( # avoidance test slow
                    aircraft_id = 0,
                    position = QVector3D(0, 0, 1000),
                    speed = QVector3D(30, -30, 0),
                    initial_target = QVector3D(75000, -75000, 1000)), # 75 km, -75 km
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(0, -100_000, 1000),
                    speed = QVector3D(30, 29, 0),
                    initial_target = QVector3D(75000, -27500, 1000)), # 75 km, -27.5 km
            ]
        elif test_case == 3:
            aircrafts : List[Aircraft] = [
                Aircraft( # avoidance test
                    aircraft_id = 0,
                    position = QVector3D(0, 0, 1000),
                    speed = QVector3D(150, -150, 0),
                    initial_target = QVector3D(75000, -75000, 1000)), # 75 km, -75 km
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(0, -100_000, 1000),
                    speed = QVector3D(150, 145, 0),
                    initial_target = QVector3D(75000, -27500, 1000)), # 75 km, -27.5 km
            ]
        elif test_case == 4:
            aircrafts : List[Aircraft] = [
                Aircraft( # avoidance test fast
                    aircraft_id = 0,
                    position = QVector3D(0, 0, 1000),
                    speed = QVector3D(300, -300, 0),
                    initial_target = QVector3D(75000, -75000, 1000)), # 75 km, -75 km
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(0, -100_000, 1000),
                    speed = QVector3D(300, 290, 0),
                    initial_target = QVector3D(75000, -27500, 1000)), # 75 km, -27.5 km
            ]
        elif test_case == 5:
            aircrafts : List[Aircraft] = [
                Aircraft( # chase test
                    aircraft_id = 0,
                    position = QVector3D(0, -1000, 1000),
                    speed = QVector3D(0, 50, 0),
                    initial_target = QVector3D(0, 0, 1000)), # 0 km, 0 km
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(0, -2000, 1000),
                    speed = QVector3D(0, 100, 0),
                    initial_target = QVector3D(0, 0, 1000)), # 0 km, 0 km
            ]
        elif test_case == 6:
            aircrafts : List[Aircraft] = [
                Aircraft( # full angle collision
                    aircraft_id = 0,
                    position = QVector3D(0, -1000, 1000),
                    speed = QVector3D(0, 50, 0),
                    initial_target = QVector3D(0, 0, 1000)), # 0 km, 0 km
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(0, 1000, 1000),
                    speed = QVector3D(0, -50, 0),
                    initial_target = QVector3D(0, 0, 1000)), # 0 km, 0 km
            ]
        elif test_case == 7:
            aircrafts : List[Aircraft] = [
                Aircraft(
                    aircraft_id = 0,
                    position = QVector3D(0, -5000, 1000),
                    speed = QVector3D(0, 50, 0),
                    initial_target = QVector3D(0, 0, 1000)),
                Aircraft(
                    aircraft_id = 1,
                    position = QVector3D(0, 5000, 1000),
                    speed = QVector3D(0, -50, 0),
                    initial_target = QVector3D(0, 0, 1000))
            ]
        else:
            aircrafts : List[Aircraft] = []
        self.setup_aircrafts(aircrafts)

    def import_simulation_data(self, data : SimulationData) -> None:
        """Imports simulation data"""
        if self.aircrafts is not None and self.aircrafts != []:
            print("Aircrafts already set, cannot import simulation data")
            return
        self.__imported_from_data = True
        self.__simulation_data = data
        self.__aircrafts = [
            Aircraft(
                aircraft_id = 0,
                position = data.aircraft_1_initial_position,
                speed = data.aircraft_1_initial_speed,
                initial_target = data.aircraft_1_initial_target,
                initial_roll_angle = data.aircraft_1_initial_roll_angle),
            Aircraft(
                aircraft_id = 1,
                position = data.aircraft_2_initial_position,
                speed = data.aircraft_2_initial_speed,
                initial_target = data.aircraft_2_initial_target,
                initial_roll_angle = data.aircraft_2_initial_roll_angle),
        ]
        logging.info("Simulation data imported successfully")

    def check_simulation_data_correctness(self) -> bool | None:
        if not self.__imported_from_data or self.__simulation_data is None or self.aircrafts is None or self.aircrafts == []:
            return None
        logging.info("Checking simulation data correctness...")
        assert len(self.aircrafts) == 2
        assert dist(self.aircrafts[0].vehicle.position.toTuple(), self.__simulation_data.aircraft_1_final_position.toTuple()) < 0.1
        assert dist(self.aircrafts[1].vehicle.position.toTuple(), self.__simulation_data.aircraft_2_final_position.toTuple()) < 0.1
        assert dist(self.aircrafts[0].vehicle.speed.toTuple(), self.__simulation_data.aircraft_1_final_speed.toTuple()) < 0.1
        assert dist(self.aircrafts[1].vehicle.speed.toTuple(), self.__simulation_data.aircraft_2_final_speed.toTuple()) < 0.1
        assert abs(self.aircrafts[0].vehicle.speed.length() - self.__simulation_data.aircraft_1_final_speed.length()) < 0.1
        assert abs(self.aircrafts[1].vehicle.speed.length() - self.__simulation_data.aircraft_2_final_speed.length()) < 0.1
        assert abs(self.simulation_adsb.minimal_relative_distance - self.__simulation_data.minimal_relative_distance) < 0.1
        logging.info("Simulation data correctness checked successfully ✅")
        return True

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
