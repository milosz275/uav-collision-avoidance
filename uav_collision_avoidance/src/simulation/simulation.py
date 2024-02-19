# simulation.py

from PySide6.QtCore import Qt, QPointF, QThread
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PySide6.QtGui import QCloseEvent, QPen, QKeySequence, QPixmap, QTransform, QVector2D, QPolygonF, QIcon

from src.aircraft.aircraft import Aircraft
from src.simulation.simulation_settings import SimulationSettings
from src.simulation.simulation_physics import SimulationPhysics
from src.simulation.simulation_state import SimulationState
from src.simulation.simulation_render import SimulationRender
from src.simulation.simulation_adsb import SimulationADSB

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

        self.simulation_render = SimulationRender([self.aircraft1.render, self.aircraft2.render], self.state)
        self.simulation_render.show()

        self.simulation_physics = SimulationPhysics(self, [self.aircraft1.vehicle, self.aircraft2.vehicle], self.state)
        self.simulation_physics.start()

        self.simulation_adsb = SimulationADSB(self, [self.aircraft1.vehicle, self.aircraft2.vehicle], self.state)
        self.simulation_adsb.start()
        return
    
    def stop_simulation(self) -> None:
        if self.simulation_physics:
            self.simulation_physics.requestInterruption()
            self.simulation_physics.quit()
            self.simulation_physics.wait()
        if self.simulation_adsb:
            self.simulation_adsb.requestInterruption()
            self.simulation_adsb.quit()
            self.simulation_adsb.wait()
        return
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.simulation_render.close()
        self.stop_simulation()
        event.accept()
        return super().closeEvent(event)
