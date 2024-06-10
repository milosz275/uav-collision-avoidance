# Generated data

This directory contains the simulation data files for the UAV collision avoidance system. The data is crucial for running simulations, analyzing performance, and testing different scenarios within the UAV collision avoidance project.

## CSV Data

The simulation data is stored in CSV format. Each row in the CSV file represents a single simulation data point. The columns in the CSV file represent the following information:
- `test_id`: The unique identifier for the test case.
- `aircraft_angle`: The initial angle between the two aircraft in degrees.
- `aircraft_1_init_pos_x`, `aircraft_1_init_pos_y`, `aircraft_1_init_pos_z`: The initial position of the first aircraft.
- `aircraft_2_init_pos_x`, `aircraft_2_init_pos_y`, `aircraft_2_init_pos_z`: The initial position of the second aircraft.
- `aircraft_1_init_speed_x`, `aircraft_1_init_speed_y`, `aircraft_1_init_speed_z`: The initial speed of the first aircraft.
- `aircraft_2_init_speed_x`, `aircraft_2_init_speed_y`, `aircraft_2_init_speed_z`: The initial speed of the second aircraft.
- `aircraft_1_init_target_x`, `aircraft_1_init_target_y`, `aircraft_1_init_target_z`: The target position of the first aircraft.
- `aircraft_2_init_target_x`, `aircraft_2_init_target_y`, `aircraft_2_init_target_z`: The target position of the second aircraft.
- `aircraft_1_final_pos_x_if_no_avoidance`, `aircraft_1_final_pos_y_if_no_avoidance`, `aircraft_1_final_pos_z_if_no_avoidance`: The final position of the first aircraft if no avoidance is applied.
- `aircraft_2_final_pos_x_if_no_avoidance`, `aircraft_2_final_pos_y_if_no_avoidance`, `aircraft_2_final_pos_z_if_no_avoidance`: The final position of the second aircraft if no avoidance is applied.
- `aircraft_1_final_pos_x_if_avoidance`, `aircraft_1_final_pos_y_if_avoidance`, `aircraft_1_final_pos_z_if_avoidance`: The final position of the first aircraft if avoidance is applied.
- `aircraft_2_final_pos_x_if_avoidance`, `aircraft_2_final_pos_y_if_avoidance`, `aircraft_2_final_pos_z_if_avoidance`: The final position of the second aircraft if avoidance is applied.
- `aircraft_1_final_speed_x_if_no_avoidance`, `aircraft_1_final_speed_y_if_no_avoidance`, `aircraft_1_final_speed_z_if_no_avoidance`: The final speed of the first aircraft if no avoidance is applied.
- `aircraft_2_final_speed_x_if_no_avoidance`, `aircraft_2_final_speed_y_if_no_avoidance`, `aircraft_2_final_speed_z_if_no_avoidance`: The final speed of the second aircraft if no avoidance is applied.
- `aircraft_1_final_speed_x_if_avoidance`, `aircraft_1_final_speed_y_if_avoidance`, `aircraft_1_final_speed_z_if_avoidance`: The final speed of the first aircraft if avoidance is applied.
- `aircraft_2_final_speed_x_if_avoidance`, `aircraft_2_final_speed_y_if_avoidance`, `aircraft_2_final_speed_z_if_avoidance`: The final speed of the second aircraft if avoidance is applied.
- `collision_if_no_avoidance`: A boolean value indicating whether a collision would occur if no avoidance is applied.
- `collision_if_avoidance`: A boolean value indicating whether a collision would occur if avoidance is applied.
- `minimal_relative_distance_if_no_avoidance`: The minimal relative distance between the aircraft if no avoidance is applied.
- `minimal_relative_distance_if_avoidance`: The minimal relative distance between the aircraft if avoidance is applied.

## Directory structure

- `simulation.csv`: The latest simulation data file. This file is not created automatically. For having specific simulation data loaded, simply copy wanted simulation data into this file.
- `simulation-*.csv`: Historical simulation data files, named with the timestamp of the simulation run. These files are not tracked by Git as per the `.gitignore` settings, except for specific examples. 

Simulation data consisting of 20 tests conducted with 10 `Hz` simulation frequency [simulation-2024-06-08-15-52-45.csv](/data/simulation-2024-06-08-15-52-45.csv).
Simulation data consisting of 200 tests conducted with 10 `Hz` simulation frequency [simulation-2024-06-10-00-21-19.csv](/data/simulation-2024-06-10-00-21-19.csv).
