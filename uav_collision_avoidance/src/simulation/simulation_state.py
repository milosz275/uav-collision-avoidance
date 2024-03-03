# simulation_state.py

from PySide6.QtCore import QSettings
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

        # render state
        self.gui_scale : float = 1.0 # define gui scaling
        self.fps : float = 0.0

        # assets
        self.aircraft_pixmap : QPixmap = QPixmap()
        self.aircraft_pixmap.load("src/assets/aircraft.png")
        return
    
    def update_settings(self) -> None:
        """"""
        self.simulation_threshold = self.simulation_settings.simulation_threshold
        self.gui_render_threshold = self.simulation_settings.gui_render_threshold
        self.adsb_threshold = self.simulation_settings.adsb_threshold
        self.g_acceleration = self.simulation_settings.g_acceleration
        return

    def toggle_pause(self) -> None:
        """Pauses the simulation"""
        self.is_paused = not self.is_paused
        return
