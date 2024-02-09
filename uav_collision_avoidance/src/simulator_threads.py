# simulator_threads.py - threads usage template
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QLabel
from PySide6.QtGui import QPixmap, QIcon

class WorkerThread(QThread):
    data_updated = Signal(str)

    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator  # Reference to the SimulatorThreads instance

    def run(self):
        # Increment the number in the worker thread
        while not self.isInterruptionRequested():
            self.simulator.number += 1
            new_data = self.simulator.number
            self.simulator.update_data(new_data)
            self.data_updated.emit(str(new_data))
            self.sleep(1)

class SimulatorThreads(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("UAV Collision Avoidance")
        self.setGeometry(0, 0, 800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        self.aircraft_image = QPixmap()
        self.aircraft_image.load("src/assets/aircraft.png")

        self.icon = QIcon()
        self.icon.addPixmap(self.aircraft_image, QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(self.icon)

        self.number : int = 0

        self.label = QLabel(self)
        self.label.setText(str(self.number))
        self.setCentralWidget(self.label)

        self.worker_thread = WorkerThread(self)

        self.worker_thread.started.connect(self.worker_started)
        self.worker_thread.finished.connect(self.worker_finished)
        self.worker_thread.data_updated.connect(self.data_updated)

        self.worker_thread.start()

        self.show()
        return
    
    def worker_started(self):
        print("Worker thread started")

    def worker_finished(self):
        print("Worker thread finished")

    def update_data(self, new_data):
        self.data = new_data
        self.label.setText(str(self.data))

    def data_updated(self, new_data):
        print("Data updated:", new_data)

    def closeEvent(self, event):
        self.worker_thread.requestInterruption()
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()
