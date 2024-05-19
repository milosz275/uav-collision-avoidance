"""Simulation settings"""

from PySide6.QtCore import QSize

class SimulationSettings:
    """Settings for the simulation"""

    screen_resolution : QSize | None = None
    resolution : tuple
    g_acceleration : float = 9.81
    simulation_frequency : float = 100.0
    simulation_threshold : float = 1000.0 / simulation_frequency
    gui_render_frequency : float = 100.0
    gui_render_threshold : float =  1000.0 / gui_render_frequency
    adsb_threshold : float = 1000.0

    @classmethod
    def __init__(cls) -> None:
        """Initializes Settings using screen resolution"""
        if cls.screen_resolution is not None:
            cls.resolution = (int(cls.screen_resolution.width() * 0.6), int(cls.screen_resolution.height() * 0.75))
