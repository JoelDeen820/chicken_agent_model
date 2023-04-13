import numpy as np

from chicken import Chicken, ChickenNeed
from foodscape import FoodScape
from tempscape import TempScape
from waterscape import WaterScape


def make_locs(n, m):
    """Makes array where each row is an index in an `n` by `m` grid.

    n: int number of rows
    m: int number of cols

    returns: NumPy array
    """
    t = [(i, j) for i in range(n) for j in range(m)]
    return np.array(t)


class Barn:

    def __create_chickens(self) -> list:
        """Creates a list of chickens.

        size: tuple of the size of the barn
        """
        chickens = []
        make_locs(self.barn_size[0], self.barn_size[1])
        for loc in make_locs(self.barn_size[0], self.barn_size[1]):
            self.chickens.append(Chicken(loc))

        self.occupacy = set(chicken.loc for chicken in self.chickens)

    def __init__(self, size: tuple) -> None:
        self.waterlines = WaterScape(size)
        self.feedlines = FoodScape(size)
        self.temp_fluxuations = TempScape(size)
        self.barn_size = size
        self.chickens = self.__create_chickens()
        self.occupacy = set()

    def look_and_move(self, loc: tuple[int, int], vision: int, need: ChickenNeed) -> tuple[int, int]:
        """Look around and move to a new location.

        loc: tuple of coordinates
        vision: int distance
        """
        locs = None

        if need == ChickenNeed.HAPPY:
            # No need to move the bird as it is already good.
            return loc
        if need == ChickenNeed.THIRST:
            locs = self.waterlines.get_vision(loc, vision)
        elif need == ChickenNeed.HUNGER:
            pass
        elif need == ChickenNeed.TEMPERATURE:
            pass

        locs = [tuple(loc) for loc in locs]

        empty_locs = [loc for loc in locs if self.occupacy[loc] == 0]

        if len(empty_locs) == 0:
            # Start looking for resource

            return loc

        return empty_locs[0]

    def step(self):
        """Simulates one time step."""
        random_order = np.random.permutation(len(self.chickens))
        for chicken in random_order:
            self.occupacy.remove(chicken.loc)
            chicken.step(self)
            self.occupacy.add(chicken.loc)
