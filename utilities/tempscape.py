
import numpy as np

from cell_2d import Cell2D

class TempScape(Cell2D):

    def __generate_tube_heater_distrobution(self, size: tuple) -> np.ndarray:
        pass
    def __init__(self, size: tuple) -> None:
        super().__init__(size[0], size[1])
        self.array = np.zeros(size, np.uint8)
        self.array = np.random.randint(0, 2, size)
