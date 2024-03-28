# UAV Collision Avoidance

Python project regarding implementation of UAV physics and collision detection/avoidance algorithms.
[Archived version](https://github.com/mldxo/uav-collision-avoidance-2)

## Introduction

UAV Collision Avoidance is my bachelor's thesis project meeting problem of UAVs safe cooperation in the 3D space. Project implements functional physics calculations, scalable GUI, realistic ADS-B probable collision avoidance systems and on-board flight planning.

## Premises

3-dimensional space defined in XYZ coordinate system, where X and Y describe flat horizontal plane and Z is height above the sea level. In scope of this project, UAVs are considered HTOL drones (Horizontal Take-off and Landing). The space is shared by two/three UAVs. There is no other objects or gusts of wind assumpted. The default distance unit is meters [m] and speed is meters per second [m/s]. No aerodynamic lift force assumed at this moment. Aircrafts are considered only to move in direction of their speed vectors. No drifting implemented.

## Technologies

Python3[^1] project is wrapped as a PyPi package[^2]. PySide6[^3], which is PyQt6 library, was used for GUI implementation.

## Structures

## Algorithms

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

[![Bash](https://skillicons.dev/icons?i=bash)](https://skillicons.dev)

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd uav-collision-avoidance
python main.py [argument]
```

[![Powershell](https://skillicons.dev/icons?i=powershell)](https://skillicons.dev)

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd uav-collision-avoidance
python main.py [argument]
```

## Remarks

One coding convention is not preserved in the scope of the project. Qt's methods are CamelCase formatted and the rest is snake_case, default Python naming convention.

## Authors

- [Miłosz Maculewicz](https://github.com/mldxo)

## References

- [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452)
- [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013)

[^1]: [Python3](https://www.python.org/)
[^2]: [PyPi](https://pypi.org/)
[^3]: [PyQt6](https://doc.qt.io/qtforpython-6/)
