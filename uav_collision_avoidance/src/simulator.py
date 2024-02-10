# simulator.py
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsPixmapItem, QGraphicsPolygonItem
from PySide6.QtGui import QPen, QKeySequence, QPixmap, QTransform, QVector2D, QPolygonF
from src.aircraft import Aircraft
from src.settings import Settings
from src.fps_counter import FPSCounter
from math import radians, sin, cos, atan2, degrees, dist, sqrt
from copy import copy

class Simulator(QMainWindow):
    """Main simulation App"""

    def __init__(self) -> None:
        super().__init__()
        Settings().__init__()
        
        self.show()
        return
