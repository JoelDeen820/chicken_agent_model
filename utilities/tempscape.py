
import numpy as np
from skimage.draw import disk

from utilities.chicken_utils import CENTIMETERS_PER_PIXEL, filter_locs, make_visible_locs
from utilities.need_not_availible import NeedNotFoundException

class TempScape:
    HEAT_RADIUS = 15 # meters 
    NUM_HEATERS = 4 
    DISTANCE_BETWEEN_HEATERS = 30 #meters
    X_PERMINITER_OFFSET = 1.0  # meters
    Y_PERMINITER_OFFSET = 0.03  # meters
    PIXELS_BETWEEN_HEATERS = int(DISTANCE_BETWEEN_HEATERS * 100 / CENTIMETERS_PER_PIXEL)
    HEAT_RADIUS_PIXELS = int(HEAT_RADIUS * 100 / CENTIMETERS_PER_PIXEL)
    PIXELS_BETWEEN_HEATERS = int(DISTANCE_BETWEEN_HEATERS * 100 / CENTIMETERS_PER_PIXEL)
    X_PERMINITER_OFFSET_PIXELS = int(X_PERMINITER_OFFSET * 100 / CENTIMETERS_PER_PIXEL)
    Y_PERMINITER_OFFSET_PIXELS = int(Y_PERMINITER_OFFSET * 100 / CENTIMETERS_PER_PIXEL)

    
    def __generate_tube_heater_distrobution(self, size: tuple) -> np.ndarray:
        pass


    def __draw_water_radius(self, points: list[tuple[int, int]]) -> None:
        """Draws the heat radius around the given points."""
        for x, y in points:
            rr, cc = disk((x, y), self.HEAT_RADIUS_PIXELS, shape=self.size)
            self.heater_array[rr, cc] = 1

    def __draw_points(self, points: list[tuple[int, int]]) -> None:
        """Draws the given points."""
        for x, y in points:
            self.waterline_array[x, y] = 1
    
    def __generate_heatmap(self, points=False) -> None:
        """Generate the waterlines."""
        heat_points = []
        for i in range(self.num_lines):
            for j in range(self.num_nipples):
                x = int(self.Y_PERMINITER_OFFSET_PIXELS + j * self.PIXELS_BETWEEN_HEATERS)
                y = int(self.X_PERMINITER_OFFSET_PIXELS + i * self.PIXELS_BETWEEN_HEATERS)
                heat_points.append((x, y))

        if points:
            self.__draw_points(heat_points)
        else:
            self.__draw_water_radius(heat_points)
    def __init__(self, size: tuple) -> None:
        """Initialize the TempScape object.

        size: tuple, (width, height) in pixels
        """
        self.size = size
        num_heaters: int = size[0] // self.PIXELS_BETWEEN_HEATERS
        self.num_heaters: int = int(num_heaters)
        self.heater_offset_y: int = self.Y_PERMINITER_OFFSET_PIXELS
        self.heater_array: np.array = np.zeros(size, dtype=np.uint8)
        self.__generate_heaters()
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

    def get_resource(self, point: tuple[int, int]) -> float:
        """Get the resource at the given point.

        point: tuple, (x, y) in pixels

        returns: float, resource at the given point."""
        resource = self.heater_array[point] * 100
        if resource == 100:
            print("warm up")
        return resource