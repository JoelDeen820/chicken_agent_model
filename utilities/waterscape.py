import numpy as np
from skimage.draw import disk

from chicken_utils import CENTIMETERS_PER_PIXEL


def make_visible_locs(vision):
    """Computes the kernel of visible cells.

    vision: int distance
    """

    def make_array(d):
        """Generates visible cells with increasing distance."""
        a = np.array([[-d, 0], [d, 0], [0, -d], [0, d]])
        np.random.shuffle(a)
        return a

    arrays = [make_array(d) for d in range(1, vision + 1)]
    return np.vstack(arrays)


class WaterScape:
    DISTANCE_BETWEEN_NIPPLES = 0.1  # in meters
    WATER_RADIUS = 0.01  # in meters
    DISTANCE_BETWEEN_LINES = 3.0  # in meters
    NUM_LINES = 2
    PIXELS_BETWEEN_LINES = DISTANCE_BETWEEN_LINES / CENTIMETERS_PER_PIXEL
    WATER_RADIUS_PIXELS = WATER_RADIUS / CENTIMETERS_PER_PIXEL
    PIXELS_BETWEEN_NIPPLES = DISTANCE_BETWEEN_NIPPLES / CENTIMETERS_PER_PIXEL

    def __draw_water_radius(self, points: list[tuple[int, int]]) -> None:
        """Draws the water radius around the given points."""
        for x, y in points:
            rr, cc = disk((x, y), self.WATER_RADIUS_PIXELS, shape=self.size)
            self.waterline_array[rr, cc] = 1

    def __draw_points(self, points: list[tuple[int, int]]) -> None:
        """Draws the given points."""
        for x, y in points:
            self.waterline_array[x, y] = 1

    def __generate_waterlines(self, points=True) -> None:
        """Generate the waterlines."""
        waterline_points = []
        for i in range(self.NUM_LINES):
            for j in range(self.num_nipples):
                x = self.waterline_offset_x + j * self.PIXELS_BETWEEN_NIPPLES
                y = self.waterline_offset_y + i * self.PIXELS_BETWEEN_LINES
                waterline_points.append((x, y))

        if points:
            self.__draw_points(waterline_points)
        else:
            self.__draw_water_radius(waterline_points)

    def __init__(self, size: tuple) -> None:
        """Initialize the WaterScape object.

        size: tuple, (width, height) in pixels
        """
        self.size = size
        self.num_nipples = size[0] // self.PIXELS_BETWEEN_NIPPLES
        self.waterline_offset_x = size[0] // 2 - self.PIXELS_BETWEEN_LINES // 2
        self.waterline_offset_y = size[1] // 2 - self.PIXELS_BETWEEN_LINES // 2
        self.waterline_array = np.zeros(size, dtype=np.uint8)
        self.__generate_waterlines()
        self.__occupancy_grid = np.zeros(size, dtype=np.uint8)

    def get_waterline_vision(self, center: tuple[int, int], vision: int) -> np.array:
        """ Find the visible waterline points for bird consumption.

        center: tuple, (x, y) in pixels
        vision: int, distance in pixels

        returns: np.array, (x, y) in pixels, where the points are waterlines visible."""
        visible_locations = make_visible_locs(vision) + center
        visible_space = self.waterline_array[visible_locations[:, 0], visible_locations[:, 1]]
        return visible_locations[np.argwhere(visible_space == 1)][:, 0, :]
