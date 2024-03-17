""""""

from PySide6.QtCore import QThread, QTime
from PySide6.QtGui import QCloseEvent

from src.simulation.simulation_state import SimulationState

class SimulationFPS(QThread):
    """Thread running frames per second counter"""

    def __init__(self, parent, simulation_state : SimulationState) -> None:
        super(SimulationFPS, self).__init__(parent)
        self.simulation_state = simulation_state
        self.counted_frames : int = 0
        self.previous_timestamp = QTime.currentTime()
        return
        
    def run(self) -> None:
        """Runs rendered simulation frames counter thread with precise 500ms timeout"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            elapsed_time : float = self.previous_timestamp.msecsTo(start_timestamp)
            if self.counted_frames > 0:
                self.simulation_state.fps = self.counted_frames / elapsed_time * 1000
                self.counted_frames = 0
            else:
                self.simulation_state.fps = 0.0
            self.previous_timestamp = QTime.currentTime()
            self.msleep(max(0, 500 - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()

    def count_frame(self) -> None:
        """Increments fps count"""
        self.counted_frames += 1

    def closeEvent(self, event: QCloseEvent) -> None:
        """Qt method performed on the main window close event"""
        event.accept()
        return super().closeEvent(event)
