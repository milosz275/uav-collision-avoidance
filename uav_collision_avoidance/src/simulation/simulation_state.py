# simulation_state.py

from PySide6.QtGui import QPixmap, QImage

class SimulationState:
    """Class defining simulation's traits"""

    def __init__(self, simulation_threshold : int) -> None:
        # simulation state
        self.simulation_threshold = simulation_threshold
        self.adsb_threshold : float = 1000
        self.is_paused : bool = False

        # render state
        self.scale : float = 1.0

        # assets
        self.aircraft_pixmap : QPixmap = QPixmap()
        self.aircraft_pixmap.load("src/assets/aircraft.png")
        self.aircraft_image : QImage = self.aircraft_pixmap.toImage()
        return

    def toggle_pause(self) -> None:
        """Pauses the simulation"""
        self.is_paused = not self.is_paused
        return