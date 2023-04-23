from math import pi

import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from IPython.display import clear_output
from scipy.signal import convolve2d

from utilities.chicken import Chicken, ChickenNeed
from utilities.chicken_utils import filter_locs
from utilities.need_not_availible import NeedNotFoundException
from utilities.utils import underride
from utilities.waterscape import WaterScape
from utilities.foodscape import FoodScape
from utilities.tempscape import TempScape


def make_locs(n, m):
    """Makes array where each row is an index in an `n` by `m` grid.

    n: int number of rows
    m: int number of cols

    returns: NumPy array
    """
    t = [(i, j) for i in range(n) for j in range(m)]
    return np.array(t)


def draw_array(array, **options) -> None:
    """Draws the cells."""
    n, m = array.shape
    options = underride(options,
                        cmap='Greens',
                        alpha=0.7,
                        vmin=0, vmax=1,
                        interpolation='none',
                        origin='upper',
                        extent=[0, m, 0, n])

    plt.axis([0, m, 0, n])
    plt.xticks([])
    plt.yticks([])

    return plt.imshow(array, **options)

def get_floor_odd_number(number: int) -> int:
    """Gets the floor of the number and makes it odd.

    number: int

    returns: int
    """
    return int(np.floor(number) // 2 * 2 + 1)


class Barn:

    def __create_chickens(self, num_birds: int) -> None:
        """Creates a list of chickens.

        size: tuple of the size of the barn
        """

        locs = make_locs(self.barn_size[0], self.barn_size[1])
        np.random.shuffle(locs)
        for i in range(num_birds):
            self.chickens.append(Chicken(locs[i]))

        self.occupacy = set(chicken.loc for chicken in self.chickens)

    def temp(self, loc) -> float:
        """Returns the temperature increase per second at loc, assuming the mass is 174 g (Average mass of a chicken)
        """
        return self.temp_fluxuations.heater_array[loc] / 174

    def __init__(self, size: tuple, num_chickens=500, tube_heaters=0) -> None:
        self.waterlines = WaterScape(size)
        self.feedlines = FoodScape(size)
        self.temp_fluxuations = TempScape(size, tube_heaters)
        self.barn_size = size
        self.occupacy = set()
        self.chickens = []
        self.__create_chickens(num_chickens)
        self.points = None

    def look_and_move(self, loc: tuple[int, int], vision: int, need: ChickenNeed, wander_angle: float) -> tuple[
        int, int]:
        """Look around and move to a new location.

        loc: tuple of coordinates
        vision: int distance
        """
        locs = None
        try:
            if need == ChickenNeed.HAPPY:
                # No need to move the bird as it is already good.
                return loc
            if need == ChickenNeed.THIRST:
                locs = self.waterlines.get_vision(loc, vision)
            elif need == ChickenNeed.HUNGER:
                locs = self.feedlines.get_vision(loc, vision)
            elif need == ChickenNeed.TEMPERATURE:
                locs = self.temp_fluxuations.get_vision(loc, vision)
        except NeedNotFoundException:
            return self.wander(loc, vision, wander_angle)

        locs = [tuple(loc) for loc in locs]

        empty_locs = [loc for loc in locs if loc not in self.occupacy]

        if len(empty_locs) == 0:
            # Start looking for resource

            return self.wander(loc, vision, wander_angle)

        return empty_locs[0]

    def wander(self, loc: tuple[int, int], vision: int, wander_angle: float) -> tuple[int, int]:
        """ Gets the bird to look around the barn for the required resource.
        """
        wander_samples = 20

        empty_locs = []

        wander_vision = vision

        while len(empty_locs) == 0:
            search_angles = (np.random.random(wander_samples) * pi / 2) - pi / 4 + wander_angle
            x = (wander_vision * np.cos(search_angles)).astype(np.int16)
            y = (wander_vision * np.sin(search_angles)).astype(np.int16)
            np_locs = filter_locs(np.array([x, y]).T + loc, self.barn_size)
            locs = [tuple(loc) for loc in np_locs]

            empty_locs = [loc for loc in locs if loc not in self.occupacy]
            wander_vision -= 1
            if wander_vision <= 0:
                break

        if len(empty_locs) == 0:
            return loc
        else:
            return empty_locs[0]

    def step(self) -> None:
        """Simulates one time step."""
        random_order = np.random.permutation(self.chickens)
        for chicken in random_order:
            self.occupacy.remove(chicken.loc)
            chicken.step(self)
            self.occupacy.add(chicken.loc)

    def get_coords(self) -> tuple[np.ndarray, np.ndarray]:
        """Gets the coordinates of the chickens."""

        chickens = self.chickens
        rows, cols = np.transpose([chicken.loc for chicken in chickens])
        xs = cols + 0.5
        ys = rows + 0.5
        return xs, ys

    def draw(self) -> None:
        """ Draws the Top-Down view of the barn
        """
        draw_array(self.temp_fluxuations.heater_array, cmap='cividis', origin='upper')
        draw_array(self.waterlines.waterline_array, cmap='viridis', origin='upper')
        draw_array(self.feedlines.feedline_array, cmap='viridis', origin='upper')

        xs, ys = self.get_coords()
        self.points = plt.plot(xs, ys, '.', color='white')[0]

    def animate(self, interval=0.1, frames=10, step=None) -> None:
        """ Animates a Top-Down view of the barn environment

            frames: number of frames to draw
            interval: time between frames in seconds
        """
        if step == None:
            step = self.step

        try:
            for i in range(frames-1):
                self.draw()
                plt.show()
                if interval:
                    sleep(interval)
                step()
                clear_output(wait=True)
            self.draw()
            plt.show()
        except KeyboardInterrupt:
            pass

    def measure_uniformity(self) -> float:
        """ Measures the uniformity of the barn.
        """
        num_birds = len(self.chickens)
        kernel_size = get_floor_odd_number(np.sqrt(num_birds))
        kernel = np.ones((kernel_size, kernel_size))
        kernel[kernel_size // 2, kernel_size // 2] = 0
        bird_locs = np.array(list(map(np.array, self.occupacy)))
        occupancy_array = np.zeros(self.barn_size)
        occupancy_array[bird_locs[:, 0], bird_locs[:, 1]] = 1
        count_result = convolve2d(occupancy_array, kernel, mode='same')
        filtered_result = count_result[bird_locs[:, 0], bird_locs[:, 1]]
        return np.std(filtered_result)

