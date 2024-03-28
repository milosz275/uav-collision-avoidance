"""Simulation rendering thread module"""

from PySide6.QtCore import QThread, QTime
from PySide6.QtWidgets import QMainWindow

from .simulation_widget import SimulationWidget
from .simulation_state import SimulationState

class SimulationRender(QThread):
    """Thread running simulation rendering"""

    def __init__(self, parent : QMainWindow, simulation_widget : SimulationWidget, simulation_state : SimulationState) -> None:
        super(SimulationRender, self).__init__(parent)
        self.simulation_widget = simulation_widget
        self.simulation_state = simulation_state
        
    def run(self) -> None:
        """Runs simulation widget update with precise timeout"""
        while not self.isInterruptionRequested():
            start_timestamp = QTime.currentTime()
            self.simulation_state.update_render_settings()
            self.simulation_widget.update()
            self.msleep(max(0, self.simulation_state.gui_render_threshold - start_timestamp.msecsTo(QTime.currentTime())))
        return super().run()
