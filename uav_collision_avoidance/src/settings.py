# settings.py
from PySide6.QtCore import QSize

class Settings:
    """Settings"""
    screen_resolution : QSize
    resolution : tuple
    refresh_rate : int = 60
    g_acceleration : float = 9.81

    @classmethod
    def __init__(cls) -> None:
        """Initialises Settings using screen resolution"""
        cls.resolution = (int(cls.screen_resolution.width() * 0.6), int(cls.screen_resolution.height() * 0.75))
        return
    
    @classmethod
    def set_resolution(cls, width, height) -> None:
        """Sets the resolution"""
        cls.resolution = (width - 10, height - 10)
        return
    
    @classmethod
    def get_resolution(cls) -> None:
        """Gets the resolution"""
        return (cls.resolution[0], cls.resolution[1])

    @classmethod
    def set_refresh_rate(cls, rate) -> None:
        """Sets the refresh rate"""
        cls.refresh_rate = rate
        return
