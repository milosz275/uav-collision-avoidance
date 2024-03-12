# simulation_state.py

from PySide6.QtCore import QSettings, QTime
from PySide6.QtGui import QPixmap

from src.simulation.simulation_settings import SimulationSettings

class SimulationState(QSettings):
    """Class defining simulation's traits"""

    def __init__(self, simulation_settings : SimulationSettings) -> None:
        # simulation state
        self.simulation_settings = simulation_settings
        self.update_settings()
        # self.time_scale : float = 1.0 # define slow motion or fast forward
        self.physics_cycles : int = 0
        self.is_paused : bool = False
        self.pause_start_timestamp : QTime = None
        self.time_paused : int = 0.0 # ms

        # render state
        self.gui_scale : float = 1.0 # define gui scaling
        self.fps : float = 0.0

        # assets
        self.aircraft_pixmap : QPixmap = QPixmap()
        self.aircraft_pixmap.load("src/assets/aircraft.png")
        return
    
    def update_settings(self) -> None:
        """Updates all state settings"""
        self.update_render_settings()
        self.update_simulation_settings()
        self.update_adsb_settings()
        return
    
    def update_render_settings(self) -> None:
        """Updates simulation render state settings"""
        self.gui_render_threshold = self.simulation_settings.gui_render_threshold
        return
    
    def update_simulation_settings(self) -> None:
        """Updates simulation physics state settings"""
        self.simulation_threshold = self.simulation_settings.simulation_threshold
        self.g_acceleration = self.simulation_settings.g_acceleration
        return
    
    def update_adsb_settings(self) -> None:
        """Updates simulation ADS-B state settings"""
        self.adsb_threshold = self.simulation_settings.adsb_threshold
        return

    def toggle_pause(self) -> None:
        """Pauses the simulation"""
        if self.is_paused:
            self.time_paused += self.pause_start_timestamp.msecsTo(QTime.currentTime())
            self.is_paused = False
        else:
            self.pause_start_timestamp = QTime.currentTime()
            self.is_paused = True
        return
