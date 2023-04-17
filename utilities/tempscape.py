
import numpy as np

class TempScape:

    def __generate_tube_heater_distrobution(self, size: tuple) -> np.ndarray:
        pass
    def __init__(self, size: tuple) -> None:
        self.array = np.zeros(size, np.uint8)
        self.array = np.random.randint(0, 2, size)
