# simulation.py

from PySide6.QtCore import Qt, QPointF, QThread
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PySide6.QtGui import QCloseEvent, QPen, QKeySequence, QPixmap, QTransform, QVector2D, QPolygonF, QIcon

from src.aircraft.aircraft import Aircraft
from src.simulation.simulation_settings import SimulationSettings
from src.simulation.simulation_physics import SimulationPhysics
from src.simulation.simulation_state import SimulationState
from src.simulation.simulation_render import SimulationRender

from typing import List
from math import radians, sin, cos, atan2, degrees, dist, sqrt
from copy import copy

class Simulation(QMainWindow):
    """Main simulation App"""

    def __init__(self) -> None:
        super().__init__()
        SimulationSettings().__init__()

        self.state = SimulationState(SimulationSettings.simulation_threshold)

        self.aircraft1 = Aircraft(10, 10, 1000, "red", self.state)
        self.aircraft2 = Aircraft(100, 100, 1000, "blue", self.state)

        self.render_widget = SimulationRender([self.aircraft1.render, self.aircraft2.render], self.state)
        self.render_widget.show()

        self.simulation_thread = SimulationPhysics(self, [self.aircraft1.vehicle, self.aircraft2.vehicle], self.state)
        self.simulation_thread.start()
        return
    
    def stop_simulation(self) -> None:
        if self.simulation_thread:
            self.simulation_thread.requestInterruption()
            self.simulation_thread.quit()
            self.simulation_thread.wait()
        return
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.render_widget.close()
        self.stop_simulation()
        event.accept()
        return super().closeEvent(event)
