
import numpy as np

CENTIMETERS_PER_PIXEL = 3.0


def filter_locs(locs: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    """Filters out the locs that are not in the given size."""
    return locs[np.logical_and(np.logical_and(locs[:, 0] >= 0, locs[:, 0] < size[0]),
                               np.logical_and(locs[:, 1] >= 0, locs[:, 1] < size[1]))]


def make_visible_locs(vision: int):
    """Computes the kernel of visible cells.

    vision: int distance
    """
    return np.argwhere(np.ones((vision, vision)))