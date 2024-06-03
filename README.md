# UAV Collision Avoidance

[![pl](https://img.shields.io/badge/lang-pl-blue.svg)](https://github.com/mldxo/uav-collision-avoidance/blob/master/README.pl.md)
[![Build](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/python-app.yml/badge.svg)](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/github-code-scanning/codeql)
[![Documentation Status](https://readthedocs.org/projects/uav-collision-avoidance/badge/?version=latest)](https://uav-collision-avoidance.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/uav-collision-avoidance.svg)](https://badge.fury.io/py/uav-collision-avoidance)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mldxo/uav-collision-avoidance)

Python project regarding implementation of two UAVs simulation with collision avoidance system based on geometrical approach.

- [Github](https://github.com/mldxo/uav-collision-avoidance)
- [PyPI](https://pypi.org/project/uav-collision-avoidance)

## Research work

### Introduction

`UAV Collision Avoidance` is my Bachelor's thesis project meeting problem of UAVs safe cooperation in the 3D space. Project implements functional physics calculations, scalable GUI, realistic ADS-B probable collision avoidance systems and on-board flight planning. Application offers multithreaded realtime simulation presenting simulated aircrafts as well as linearly pre-rendered simulation allowing for quick algorithm effectiveness testing.

### Documentation

- [Docs](/docs/en/README.md)
- [Wiki](https://github.com/mldxo/uav-collision-avoidance/wiki)

### Premises

1. System Definition: The system is defined as a 3-dimensional (3D) space using an XYZ coordinate system. X and Y represent a flat horizontal plane, while Z represents height above sea level.
2. Physics Simulation: Physics are simulated by differentiating parts of the second according to appropriate formulas. The physics of Unmanned Aerial Vehicles (UAVs) are considered relative to the Earth's frame, separated from the aircraft's frame and wind relative frame. 3D space is flat, and the Earth's curvature is not considered. Gaining or losing altitude preserves the aircraft's speed. RPY frame is considered.[^6]
3. Aircraft Characteristics: The aircraft are considered Horizontal Take-off and Landing (HTOL) drones. They can only move in the direction of their speed vectors. The form of the aircraft is approximated to a simple solid sphere.
4. Environment: The space is shared by two or three UAVs. There are no other objects or wind gusts assumed in this environment.
5. Aerodynamics: No aerodynamic lift force is assumed at this moment. When turning, aircraft always take the maximum angle change that physics allow, respecting its mass inertia. Maximum pitch and roll angles are considered `-45°, 45°` and `-90°, 90°` respectively, where positive pitch angle means climbing and positive roll angle means banking right. Angles are not approximated for realism preservation.
6. Units of Measurement: The default distance units are meters $\pu{m}$, speed is measured in meters per second $\pu{m/s}$, and frame times are represented in milliseconds $\pu{ms}$.

### Algorithms

Both collision detection and avoidance algorithms rely on geometrical approach. They were presented in referenced paper[^4]. Collision detection differentiates between collision and head-on collision. The second one applies when UAVs have no distance between their projected center of masses collision, and the first one when it is every other type of contact.

### Results

Geometrical approach proves useful in collision detection and avoidance. The system is capable of avoiding collisions in most cases. The system is not perfect and can fail in some scenarios, especially when the aircrafts are too close to each other when conflict is detected. The system is energy-efficient and can be used in real-life scenarios.

Proposed test cases generation and evaluation system is simple and effective. It allows for quick testing of the system's effectiveness in various scenarios. The system can be further developed to include more complex scenarios and additional parameters.

## Python Project

### Technologies

Python3[^1] project is wrapped as a PyPI package[^2]. PySide6[^3] (Qt's Python Qt6 library) was used for GUI implementation.

### Structures

Application is built based on two main object types, simulation and aircraft. Simulation is created up to initial settings, allowing for concurrent realtime variant and linear pre-rendering. Aircraft consists of two elements, physical representation of the UAV and Flight Control Computer, which is controlled by the ADS-B thread. Research among the UAV systems was drawn on from second cited paper[^5].

### App arguments

There are eight possible arguments at the moment:
- default (no arguments) - runs GUI simulation; avoiding collision can be achieved by pressing T, when aircrafts have their safe zones occupied
- realtime `file_path` `test_index` `collision_avoidance` - runs GUI simulation; file name can be specified and defaults to latest simulation data found; test index can be specified and defaults to 0; collision avoidance can be specified and defaults to off
- headless - runs physical simulation with ADS-B and collision avoidance algorithm
- tests `test_number` - runs full tests comparing effectiveness of collision avoidance algorithm, test number defaults to 15
- ongoing - runs default test number in parallel comparing effectiveness of collision avoidance algorithm continuously till Ctrl+C
- load `file_path` `test_index` - loads and conducts headless simulation from file when specified, otherwise loads default example test case from data directory [data](/data); test index can be specified and defaults to 0
- help `argument` - prints help message for the app argument; defaults to all arguments list
- version - prints version of the app

### Key shortcuts

Realtime version of the app has several key shortcuts allowing user interaction with the environment.

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
- F2/F3 keys - speed down/up target speed of Aircraft 0
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

Install the app by running the following command:

```bash
pip install uav-collision-avoidance
```

#### Debian 12 Dependencies

For Debian 12, you need to install the following dependencies:

```bash
sudo apt-get install libgl1 libxcb-xinerama0
```

To run the app headless, you need to run the following export:

```bash
export QT_QPA_PLATFORM=offscreen
```

### Usage

Use any of the following to run the app:

```bash
uav-collision-avoidance
```

```bash
uav-collision-avoidance realtime [file_name] [test_index] [collision_avoidance]
```

```bash
uav-collision-avoidance headless
```

```bash
uav-collision-avoidance tests [test_number]
```

```bash
uav-collision-avoidance ongoing
```

```bash
uav-collision-avoidance load [file_name] [test_index]
```

```bash
uav-collision-avoidance help [argument]
```

```bash
uav-collision-avoidance version
```

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

3-dimensional (3D) world is projected on 2D screen by flattening height (z coordinate). On the program start, the view is not centered on any of the aircrafts. The view can be moved with arrow keys or centered on the aircraft using `N` key.

One coding convention is not preserved in the scope of the project. Qt's methods are CamelCase formatted and the rest is default Python naming convention including snake_case for variable and member names.

## Current Work / TODOs

- [ ] ADS-B: FCC angle optimization
- [ ] Rendering: Aircraft centered view optimization
- [x] Wiki: Documentation

## Authors

[Miłosz Maculewicz](https://github.com/mldxo)

## License
Check [LICENSE](/LICENSE)

## References

<p align="left">
    <img width="30px" alt="Aircraft icon" style="padding-right:10px;" src="/assets/aircraft.png" />
</p>

Drone by Anthony Lui from <a href="https://thenounproject.com/browse/icons/term/drone/" target="_blank" title="Drone Icons">Noun Project</a> (CC BY 3.0)

All used references are listed below.

[^1]: [Python3](https://www.python.org/)
[^2]: [PyPI](https://pypi.org/)
[^3]: [PyQt6](https://doc.qt.io/qtforpython-6/)
[^4]: [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013/)
[^5]: [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452/)
[^6]: [Aircraft principal axes](https://en.wikipedia.org/wiki/Aircraft_principal_axes)
