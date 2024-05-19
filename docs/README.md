# UAV Collision Avoidance Documentation

## Overview

This documentation provides a detailed overview of the classes defined in the UAV Collision Avoidance project. Each class is described with its purpose, attributes, and methods.

---

## File: `main.py`

### Function: `main()`

**Description**: 
Entry point of the application. Acts as outer runner for the app.

---

## File: `src/main.py`

### Function: `main()`

**Description**: 
Proper entry point of the application. Begins QtApplication. Parses arguments and starts the appropriate simulation mode.

#### Methods:
- `run_simulation_tests(test_number : int)`: Handles concurrent test running.

---

## File: `src/version.py`

### Function: `get_version()`

**Description**: 
Parses current app version from `pyproject.toml` file.

---

## File: `src/simulation/simulation.py`

### Class: `Simulation`

**Description**: 
The primary class responsible for conducting simulations. It can operate in two basic modes:
- **realtime**: Creates a user interface and conducts a simulation that mimics real-time conditions.
- **headless**: Conducts a simulation without real-time imitation.

The `Simulation` class is responsible for generating test cases, conducting series of tests, creating and exporting data sets, as well as plotting the paths of UAVs. Derived Simulation- classes are created within the object of this class using composition.

#### Properties:
- `simulation_id`: Identifier of the simulation.
- `hash`: Unique hash string for the simulation.
- `headless`: Flag representing if the simulation does not contain user interface.
- `tests`: Flag representing if the simulation will run tests.
- `simulation_time`: Time that should be simulated [s].
- `aircrafts`: List of simulated aircrafts.
- `state`: State of the simulation.
- `imported_from_data`: Flag representing if the simulation was loaded from file.
- `simulation_data`: Contains simulation data structure if loaded from file.

#### Methods:
- `__init__(headless : bool, tests : bool, simulation_time : int) -> None`: Initializes a new simulation instance without initializing state and aircrafts.
- `obtain_simulation_id() -> int`: Obtains identifier for the simulation.
- `obtain_simulation_hash() -> str`: Obtains unique hash for the simulation.
- `run() -> None`: Starts appropriate type of simulation.
- `run_gui(avoid_collisions : bool, load_latest_data_file : bool) -> None`: Explicitly runs simulation with graphical user interface (GUI).
- `run_headless(avoid_collisions : bool, aircrafts : List[Aircraft], test_index : int, aircraft_angle : float) -> SimulationData`: Explicitly runs simulation headless. Returns simulation data structure for performing checks.
- `generate_test_aircrafts() -> List[Tuple[List[Aircraft], float]]`: Generates random list of lists of Aircrafts (paired with start angle between them) ready to be iterated through and used in test simulation.
- `generate_consistent_list_of_aircraft_lists() -> List[Tuple[List[Aircraft], float]]`: Returns predefined set of aircrafts
- `run_tests(begin_with_default_set : bool, test_number : int)`: Runs headless simulation sequentially using test cases generation. Exports simulation data.
- `load_latest_simulation_data_file() -> bool`: Tries to load the latest found data file (can be overridden with using simulation.csv file name). Returns true if successful.
- `load_simulation_data_from_file(file_path : str, test_id : int, avoid_collisions : bool) -> bool`: Tries to load data file of the given name. Returns true if successful.
- `stop()`: Stops running simulation by trying to use appropriate stop method.
- `stop_realtime_simulation() -> None`: Stops simulation that was running real-time (with GUI).
- `stop_headless_simulation() -> None`: Stops simulation that was running headless (no GUI).
- `add_aircraft(aircraft : Aircraft) -> None`: Appends given aircraft to initialized aircraft list.
- `remove_aircraft(aircraft : Aircraft) -> None`: Tries to remove given aircraft from aircraft list.
- `setup_aircrafts(self, aircrafts : List[Aircraft]) -> None`: Initializes new aircraft list using given aircraft list.
- `setup_debug_aircrafts(self, test_case : int) -> None`: Overrides aircraft list with predefined aircraft set.
- `import_simulation_data(data : SimulationData) -> None`: Attempts to load simulation data from given data structure.
- `check_simulation_data_correctness() -> bool`: Runs check of current simulation state with loaded, expected simulation data. Returns true if correct.
- `export_visited_locations(simulation_data : SimulationData, test_index : int)`: Exports locations marked as visited from aircrafts' FCCs. Attempts to create visual representations of aircraft paths.

---

## File: `src/simulation/simulation_physics.py`

### Class: `SimulationPhysics`

**Description**: 
Enables the creation of a thread responsible for simulating physics, tracking vehicle locations, and performing operations on them over time. It imitates physical laws affecting physical bodies through the use of differentiation.

#### Properties:
- `aircrafts`: List of simulated aircrafts.
- `aircraft_vehicles`: List of simulated aircraft vehicles.
- `aircraft_fccs`: List of simulated aircraft FCCs.
- `simulation_state`: State of the simulation.
- `cycles`: Number of counted cycles.

#### Methods:

- `__init__(aircrafts : List[Aircraft], simulation_state : SimulationState) -> None`: Initializes a new physics simulation instance.
- `count_cycles() -> None`: Increments the number of counted cycles and updates simulation state.
- `run() -> None`: Starts the physics simulation.
- `mark_start_time() -> None`: Marks the start time of the simulation.
- `mark_stop_time() -> None`: Marks the end time of the simulation.
- `cycle(elapsed_time : float) -> None`: Performs a single cycle of the simulation.
- `reset_aircrafts() -> None`: Resets the positions of all aircrafts.
- `update_aircrafts_positions() -> bool`: Updates the positions of all aircrafts. Returns true if any of the aircrafts have collided.
- `update_aircrafts_speed_angles() -> None`: Updates the speed and angle of all aircrafts.
- `test_speed() -> None`: Tests the correctness of the speed of all aircrafts.

---

## File: `src/simulation/simulation_adsb.py`

### Class: `SimulationADSB`

**Description**: 
Enables the creation of a thread responsible for simulating the ADS-B (Automatic Dependent Surveillance-Broadcast) system. Manages the onboard computers (FCC) of UAVs to send collision avoidance data when necessary.

#### Properties:
- `aircrafts`: List of simulated aircrafts.
- `aircraft_vehicles`: List of simulated aircraft vehicles.
- `aircraft_fccs`: List of simulated aircraft FCCs.
- `simulation_state`: State of the simulation.
- `adsb_cycles`: Number of counted ADS-B system cycles.
- `minimal_relative_distance`: Minimal known relative distance between two aircrafts.

#### Methods:
- `__init__(aircrafts : List[Aircraft], simulation_state : SimulationState) -> None`: Initializes a new ADS-B simulation instance.
- `count_adsb_cycles() -> None`: Increments the number of counted ADS-B system cycles.
- `run() -> None`: Starts the ADS-B simulation.
- `cycle() -> None`: Performs a single cycle of the ADS-B simulation.
- `print_adsb_report() -> None`: Prints the ADS-B data of all aircrafts.
- `reset_destinations() -> None`: Resets the destinations of all aircrafts to initial state.

---

## File: `src/simulation/simulation_state.py`

### Class: `SimulationState`

**Description**: 
Stores the current state of the simulation - variables accessible to all components of the program. It supports both realtime and headless simulations.

#### Properties:
- `simulation_settings`: Simulation settings.
- `is_realtime`: Flag representing if the simulation is running in real-time.
- `avoid_collisions`: Flag representing if the simulation should avoid collisions.
- `override_avoid_collisions`: Flag representing if the collision avoidance should be overridden.
- `minimum_separation`: Minimum separation between aircrafts.
- `physics_cycles`: Number of counted physics cycles.
- `is_paused`: Flag representing if the simulation is paused.
- `is_running`: Flag representing if the simulation is running.
- `reset_demanded`: Flag representing if the simulation should be reset.
- `pause_start_timestamp`: Time when the simulation was paused.
- `time_paused`: Time the simulation was paused.
- `adsb_report`: Flag representing if the ADS-B report should be printed.
- `collision`: Flag representing if a collision has occurred.
- `first_cause_collision`: Flag representing if the first aircraft caused a collision.
- `second_cause_collision`: Flag representing if the second aircraft caused a collision.
- `fps`: Number of frames per second (if GUI is initialized).

> [!WARNING]
> Documentation below is still in progress.

#### Methods:
- `__init__(simulation_settings : SimulationSettings, is_realtime : bool, avoid_collisions : bool) -> None`: Initializes a new simulation state instance.

---

## File: `src/simulation/simulation_settings.py`

### Class: `SimulationSettings`

**Description**: 
A static class that stores constants used in the program and the initial simulation data.

---

## File: `src/simulation/simulation_widget.py`

### Class: `SimulationWidget`

**Description**: 
Enables the creation of a user interface - an interactive window that visualizes the simulation process, allowing the tracking of a selected vehicle and modification of its flight plan.

---

## File: `src/simulation/simulation_render.py`

### Class: `SimulationRender`

**Description**: 
Enables the creation of a thread responsible for refreshing the simulation window in the `SimulationWidget`.

---

## File: `src/simulation/simulation_fps.py`

### Class: `SimulationFPS`

**Description**: 
Provides an interface for counting and displaying the number of frames generated per second during a realtime simulation.

---

## File: `src/simulation/simulation_data.py`

### Class: `SimulationData`

**Description**: 
Allows tracking of data related to the simulation, which is necessary for loading and generating tests.

---

## File: `src/aircraft/aircraft.py`

### Class: `Aircraft`

**Description**: 
Represents a simulated UAV. It creates its components using composition - objects of the `AircraftFCC` and `AircraftVehicle` classes.

---

## File: `src/aircraft/aircraft_fcc.py`

### Class: `AircraftFCC`

**Description**: 
Represents the onboard computer of a UAV. Tracks its planned route and sets the appropriate flight parameters.

---

## File: `src/aircraft/aircraft_vehicle.py`

### Class: `AircraftVehicle`

**Description**: 
Represents the UAV as a physical object. Stores information about its position in space and speed, as well as the size of the UAV and its inertia.

---

## Contribution Guidelines

Before contributing, please check [CONTRIBUTING.md](https://github.com/mldxo/uav-collision-avoidance/blob/main/CONTRIBUTING.md).

Contributions to the project are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

For more information, visit the [GitHub repository](https://github.com/mldxo/uav-collision-avoidance).
