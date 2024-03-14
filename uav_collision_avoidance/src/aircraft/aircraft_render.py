# aircraft_render.py

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_fcc import AircraftFCC
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.simulation.simulation_state import SimulationState

class AircraftRender(QObject):
    """Aircraft graphical representation"""

    def __init__(self, aircraft_id : int, vehicle : AircraftVehicle, fcc : AircraftFCC, state : SimulationState) -> None:
        super().__init__()
        self.aircraft_id = aircraft_id
        self.vehicle = vehicle
        self.state = state
        self.fcc = fcc

        # fields updated with AircraftVehicle and AircraftFCC
        self.position : QVector3D = QVector3D(0, 0, 0)
        self.size : float = 0.0
        self.yaw_angle : float = 0.0
        self.pitch_angle : float = 0.0
        self.roll_angle : float = 0.0
        self.safezone_occupied : bool = False
        return
    
    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        """Remotely moves aircraft vehicle"""
        self.vehicle.move(dx, dy, dz)
        return

    def update(self) -> None:
        """Updates graphical location of the render based on vehicle position"""
        self.position.setX(self.vehicle.position().x() * self.state.gui_scale)
        self.position.setY(self.vehicle.position().y() * self.state.gui_scale)
        self.position.setZ(self.vehicle.position().z() * self.state.gui_scale)
        self.size = self.vehicle.size() * self.state.gui_scale
        self.yaw_angle = self.vehicle.yaw_angle()
        self.pitch_angle = self.vehicle.pitch_angle()
        self.roll_angle = self.vehicle.roll_angle()
        self.safezone_occupied = self.fcc.safezone_occupied()
        return
