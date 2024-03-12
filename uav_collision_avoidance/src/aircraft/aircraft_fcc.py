# aircraft_fcc.py

from typing import List

from PySide6.QtCore import QObject
from PySide6.QtGui import QVector3D

class AircraftFCC(QObject):
    """Aircraft Flight Control Computer"""

    def __init__(self) -> None:
        super().__init__()
        
        self.safezone_occupied : bool = False

        self.target_yaw_angle : float = 0.0
        self.target_roll_angle : float = 30.0
        self.target_pitch_angle : float = 0.0
        # self.target_speed : float = 100.0

        self.points : List[QVector3D] = [
            QVector3D(10000, 10000, 1000),
            QVector3D(100000, 100000, 1000),
        ]
        return

    def update(self) -> None:
        """Updates current targetted movement angles"""
        # todo
        return
