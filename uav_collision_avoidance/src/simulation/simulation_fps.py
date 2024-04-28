"""Simulation frames per second counter thread module"""

from PySide6.QtCore import QThread, QTime, QMutex, QMutexLocker
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow

from .simulation_state import SimulationState

class SimulationFPS(QThread):
    """Thread running frames per second counter"""

    def __init__(self, parent : QMainWindow, simulation_state : SimulationState) -> None:
        super(SimulationFPS, self).__init__(parent)
        self.__mutex : QMutex = QMutex()
        self.__simulation_state = simulation_state
        self.__counted_frames : int = 0
        self.__previous_timestamp = QTime.currentTime()
        
    def run(self) -> None:
        """Runs rendered simulation frames counter thread with precise 500ms timeout"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            elapsed_time : float = self.previous_timestamp.msecsTo(start_timestamp)
            if self.counted_frames() > 0:
                self.simulation_state.fps = self.counted_frames() / elapsed_time * 1000
                self.reset_frames()
            else:
                self.simulation_state.fps = 0.0
            self.previous_timestamp = QTime.currentTime()
            self.msleep(max(0, 500 - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()

    def count_frame(self) -> None:
        """Increments fps count"""
        with QMutexLocker(self.__mutex):
            self.__counted_frames += 1

    def reset_frames(self) -> None:
        """Resets fps count"""
        with QMutexLocker(self.__mutex):
            self.__counted_frames = 0

    def counted_frames(self) -> int:
        """Returns counted frames"""
        with QMutexLocker(self.__mutex):
            return self.__counted_frames
        
    @property
    def simulation_state(self) -> SimulationState:
        """Returns simulation state"""
        with QMutexLocker(self.__mutex):
            return self.__simulation_state
    
    @property
    def previous_timestamp(self) -> QTime:
        """Returns previous timestamp"""
        with QMutexLocker(self.__mutex):
            return self.__previous_timestamp
    
    @previous_timestamp.setter
    def previous_timestamp(self, previous_timestamp : QTime) -> None:
        """Sets previous timestamp"""
        with QMutexLocker(self.__mutex):
            self.__previous_timestamp = previous_timestamp

    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        event.accept()
        return super().closeEvent(event)
