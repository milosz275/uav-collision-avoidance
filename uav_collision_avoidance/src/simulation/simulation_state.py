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
        self.__simulation_settings = simulation_settings
        self.__is_realtime : bool = is_realtime
        self.__avoid_collisions : bool = avoid_collisions
        self.__override_avoid_collisions : bool = True
        self.__minimum_separation : float = 9260.0 # 5nmi
        self.__physics_cycles : int = 0
        self.__is_paused : bool = False
        self.__is_running : bool = True
        self.__reset_demanded : bool = False
        self.__pause_start_timestamp : QTime | None = None
        self.__time_paused : int = 0 # ms
        self.__adsb_report : bool = True
        self.__collision : bool = False
        self.__first_cause_collision : bool = False
        self.__second_cause_collision : bool = False
        self.__focused_aircraft_id : int = 0
        self.update_settings()

        # render state
        self.__fps : float = 0.0
        if is_realtime:
            override_gui_scale : bool = True
            if not override_gui_scale:
                self.__gui_scale : float = 0.5 # define gui scaling
                if SimulationSettings.screen_resolution.height() < 1440:
                    self.__gui_scale = 0.375
                elif SimulationSettings.screen_resolution.height() < 1080:
                    self.__gui_scale = 0.25
                elif SimulationSettings.screen_resolution.height() < 480:
                    self.__gui_scale = 0.125
            else:
                self.__gui_scale : float = 0.75
            self.__draw_fps : bool = True
            self.__draw_aircraft : bool = True
            self.__draw_grid : bool = False
            self.__draw_path : bool = True
            self.__draw_speed_vectors : bool = True
            self.__draw_safe_zones : bool = True
            self.__draw_collision_detection : bool = True
            self.__optimize_drawing : bool = False
            self.__follow_aircraft : bool = False

            # assets
            self.__aircraft_pixmap : QPixmap = QPixmap()
            if not self.__aircraft_pixmap.load("assets/aircraft.png"):
                try:
                    Path("assets").mkdir(parents=True, exist_ok=True)
                    urlretrieve(
                        "https://raw.githubusercontent.com/mldxo/uav-collision-avoidance/main/assets/aircraft.png",
                        "assets/aircraft.png")
                    self.__aircraft_pixmap.load("assets/aircraft.png")
                except:
                    pass

    @property
    def simulation_settings(self) -> SimulationSettings:
        """Returns simulation settings"""
        with QMutexLocker(self.__mutex):
            return self.__simulation_settings
    
    @property
    def is_realtime(self) -> bool:
        """Returns simulation type"""
        with QMutexLocker(self.__mutex):
            return self.__is_realtime
    
    @property
    def avoid_collisions(self) -> bool:
        """Returns collision avoidance flag"""
        with QMutexLocker(self.__mutex):
            return self.__avoid_collisions
    
    @avoid_collisions.setter
    def avoid_collisions(self, avoid_collisions : bool) -> None:
        """Sets collision avoidance flag"""
        with QMutexLocker(self.__mutex):
            self.__avoid_collisions = avoid_collisions

    def toggle_avoid_collisions(self) -> None:
        """Toggles collision avoidance"""
        with QMutexLocker(self.__mutex):
            self.__avoid_collisions = not self.__avoid_collisions

    @property
    def override_avoid_collisions(self) -> bool:
        """Returns collision avoidance override flag"""
        with QMutexLocker(self.__mutex):
            return self.__override_avoid_collisions
    
    @override_avoid_collisions.setter
    def override_avoid_collisions(self, override_avoid_collisions : bool) -> None:
        """Sets collision avoidance override flag"""
        with QMutexLocker(self.__mutex):
            self.__override_avoid_collisions = override_avoid_collisions

    @property
    def minimum_separation(self) -> float:
        """Returns minimum separation distance"""
        with QMutexLocker(self.__mutex):
            return self.__minimum_separation
    
    @property
    def physics_cycles(self) -> int:
        """Returns physics cycles count"""
        with QMutexLocker(self.__mutex):
            return self.__physics_cycles
        
    @physics_cycles.setter
    def physics_cycles(self, physics_cycles : int) -> None:
        """Sets physics cycles count"""
        with QMutexLocker(self.__mutex):
            self.__physics_cycles = physics_cycles
    
    @property
    def is_paused(self) -> bool:
        """Returns pause state"""
        with QMutexLocker(self.__mutex):
            return self.__is_paused
        
    @is_paused.setter
    def is_paused(self, is_paused : bool) -> None:
        """Sets pause state"""
        with QMutexLocker(self.__mutex):
            self.__is_paused = is_paused
        
    def toggle_pause(self) -> None:
        """Pauses the simulation"""
        if self.is_paused:
            self.append_time_paused()
            self.is_paused = False
        else:
            if not self.is_running:
                return
            self.pause_start_timestamp = QTime.currentTime()
            self.is_paused = True
    
    @property
    def is_running(self) -> bool:
        """Returns running state"""
        with QMutexLocker(self.__mutex):
            return self.__is_running
        
    @is_running.setter
    def is_running(self, is_running : bool) -> None:
        """Sets running state"""
        with QMutexLocker(self.__mutex):
            self.__is_running = is_running
    
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
    def pause_start_timestamp(self) -> QTime | None:
        """Returns pause start timestamp"""
        with QMutexLocker(self.__mutex):
            return self.__pause_start_timestamp
        
    @pause_start_timestamp.setter
    def pause_start_timestamp(self, pause_start_timestamp : QTime | None) -> None:
        """Sets pause start timestamp"""
        with QMutexLocker(self.__mutex):
            self.__pause_start_timestamp = pause_start_timestamp
        
    def append_time_paused(self) -> None:
        """Appends time elapsed during recent pause"""
        with QMutexLocker(self.__mutex):
            if self.__pause_start_timestamp is not None:
                self.__time_paused += self.__pause_start_timestamp.msecsTo(QTime.currentTime())
    
    @property
    def time_paused(self) -> int:
        """Returns time paused"""
        with QMutexLocker(self.__mutex):
            return self.__time_paused
        
    @time_paused.setter
    def time_paused(self, time_paused : int) -> None:
        """Sets time paused"""
        with QMutexLocker(self.__mutex):
            self.__time_paused = time_paused
    
    @property
    def adsb_report(self) -> None:
        """Returns ADS-B command-line info reporting flag"""
        with QMutexLocker(self.__mutex):
            return self.__adsb_report

    def toggle_adsb_report(self) -> None:
        """Toggles ADS-B command-line info report"""
        with QMutexLocker(self.__mutex):
            self.__adsb_report = not self.__adsb_report

    @property
    def collision(self) -> bool:
        """Returns collision state"""
        with QMutexLocker(self.__mutex):
            return self.__collision

    def register_collision(self) -> None:
        """Registers collision"""
        with QMutexLocker(self.__mutex):
            self.__collision = True
    
    @property
    def first_cause_collision(self) -> bool:
        """Returns causing collision state"""
        with QMutexLocker(self.__mutex):
            return self.__first_cause_collision
    
    def toggle_first_cause_collision(self) -> None:
        """Toggles causing collision state"""
        with QMutexLocker(self.__mutex):
            self.__first_cause_collision = not self.__first_cause_collision
    
    @property
    def second_cause_collision(self) -> bool:
        """Returns causing collision state"""
        with QMutexLocker(self.__mutex):
            return self.__second_cause_collision
    
    def toggle_second_cause_collision(self) -> None:
        """Toggles causing collision state"""
        with QMutexLocker(self.__mutex):
            self.__second_cause_collision = not self.__second_cause_collision

    @property
    def gui_scale(self) -> float:
        """Returns GUI scaling factor"""
        with QMutexLocker(self.__mutex):
            return self.__gui_scale
    
    @gui_scale.setter
    def gui_scale(self, gui_scale : float) -> None:
        """Sets GUI scaling factor"""
        with QMutexLocker(self.__mutex):
            self.__gui_scale = gui_scale

    @property
    def fps(self) -> float:
        """Returns FPS"""
        with QMutexLocker(self.__mutex):
            return self.__fps
    
    @fps.setter
    def fps(self, fps : float) -> None:
        """Sets FPS"""
        with QMutexLocker(self.__mutex):
            self.__fps = fps

    @property
    def draw_fps(self) -> bool:
        """Returns FPS display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_fps

    def toggle_draw_fps(self) -> None:
        """Toggles FPS display"""
        with QMutexLocker(self.__mutex):
            self.__draw_fps = not self.__draw_fps

    @property
    def draw_aircraft(self) -> bool:
        """Returns aircraft display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_aircraft
        
    def toggle_draw_aircraft(self) -> None:
        """Toggles aircraft display"""
        with QMutexLocker(self.__mutex):
            self.__draw_aircraft = not self.__draw_aircraft

    @property
    def draw_grid(self) -> bool:
        """Returns grid display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_grid
        
    def toggle_draw_grid(self) -> None:
        """Toggles grid display"""
        with QMutexLocker(self.__mutex):
            self.__draw_grid = not self.__draw_grid

    @property
    def draw_path(self) -> bool:
        """Returns path display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_path
        
    def toggle_draw_path(self) -> None:
        """Toggles path display"""
        with QMutexLocker(self.__mutex):
            self.__draw_path = not self.__draw_path

    @property
    def draw_speed_vectors(self) -> bool:
        """Returns speed vector display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_speed_vectors
        
    def toggle_draw_speed_vectors(self) -> None:
        """Toggles speed vector display"""
        with QMutexLocker(self.__mutex):
            self.__draw_speed_vectors = not self.__draw_speed_vectors

    @property
    def draw_safe_zones(self) -> bool:
        """Returns safe_zone display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_safe_zones
        
    def toggle_draw_safe_zones(self) -> None:
        """Toggles safe_zone display"""
        with QMutexLocker(self.__mutex):
            self.__draw_safe_zones = not self.__draw_safe_zones

    @property
    def draw_collision_detection(self) -> bool:
        """Returns collision detection display flag"""
        with QMutexLocker(self.__mutex):
            return self.__draw_collision_detection
        
    def toggle_draw_collision_detection(self) -> None:
        """Toggles collision detection display"""
        with QMutexLocker(self.__mutex):
            self.__draw_collision_detection = not self.__draw_collision_detection

    @property
    def optimize_drawing(self) -> bool:
        """Returns drawing optimization flag"""
        with QMutexLocker(self.__mutex):
            return self.__optimize_drawing
        
    def toggle_optimize_drawing(self) -> None:
        """Toggles drawing optimization"""
        with QMutexLocker(self.__mutex):
            self.__optimize_drawing = not self.__optimize_drawing

    @property
    def follow_aircraft(self) -> bool:
        """Returns aircraft following flag"""
        with QMutexLocker(self.__mutex):
            return self.__follow_aircraft
        
    def toggle_follow_aircraft(self) -> None:
        """Toggles aircraft following"""
        with QMutexLocker(self.__mutex):
            self.__follow_aircraft = not self.__follow_aircraft

    @property
    def focused_aircraft_id(self) -> int:
        """Returns aircraft id to focus on"""
        with QMutexLocker(self.__mutex):
            return self.__focused_aircraft_id
        
    def toggle_focus_aircraft(self) -> None:
        """Toggles aircraft focus"""
        with QMutexLocker(self.__mutex):
            self.__focused_aircraft_id = int(not self.__focused_aircraft_id)

    @property
    def gui_render_threshold(self) -> int:
        """Returns GUI render threshold"""
        with QMutexLocker(self.__mutex):
            return self.__gui_render_threshold
        
    @gui_render_threshold.setter
    def gui_render_threshold(self, gui_render_threshold : int) -> None:
        """Sets GUI render threshold"""
        with QMutexLocker(self.__mutex):
            self.__gui_render_threshold = gui_render_threshold

    @property
    def aircraft_pixmap(self) -> QPixmap:
        """Returns aircraft pixmap"""
        with QMutexLocker(self.__mutex):
            return self.__aircraft_pixmap
        
    @aircraft_pixmap.setter
    def aircraft_pixmap(self, aircraft_pixmap : QPixmap) -> None:
        """Sets aircraft pixmap"""
        with QMutexLocker(self.__mutex):
            self.__aircraft_pixmap = aircraft_pixmap

    @property
    def adsb_threshold(self) -> int:
        """Returns ADS-B threshold"""
        with QMutexLocker(self.__mutex):
            return self.__adsb_threshold
        
    @adsb_threshold.setter
    def adsb_threshold(self, adsb_threshold : int) -> None:
        """Sets ADS-B threshold"""
        with QMutexLocker(self.__mutex):
            self.__adsb_threshold = adsb_threshold

    @property
    def simulation_threshold(self) -> float:
        """Returns simulation threshold"""
        with QMutexLocker(self.__mutex):
            return self.__simulation_threshold
        
    @property
    def g_acceleration(self) -> float:
        """Returns acceleration due to gravity"""
        with QMutexLocker(self.__mutex):
            return self.__g_acceleration

    def update_settings(self) -> None:
        """Updates all state settings"""
        self.update_render_settings()
        self.update_simulation_settings()
        self.update_adsb_settings()

    def update_render_settings(self) -> None:
        """Updates simulation render state settings"""
        self.__gui_render_threshold = self.simulation_settings.gui_render_threshold
    
    def update_simulation_settings(self) -> None:
        """Updates simulation physics state settings"""
        self.__simulation_threshold = self.simulation_settings.simulation_threshold
        self.__g_acceleration = self.simulation_settings.g_acceleration
    
    def update_adsb_settings(self) -> None:
        """Updates simulation ADS-B state settings"""
        self.__adsb_threshold = self.simulation_settings.adsb_threshold

    def __del__(self) -> None:
        self.__mutex.unlock()
