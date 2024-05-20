# Documentation

## Overview

This documentation provides a detailed overview of the classes defined in the UAV Collision Avoidance project. Each class is described with its purpose, attributes, and methods.

The classes are organized into the following categories:
- `main`: Entry point of the application.
- `simulation`: Classes responsible for conducting simulations.
- `aircraft`: Classes representing UAVs.

All classes make use of Python's properties and setters utilizing mutexes and mutex locks to ensure encapsulation and data integrity.

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

#### Methods:
- `__init__(simulation_settings : SimulationSettings, is_realtime : bool, avoid_collisions : bool) -> None`: Initializes a new simulation state instance.
- `toggle_avoid_collisions() -> None`: Toggles the collision avoidance flag.
- `toggle_pause() -> None`: Toggles the pause flag.
- `reset() -> None`: Sets the reset demanded flag true.
- `apply_reset() -> None`: Sets the reset demanded flag false.
- `append_time_paused() -> None`: Appends the time paused to the total time paused.
- `toggle_adsb_report() -> None`: Toggles the ADS-B report flag.
- `register_collision() -> None`: Registers a collision.
- `toggle_first_cause_collision() -> None`: Toggles the first cause collision flag.
- `toggle_second_cause_collision() -> None`: Toggles the second cause collision flag.
- `toggle_draw_fps() -> None`: Toggles the FPS drawing flag.
- `toggle_draw_aircraft() -> None`: Toggles the aircraft drawing flag.
- `toggle_draw_grid() -> None`: Toggles the grid drawing flag.
- `toggle_draw_path() -> None`: Toggles the paths drawing flag.
- `toggle_draw_speed_vectors() -> None`: Toggles the speed vectors drawing flag.
- `toggle_draw_safe_zones() -> None`: Toggles the safe zones drawing flag.
- `toggle_draw_collision_detection() -> None`: Toggles the collision detection drawing flag.
- `toggle_optimize_drawing() -> None`: Toggles the drawing optimization flag.
- `toggle_follow_aircraft() -> None`: Toggles the follow aircraft flag.
- `toggle_focus_aircraft() -> None`: Toggles the focus aircraft flag.
- `update_settings() -> None`: Updates all state settings.
- `update_render_settings() -> None`: Updates simulation render state settings
- `update_simulation_settings() -> None`: Updates simulation physics state settings
- `update_adsb_settings() -> None`: Updates simulation ADS-B state settings

---

## File: `src/simulation/simulation_settings.py`

### Class: `SimulationSettings`

**Description**: 
A static class that stores constants used in the program and the initial simulation data.

#### Static members:
- `screen_resolution`: Screen resolution (QSize).
- `resolution`: Resolution of the simulation (float).
- `g_acceleration`: Gravitational acceleration (float = 9.81).
- `simulation_frequency`: Frequency of the simulation (float = 100.0).
- `simulation_threshold`: Threshold of the simulation (float = 1000 / 100.0).
- `gui_render_frequency`: Frequency of the GUI render (float = 100.0).
- `gui_render_threshold`: Threshold of the GUI render (float = 1000 / 100.0).
- `adsb_threshold` : Threshold of the ADS-B system (float = 1000.0).

#### Methods:
- `__init__()` : Initializes a new simulation settings instance.

---

## File: `src/simulation/simulation_widget.py`

### Class: `SimulationWidget`

**Description**: 
Enables the creation of a user interface - an interactive window that visualizes the simulation process, allowing the tracking of a selected vehicle and modification of its flight plan.

#### Properties:
- `aircrafts`: List of simulated aircrafts.
- `aircraft_vehicles`: List of simulated aircraft vehicles.
- `aircraft_fccs`: List of simulated aircraft FCCs.
- `simulation_fps`: FPS tracking object.
- `simulation_state`: State of the simulation.
- `window_width`: Width of the simulation window.
- `window_height`: Height of the simulation window.
- `screen_offset_x`: Offset of the screen in the x-axis.
- `screen_offset_y`: Offset of the screen in the y-axis.
- `icon`: Icon of the simulation.
- `moving_view_up`: Flag representing if the view is moving up.
- `moving_view_down`: Flag representing if the view is moving down.
- `moving_view_left`: Flag representing if the view is moving left.
- `moving_view_right`: Flag representing if the view is moving right.
- `steering_up`: Flag representing if the steering is up.
- `steering_down`: Flag representing if the steering is down.
- `steering_left`: Flag representing if the steering is left.
- `steering_right`: Flag representing if the steering is right.

#### Methods:
- `__init__(aircrafts : List[Aircraft], simulation_state : SimulationState) -> None`: Initializes a new simulation widget instance.
- `generate_icon() -> None`: Generates the icon of the simulation.
- `draw_aircraft(aircraft : AircraftVehicle, scale : float) -> None`: Draws the aircraft on the simulation window.
- `draw_destinations(aircraft : AircraftVehicle, scale : float) -> None`: Draws the destinations of the aircraft on the simulation window.
- `draw_text(point : QVector3D, scale : float, text : str, color : QColor) -> None`: Draws the text on the simulation window.
- `draw_circle(point : QVector3D, size : float, scale : float, color : QColor) -> None`: Draws the circle on the simulation window.
- `draw_disk(point : QVector3D, size : float, scale : float, color : QColor) -> None`: Draws the disk (full circle) on the simulation window.
- `draw_line(start : QVector3D, end : QVector3D, scale : float, color : QColor) -> None`: Draws the line on the simulation window.
- `draw_vector(start : QVector3D, vector : QVector3D, scale : float, color : QColor) -> None`: Draws the vector on the simulation window.
- `draw_collision_detection(scale : float) -> None`: Draws the collision detection on the simulation window.
- `draw_grid(scale : float, x_offset : float, y_offset : float) -> None`: Draws the grid on the simulation window.
- `update_moving_offsets() -> None`: Updates the moving offsets of the simulation window.
- `update_steering() -> None`: Updates the steering of the simulation window.
- `center_offsets() -> None`: Centers the offsets of the simulation window.
- `update_resolutions() -> None`: Updates the resolution of the simulation window.
- `zoom(factor : float) -> None`: Zooms the simulation window.
- `paintEvent(event : QPaintEvent) -> None`: Paints the simulation window.
- `mousePressEvent(event : QMouseEvent) -> None`: Handles mouse press events.
- `mouseReleaseEvent(event : QMouseEvent) -> None`: Handles mouse release events.
- `mouseDoubleClickEvent(event : QMouseEvent) -> None`: Handles mouse double click events.
- `wheelEvent(event : QWheelEvent) -> None`: Handles mouse wheel events.
- `keyPressEvent(event : QKeyEvent) -> None`: Handles key press events.
- `keyReleaseEvent(event : QKeyEvent) -> None`: Handles key release events.
- `resizeEvent(event : QResizeEvent) -> None`: Handles resize events.
- `closeEvent(event : QCloseEvent) -> None`: Handles close events.

---

## File: `src/simulation/simulation_render.py`

### Class: `SimulationRender`

**Description**: 
Enables the creation of a thread responsible for refreshing the simulation window in the `SimulationWidget`.

> [!WARNING]
> Documentation below is still in progress.

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

## References

All used references are listed below.

- [Python3](https://www.python.org/)
- [PyPi](https://pypi.org/)
- [PyQt6](https://doc.qt.io/qtforpython-6/)
- [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013/)
- [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452/)
- [Aircraft principal axes](https://en.wikipedia.org/wiki/Aircraft_principal_axes)
