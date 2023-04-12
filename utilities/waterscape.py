import numpy as np
from skimage.draw import disk

from chicken_utils import CENTIMETERS_PER_PIXEL


class WaterScape:

    DISTANCE_BETWEEN_NIPPLES = 0.1  # in meters
    WATER_RADIUS = 0.01  # in meters
    DISTANCE_BETWEEN_LINES = 3.0  # in meters
    NUM_LINES = 2
    PIXELS_BETWEEN_LINES = DISTANCE_BETWEEN_LINES / CENTIMETERS_PER_PIXEL
    WATER_RADIUS_PIXELS = WATER_RADIUS / CENTIMETERS_PER_PIXEL
    PIXELS_BETWEEN_NIPPLES = DISTANCE_BETWEEN_NIPPLES / CENTIMETERS_PER_PIXEL


    def __generate_waterlines(self) -> None:
        """Generate the waterlines."""
        waterline_points = []
        for i in range(self.NUM_LINES):
            for j in range(self.num_nipples):
                x = self.waterline_offset_x + j * self.PIXELS_BETWEEN_NIPPLES
                y = self.waterline_offset_y + i * self.PIXELS_BETWEEN_LINES
                waterline_points.append((x, y))

        for x, y in waterline_points:
            rr, cc = disk((x, y), self.WATER_RADIUS_PIXELS, shape=self.size)
            self.waterline_array[rr, cc] = 1

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

