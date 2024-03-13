# simulation.py

import logging
from typing import List

from PySide6.QtCore import QThread
from PySide6.QtGui import QCloseEvent, QVector3D
from PySide6.QtWidgets import QMainWindow

from src.aircraft.aircraft import Aircraft
from src.aircraft.aircraft_vehicle import AircraftVehicle
from src.aircraft.aircraft_render import AircraftRender
from src.simulation.simulation_settings import SimulationSettings
from src.simulation.simulation_physics import SimulationPhysics
from src.simulation.simulation_state import SimulationState
from src.simulation.simulation_render import SimulationRender
from src.simulation.simulation_widget import SimulationWidget
from src.simulation.simulation_adsb import SimulationADSB
from src.simulation.simulation_fps import SimulationFPS

class Simulation(QMainWindow):
    """Main simulation App"""

    def __init__(self) -> None:
        super().__init__()
        SimulationSettings().__init__()
        self.is_running : bool = False
        return

    def run_realtime(self) -> None:
        """Executes realtime simulation"""
        if self.is_running:
            print("Another instance already running")
            return
        logging.info("Starting realtime simulation")
        self.is_running = True
        self.state = SimulationState(SimulationSettings())

        self.aircrafts : List[Aircraft] = [
            Aircraft(position=QVector3D(10, 10, 1000), speed=QVector3D(100, 100, 0), state=self.state),
            Aircraft(position=QVector3D(100, 100, 1000), speed=QVector3D(100, 0, 0), state=self.state),
        ]

        self.aircraft_vehicles : List[AircraftVehicle] = [aircraft.vehicle() for aircraft in self.aircrafts]
        self.aircraft_renders : List[AircraftRender] = [aircraft.render() for aircraft in self.aircrafts]

        self.simulation_physics = SimulationPhysics(self, self.aircrafts, self.state)
        self.simulation_physics.start(priority=QThread.Priority.TimeCriticalPriority)

        self.simulation_adsb = SimulationADSB(self, self.aircraft_vehicles, self.state)
        self.simulation_adsb.start(priority=QThread.Priority.NormalPriority)

        self.simulation_fps = SimulationFPS(self, self.state)
        self.simulation_fps.start(priority=QThread.Priority.NormalPriority)

        self.simulation_widget = SimulationWidget(self.aircraft_renders, self.simulation_fps, self.state)
        self.simulation_widget.show()

        self.simulation_render = SimulationRender(self, self.simulation_widget, self.state)
        self.simulation_render.start(priority=QThread.Priority.NormalPriority)

        self.simulation_widget.stop_signal.connect(self.stop_simulation)
        return
    
    def run_prerender(self) -> None:
        """Executes prerender simulation"""
        if self.is_running:
            print("Another instance already running")
            return
        logging.info("Starting prerendered simulation")
        self.is_running = True
        # todo
        return

    def stop_simulation(self) -> None:
        """Finishes all active simulation threads"""
        if not self.is_running:
            return
        logging.info("Stopping simulation")

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
        print("Time elapsed: " + "{:.2f}".format(real_time) + "s (" + "{:.2f}".format(real_time_pauses) + "s with pauses)")
        print("Time efficiency: " + "{:.2f}".format(simulated_time / real_time * 100) + "%")
        logging.info("Calculated time efficiency: " + "{:.2f}".format(simulated_time / real_time * 100) + "%")

        self.simulation_adsb.quit()
        self.simulation_adsb.wait()
        self.simulation_render.quit()
        self.simulation_render.wait()
        self.simulation_fps.quit()
        self.simulation_fps.wait()
        return
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        self.stop_simulation()
        event.accept()
        return super().closeEvent(event)
