import numpy as np

from cell_2d import Cell2D



def generate_waterlines(n, m, num_nipples):
    """Generates a list of waterlines.

    n: number of rows
    m: number of columns
    num_nipples: number of nipples

    returns: list of NumPy arrays
    """




class WaterScape(Cell2D):

    SPACING = 0.1

    def __init__(self, n, m):
        super().__init__(n, m)
        self.array = np.zeros((n, m), np.uint8)
        self.array = np.random.randint(0, 2, (n, m))
