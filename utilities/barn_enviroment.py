

from waterscape import WaterScape
from foodscape import FoodScape
from tempscape import TempScape
from chicken import Chicken

class Barn:

    def __create_chickens(self) -> list:
        """Creates a list of chickens.

        size: tuple of the size of the barn
        """
        chickens = []
        for i in range(self.barn_size[0]):
            for j in range(self.barn_size[1]):
                chickens.append(Chicken())

        return chickens

    def __init__(self, size: tuple) -> None:
        self.waterlines = WaterScape(size)
        self.feedlines = FoodScape(size)
        self.temp_fluxuations = TempScape(size)
        self.barn_size = size
        self.chickens = self.__create_chickens()

