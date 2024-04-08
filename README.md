# UAV Collision Avoidance

Python project regarding implementation of UAV physics and collision detection/avoidance algorithms.
- [Current version](https://github.com/mldxo/uav-collision-avoidance)
- [Archived version](https://github.com/mldxo/uav-collision-avoidance-2)
- [Pypi project](https://pypi.org/project/uav-collision-avoidance)

## Introduction

UAV Collision Avoidance is my Bachelor's thesis project meeting problem of UAVs safe cooperation in the 3D space. Project implements functional physics calculations, scalable GUI, realistic ADS-B probable collision avoidance systems and on-board flight planning. Application offers realtime simulation presenting moving aircrafts as well as rendered simulation allowing for algorithm effectiveness testing.

## Premises

3-dimensional (3D) space defined in XYZ coordinate system, where X and Y describe flat horizontal plane and Z is height above the sea level. Physics is simulated differentiating between parts of the second according to adequate formulas. In scope of this project, UAVs' physics are considered relative to the Earth frame and the aeroplanes are considered HTOL drones (Horizontal Take-off and Landing) that can only move in direction of their speed vectors. The space is shared by two or three UAVs. There is no other objects or gusts of wind assumpted. No aerodynamic lift force assumed at this moment. The default distance units are meters [m] and speed is meters per second [m/s], frame times are represented in miliseconds [ms].

## Technologies

Python3[^1] project is wrapped as a PyPi package[^2]. PySide6[^3] (Qt's Python Qt6 library) was used for GUI implementation.

## Algorithms

Both collision detection and avoidance algorithms rely on geometrical approach. They were presented in referenced paper[^4].

## Structures

Application is built based on two main object types, simulation and aircraft. Simulation is created up to initial settings, allowing for concurrent realtime variant and linear prerendering. Aircraft consists of two elements, physical representation of the UAV and Flight Control Computer, which is controlled by the physics thread. Research among the UAV systems was possible thanks to second paper[^5].

## App arguments

There are three possible arguments at the moment:
- realtime - runs GUI application with realtime simulation
- prerender - runs physical simulation
- tests - runs full tests with comparison of using and not using collision avoidance algorithm

App defaults to realtime simulation.

## Usage

Use `pip install uav-collision-avoidance` to install the app and run one of the following:
- uav-collision-avoidance
- uav-collision-avoidance-realtime
- uav-collision-avoidance-prerender
- uav-collision-avoidance-tests

## Build

Build it by cloning the repo and running the following commands:

<p align="left">
    <img width="30px" alt="Bash" style="padding-right:10px;" src="https://skillicons.dev/icons?i=bash" />
</p>

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py [argument]
```

<p align="left">
    <img width="30px" alt="Powershell" style="padding-right:10px;" src="https://skillicons.dev/icons?i=powershell" />
</p>

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py [argument]
```

## Remarks

One coding convention is not preserved in the scope of the project. Qt's methods are CamelCase formatted and the rest is default Python naming convention including snake_case for variable and member names.

## Authors

- [Miłosz Maculewicz](https://github.com/mldxo)

## References

All used references are listed below.

[^1]: [Python3](https://www.python.org/)
[^2]: [PyPi](https://pypi.org/)
[^3]: [PyQt6](https://doc.qt.io/qtforpython-6/)
[^4]: [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013/)
[^5]: [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452/)
