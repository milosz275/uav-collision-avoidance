"""Simulation state module"""

from urllib.request import urlretrieve
from pathlib import Path

from PySide6.QtCore import QSettings, QTime, QMutex, QMutexLocker
from PySide6.QtGui import QPixmap

from .simulation_settings import SimulationSettings

class SimulationState(QSettings):
    """Class defining simulation's traits"""

    def __init__(self, simulation_settings : SimulationSettings, is_realtime : bool = True, avoid_collisions : bool = False) -> None:
        super(SimulationState, self).__init__()
        self.__mutex : QMutex = QMutex()

        # simulation state
        self.simulation_settings = simulation_settings
        self.update_settings()
        self.is_realtime : bool = is_realtime
        self.avoid_collisions : bool = avoid_collisions
        self.minimum_separation : float = 9260.0 # 5nmi
        self.physics_cycles : int = 0
        self.is_paused : bool = False
        self.is_running : bool = True
        self.__reset_demanded : bool = False
        self.pause_start_timestamp : QTime | None = None
        self.time_paused : int = 0 # ms
        self.__adsb_report : bool = False
        self.__collision : bool = False
        self.__first_cause_collision : bool = False
        self.__second_cause_collision : bool = False

        if is_realtime:
            # render state
            self.__gui_scale : float = 1.0 # define gui scaling
            if SimulationSettings.screen_resolution.height() < 1440:
                self.gui_scale = 0.75
            elif SimulationSettings.screen_resolution.height() < 1080:
                self.gui_scale = 0.5
            elif SimulationSettings.screen_resolution.height() < 480:
                self.gui_scale = 0.25
            self.fps : float = 0.0
            self.draw_fps : bool = True
            self.draw_aircraft : bool = True
            self.draw_grid : bool = False
            self.draw_path : bool = True
            self.draw_speed_vectors : bool = True
            self.draw_collision_detection : bool = True
            self.optimize_drawing : bool = False
            self.follow_aircraft : bool = False
            self.focus_aircraft_id : int = 0

            # assets
            self.aircraft_pixmap : QPixmap = QPixmap()
            if not self.aircraft_pixmap.load("assets/aircraft.png"):
                try:
                    Path("assets").mkdir(parents=True, exist_ok=True)
                    urlretrieve(
                        "https://raw.githubusercontent.com/mldxo/uav-collision-avoidance/main/assets/aircraft.png",
                        "assets/aircraft.png")
                    self.aircraft_pixmap.load("assets/aircraft.png")
                except:
                    pass
    
    @property
    def adsb_report(self) -> None:
        """Returns ADS-B commandline info reporting flag"""
        return self.__adsb_report

    def update_settings(self) -> None:
        """Updates all state settings"""
        self.update_render_settings()
        self.update_simulation_settings()
        self.update_adsb_settings()

    def toggle_adsb_report(self) -> None:
        """Toggles ADS-B commandline info report"""
        self.__adsb_report = not self.__adsb_report
    
    def update_render_settings(self) -> None:
        """Updates simulation render state settings"""
        self.gui_render_threshold = self.simulation_settings.gui_render_threshold
    
    def update_simulation_settings(self) -> None:
        """Updates simulation physics state settings"""
        self.simulation_threshold = self.simulation_settings.simulation_threshold
        self.g_acceleration = self.simulation_settings.g_acceleration
    
    def update_adsb_settings(self) -> None:
        """Updates simulation ADS-B state settings"""
        self.adsb_threshold = self.simulation_settings.adsb_threshold

    def append_paused_time(self) -> None:
        """Appends time elapsed during recent pause"""
        if self.pause_start_timestamp is not None:
            self.time_paused += self.pause_start_timestamp.msecsTo(QTime.currentTime())

    def toggle_pause(self) -> None:
        """Pauses the simulation"""
        if self.is_paused:
            self.append_paused_time()
            self.is_paused = False
        else:
            if not self.is_running:
                return
            self.pause_start_timestamp = QTime.currentTime()
            self.is_paused = True
    
    @property
    def collision(self) -> bool:
        """Returns collision state"""
        return self.__collision

    def register_collision(self) -> None:
        """Registers collision"""
        self.__collision = True
    
    @property
    def first_cause_collision(self) -> bool:
        """Returns causing collision state"""
        return self.__first_cause_collision
    
    def toggle_first_causing_collision(self) -> None:
        """Toggles causing collision state"""
        self.__first_cause_collision = not self.__first_cause_collision
    
    @property
    def second_cause_collision(self) -> bool:
        """Returns causing collision state"""
        return self.__second_cause_collision
    
    def toggle_second_causing_collision(self) -> None:
        """Toggles causing collision state"""
        self.__second_cause_collision = not self.__second_cause_collision
    
    @property
    def reset_demanded(self) -> bool:
        """Returns simulation reset state"""
        with QMutexLocker(self.__mutex):
            return self.__reset_demanded

    def reset(self) -> None:
        """Resets simulation to its start state"""
        with QMutexLocker(self.__mutex):
            self.__reset_demanded = True

    def apply_reset(self) -> None:
        """Sets back simulation reset state"""
        with QMutexLocker(self.__mutex):
            self.__reset_demanded = False

    @property
    def gui_scale(self) -> float:
        """Returns GUI scaling factor"""
        return self.__gui_scale
    
    @gui_scale.setter
    def gui_scale(self, value : float) -> None:
        """Sets GUI scaling factor"""
        if value > 0.0:
            self.__gui_scale = value
