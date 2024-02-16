# simulation_state.py

from PySide6.QtGui import QPixmap

class SimulationState:
    """Class defining simulation's traits"""

    def __init__(self, simulation_threshold : int) -> None:
        # simulation state
        self.simulation_threshold = simulation_threshold
        self.is_paused : bool = False

        # render state
        self.scale : float = 1.0

        # assets
        self.aircraft_image = QPixmap()
        self.aircraft_image.load("src/assets/aircraft.png")
        return

    def toggle_pause(self) -> None:
        self.is_paused = not self.is_paused
        return
