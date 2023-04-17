import numpy as np
from skimage.draw import disk

from utilities.chicken_utils import CENTIMETERS_PER_PIXEL, filter_locs, make_visible_locs
from utilities.need_not_availible import NeedNotFoundException


class WaterScape:
    DISTANCE_BETWEEN_NIPPLES = 0.35  # in meters
    WATER_RADIUS = 0.1  # in meters
    DISTANCE_BETWEEN_LINES = 3.0  # in meters
    NUM_LINES = 2
    X_PERMINITER_OFFSET = 1.0  # meters
    Y_PERMINITER_OFFSET = 0.03  # meters
    PIXELS_BETWEEN_LINES = int(DISTANCE_BETWEEN_LINES * 100 / CENTIMETERS_PER_PIXEL)
    WATER_RADIUS_PIXELS = int(WATER_RADIUS * 100 / CENTIMETERS_PER_PIXEL)
    PIXELS_BETWEEN_NIPPLES = int(DISTANCE_BETWEEN_NIPPLES * 100 / CENTIMETERS_PER_PIXEL)
    X_PERMINITER_OFFSET_PIXELS = int(X_PERMINITER_OFFSET * 100 / CENTIMETERS_PER_PIXEL)
    Y_PERMINITER_OFFSET_PIXELS = int(Y_PERMINITER_OFFSET * 100 / CENTIMETERS_PER_PIXEL)

    def __draw_water_radius(self, points: list[tuple[int, int]]) -> None:
        """Draws the water radius around the given points."""
        for x, y in points:
            rr, cc = disk((x, y), self.WATER_RADIUS_PIXELS, shape=self.size)
            self.waterline_array[rr, cc] = 1

    def __draw_points(self, points: list[tuple[int, int]]) -> None:
        """Draws the given points."""
        for x, y in points:
            self.waterline_array[x, y] = 1

    def __generate_waterlines(self, points=False) -> None:
        """Generate the waterlines."""
        waterline_points = []
        for i in range(self.num_lines):
            for j in range(self.num_nipples):
                x = int(self.Y_PERMINITER_OFFSET_PIXELS + j * self.PIXELS_BETWEEN_NIPPLES)
                y = int(self.X_PERMINITER_OFFSET_PIXELS + i * self.PIXELS_BETWEEN_LINES)
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
        num_nipples: int = size[0] // self.PIXELS_BETWEEN_NIPPLES
        self.num_nipples: int = int(num_nipples)
        # self.waterline_offset_x = (size[0] - 1) // 2 - self.PIXELS_BETWEEN_LINES // 2
        self.num_lines: int = size[1] // self.PIXELS_BETWEEN_LINES
        self.waterline_offset_y: int = self.Y_PERMINITER_OFFSET_PIXELS
        self.waterline_array: np.array = np.zeros(size, dtype=np.uint8)
        self.__generate_waterlines()
        self.__occupancy_grid: np.array = np.zeros(size, dtype=np.uint8)

    def get_vision(self, center: tuple[int, int], vision: int) -> np.array:
        """ Find the visible waterline points for bird consumption.

        center: tuple, (x, y) in pixels
        vision: int, distance in pixels

        returns: np.array, (x, y) in pixels, where the points are waterlines visible."""
        visible_locations = filter_locs(make_visible_locs(vision) + center, self.size)
        visible_space = self.waterline_array[visible_locations[:, 0], visible_locations[:, 1]]
        locations: np.array = visible_locations[np.argwhere(visible_space == 1)]
        if locations.size == 1:
            raise NeedNotFoundException
        return locations[:, 0, :]

    def get_resource(self, point: tuple[int, int]) -> float:
        """Get the resource at the given point.

        point: tuple, (x, y) in pixels

        returns: float, resource at the given point."""
        resource = self.waterline_array[point] * 100
        if resource == 100:
            print("drank water")
        return resource
