# simulation_state.py

class SimulationState:
    def __init__(self) -> None:
        self._is_paused : bool = False
        return
    
    def is_paused(self) -> bool:
        return self._is_paused

    def toggle_pause(self) -> None:
        self._is_paused = not self._is_paused
        return
