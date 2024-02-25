# aircraft_fcc.py

from PySide6.QtCore import QObject

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""

    def __init__(self) -> None:
        super().__init__()
        
        self.safezone_occupied : bool = False

        self.target_yaw_angle : float = 0.0
        self.target_roll_angle : float = 0.0
        self.target_pitch_angle : float = 0.0

        return
