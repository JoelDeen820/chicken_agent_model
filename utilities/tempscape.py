import math

import numpy as np
from skimage.draw import disk

from utilities.chicken_utils import CENTIMETERS_PER_PIXEL, filter_locs, make_visible_locs
from utilities.need_not_availible import NeedNotFoundException


class TempScape:
    DISTANCE_BETWEEN_HEATERS = 3  # meters
    HEAT_RADIUS = 15  # meters
    BARN_HEIGHT = 5  # meters
    HEATER_INTENSITY = 117000 / (math.pow(BARN_HEIGHT, 2))  # In W
    DISTANCE_BETWEEN_LINES = 4  # in meters
    NUM_LINES = 2
    X_PERMINITER_OFFSET = 2.5  # meters
    Y_PERMINITER_OFFSET = 1.5  # meters
    PIXELS_BETWEEN_HEATERS = int(DISTANCE_BETWEEN_HEATERS * 100 / CENTIMETERS_PER_PIXEL)
    HEAT_RADIUS_PIXELS = int((HEAT_RADIUS - BARN_HEIGHT) * 100 / CENTIMETERS_PER_PIXEL)
    PIXELS_BETWEEN_LINES = int(DISTANCE_BETWEEN_LINES * 100 / CENTIMETERS_PER_PIXEL)
    X_PERMINITER_OFFSET_PIXELS = int(X_PERMINITER_OFFSET * 100 / CENTIMETERS_PER_PIXEL)
    Y_PERMINITER_OFFSET_PIXELS = int(Y_PERMINITER_OFFSET * 100 / CENTIMETERS_PER_PIXEL)
    MINIMIUM_TEMPUATURE = 25  # degrees celcius

    def __generate_tube_heater_heatmap(self, points=False) -> None:
        """Generate the heatmap for tube heaters."""
        heat_points = []
        for i in range(self.num_rows):
            for j in range(self.size[0]):  # uses all pixels as heat sources
                x = int(self.Y_PERMINITER_OFFSET_PIXELS + j * (self.PIXELS_BETWEEN_HEATERS // 10))
                y = int(self.X_PERMINITER_OFFSET_PIXELS + i * self.PIXELS_BETWEEN_LINES)
                heat_points.append((x, y))

        if points:
            self.__draw_points(heat_points)
        else:
            self.__draw_heat_radius(heat_points)

    def __draw_heat_radius(self, points: list[tuple[int, int]]) -> None:
        """Draws the heat radius around the given points."""
        for x, y in points:
            rr, cc = disk((x, y), self.HEAT_RADIUS_PIXELS, shape=self.size)
            for i in range(len(rr)):
                if math.dist((x, y), (rr[i], cc[i])) != 0:
                    self.heater_array[rr[i], cc[i]] += self.HEATER_INTENSITY / (
                        (math.pow(math.dist((x, y), (rr[i], cc[i])), 2)))
                else:
                    self.heater_array[rr[i], cc[i]] += self.HEATER_INTENSITY

    def __draw_points(self, points: list[tuple[int, int]]) -> None:
        """Draws the given points."""
        for x, y in points:
            self.heater_array[x, y] = self.HEATER_INTENSITY

    def __generate_heatmap(self, points=False) -> None:
        """Generate the heatmap for ceiling heaters."""
        heat_points = []
        for i in range(self.num_rows):
            for j in range(self.num_lines):
                x = int(self.Y_PERMINITER_OFFSET_PIXELS + j * self.PIXELS_BETWEEN_HEATERS)
                y = int(self.X_PERMINITER_OFFSET_PIXELS + i * self.PIXELS_BETWEEN_LINES)
                heat_points.append((x, y))
        if points:
            self.__draw_points(heat_points)
        else:
            self.__draw_heat_radius(heat_points)
        self.heater_array += self.MINIMIUM_TEMPUATURE

    def __init__(self, size: tuple, is_tube_heater=False) -> None:
        """Initialize the TempScape object.

        size: tuple, (width, height) in pixels
        is_tube_heater: int, 0 for ceiling heaters, 1 for tube heaters
        """
        self.size = size
        num_heaters: int = size[0] // self.PIXELS_BETWEEN_HEATERS
        self.num_lines: int = int(num_heaters)
        self.num_rows: int = size[1] // self.PIXELS_BETWEEN_LINES
        self.heater_offset_y: int = self.Y_PERMINITER_OFFSET_PIXELS
        self.heater_array: np.array = np.zeros(size, dtype=np.uint8)
        if is_tube_heater:
            self.__generate_tube_heater_heatmap()
        else:
            self.__generate_heatmap()
        self.__occupancy_grid: np.array = np.zeros(size, dtype=np.uint8)

    def get_vision(self, center: tuple[int, int], vision: int) -> np.array:
        """ Find the visible heaters points for bird consumption.

        center: tuple, (x, y) in pixels
        vision: int, distance in pixels

        returns: np.array, (x, y) in pixels, where the points are waterlines visible."""
        visible_locations = filter_locs(make_visible_locs(vision) + center, self.size)
        visible_space = self.heater_array[visible_locations[:, 0], visible_locations[:, 1]]
        locations: np.array = visible_locations[np.argwhere(visible_space == 1)]
        if locations.size == 1:
            raise NeedNotFoundException
        return locations[:, 0, :]

    def get_current_temp(self, point: tuple[int, int]) -> int:
        """Get the current temperature at the given point.

        point: tuple, (x, y) in pixels

        returns: int, temperature in degrees celcius"""
        return self.heater_array[point[0], point[1]]
