# UAV Collision Avoidance

Python project regarding implementation of UAV physics and collision detection/avoidance algorithms.
- [Github repo](https://github.com/mldxo/uav-collision-avoidance)
- [PyPi project](https://pypi.org/project/uav-collision-avoidance)

## Research work

### Introduction

UAV Collision Avoidance is my Bachelor's thesis project meeting problem of UAVs safe cooperation in the 3D space. Project implements functional physics calculations, scalable GUI, realistic ADS-B probable collision avoidance systems and on-board flight planning. Application offers realtime simulation presenting moving aircrafts as well as rendered simulation allowing for algorithm effectiveness testing.

### Premises

3-dimensional (3D) space defined in XYZ coordinate system, where X and Y describe flat horizontal plane and Z is height above the sea level. Physics is simulated differentiating between parts of the second according to adequate formulas. In scope of this project, UAVs' physics are considered relative to the Earth frame and the aeroplanes are considered HTOL drones (Horizontal Take-off and Landing) that can only move in direction of their speed vectors. Aircrafts' form are approaximated to simple solid sphere. The space is shared by two or three UAVs. There is no other objects or gusts of wind assumpted. No aerodynamic lift force assumed at this moment. The default distance units are meters [m] and speed is meters per second [m/s], frame times are represented in miliseconds [ms].

### Algorithms

Both collision detection and avoidance algorithms rely on geometrical approach. They were presented in referenced paper[^4]. Collision detection differentiates between collision and head-on collision. The second one applies when UAVs have no distance between their projected center of masses collision, and the first one when it is every other type of contact.

## Python Project

### Technologies

Python3[^1] project is wrapped as a PyPi package[^2]. PySide6[^3] (Qt's Python Qt6 library) was used for GUI implementation.

### Structures

Application is built based on two main object types, simulation and aircraft. Simulation is created up to initial settings, allowing for concurrent realtime variant and linear prerendering. Aircraft consists of two elements, physical representation of the UAV and Flight Control Computer, which is controlled by the physics thread. Research among the UAV systems was possible thanks to second paper[^5].

### App arguments

There are three possible arguments at the moment:
- realtime - runs GUI application with realtime simulation
- prerender - runs physical simulation
- tests - runs full tests with comparison of using and not using collision avoidance algorithm

App defaults to realtime simulation.

### Key shortcuts

> [!NOTE]
> Aircraft 0 is the first one, Aircraft 1 is the second one.

There are several key shortcuts for realtime version of the app that allow full-scale testing.

- Left mouse click - appends click location to the top of destination list of Aircraft 0
- Right mouse click - adds click location to the end of destination list of Aircraft 0
- Middle mouse click (scroll click) - teleports Aircraft 0 to the click location
- Mouse wheel - zooms in/out the simulation render smoothly
- Plus/minus keys (+/-) - zooms in/out the simulation render quickly
- Arrow keys (↑ ↓ → ←) - moves the view
- F1 key - toggles ADS-B Aircraft 0 info reporting
- F2/F3 keys - speed up/down target speed of Aircraft 0
- N key - toggles Aircraft 0/1 view following (default off)
- M key - switches between Aircraft 0/1 view following (default 0)
- O key - toggles Aircraft 0 targeting Aircraft 1's speed vector (default off)
- P key - toggles Aircraft 1 targeting Aircraft 0's speed vector (default off)
- T key - toggles collision avoidance maneuvering (default off)
- WSAD keys - sets course for Aircraft 0 - 0, 180, 270, 90 degrees respectively
- R - resets simulation to start state
- Slash key (/) - pauses physics simulation
- Escape key (Esc) - closes and ends simulation

### Install

Use `pip install uav-collision-avoidance` to install the app and run one of the following:
- uav-collision-avoidance
- uav-collision-avoidance realtime
- uav-collision-avoidance prerender
- uav-collision-avoidance tests

### Build

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

### Remarks

One coding convention is not preserved in the scope of the project. Qt's methods are CamelCase formatted and the rest is default Python naming convention including snake_case for variable and member names.

## Current Work / TODOs

- [ ] Reimplement safe zone
- [ ] Symmetrical bank (roll) during turn, no angle approaximation
- [ ] Altitude change with symmetrical command
- [ ] Generating test cases
- [ ] Test cases comparison
- [ ] Documentation
- [ ] Centered view optimization

## Authors

- [Miłosz Maculewicz](https://github.com/mldxo)

## References

All used references are listed below.

[^1]: [Python3](https://www.python.org/)
[^2]: [PyPi](https://pypi.org/)
[^3]: [PyQt6](https://doc.qt.io/qtforpython-6/)
[^4]: [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013/)
[^5]: [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452/)
