import numpy as np

from cell_2d import Cell2D


def generate_waterlines(n, m, num_nipples):
    """Generates a list of waterlines.

    n: number of rows
    m: number of columns
    num_nipples: number of nipples

    returns: list of NumPy arrays
    """
    pass



class WaterScape(Cell2D):

    SPACING = 0.1
    WATER_RADIUS = 0.01

    def __init__(self, size: tuple) -> None:
        super().__init__(size[0], size[1])
        self.array = np.zeros(size, np.uint8)
        self.array = np.random.randint(0, 2, size)
