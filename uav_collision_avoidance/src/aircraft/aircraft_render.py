# aircraft_render.py

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QVector3D

from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_fcc import AircraftFCC
from src.simulation.simulation_state import SimulationState

class AircraftRender(QObject):
    """Aircraft graphical representation"""

    position_changed = Signal(float, float, float)

    def __init__(self, aircraft_id : int, vehicle : AircraftVehicle, fcc : AircraftFCC, state : SimulationState) -> None:
        super().__init__()
        self.aircraft_id = aircraft_id
        self.state = state
        self.fcc = fcc

        # fields updated with AircraftVehicle and AircraftFCC
        self.position : QVector3D = QVector3D(0, 0, 0)
        self.size : float = 0.0
        self.yaw_angle : float = 0.0
        self.pitch_angle : float = 0.0
        self.roll_angle : float = 0.0
        self.safezone_occupied : bool = False

        if vehicle:
            self.vehicle = vehicle
            self.vehicle.position_changed.connect(self.update)
        return
    
    def move(self, dx : float, dy : float, dz : float = 0.0) -> None:
        """Remote method for moving vehicle"""
        self.vehicle.move(dx, dy, dz)
        return

    def set_vehicle(self, vehicle) -> None:
        """Sets the physical aircraft for rendered aircraft"""
        if not self.vehicle:
            self.vehicle = vehicle
            self.vehicle.position_changed.connect(self.update)
        return
    
    def disconnect_vehicle(self) -> None:
        """Disconnects active vehicle from renderer"""
        if self.vehicle:
            self.vehicle.position_changed.disconnect(self.update)
        return

    def update(self) -> None:
        """Updates graphical location of the render based on vehicle position"""
        self.position.setX(self.vehicle.position.x() * self.state.scale)
        self.position.setY(self.vehicle.position.y() * self.state.scale)
        self.position.setZ(self.vehicle.position.z() * self.state.scale)
        self.position_changed.emit(self.position.x(), self.position.y(), self.position.z())
        self.size = self.vehicle.size * self.state.scale
        self.yaw_angle = self.vehicle.yaw_angle()
        self.pitch_angle = self.vehicle.pitch_angle()
        self.roll_angle = self.vehicle.roll_angle
        self.safezone_occupied = self.fcc.safezone_occupied
        return
