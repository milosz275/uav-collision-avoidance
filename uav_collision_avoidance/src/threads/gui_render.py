# gui_render.py
from PySide6.QtCore import QThread

class GuiRenderer(QThread):
    """Gui Renderer"""

    def __init__(self, simulator):
        super().__init__()
        self.setParent(simulator)
        self.simulator = simulator

    def run(self):
        while not self.isInterruptionRequested():
            self.simulator.render_scene()
            self.msleep(100)
