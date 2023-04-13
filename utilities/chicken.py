from enum import Enum
from math import pi, sin, cos
from random import random

import numpy as np


class ChickenNeed(Enum):
    HAPPY = 0
    THIRST = 1
    HUNGER = 2
    TEMPERATURE = 3


class Chicken:
    BASE_HUNGER = 25
    BASE_THIRST = 100

    IDEAL_MAX_TEMP = 20
    IDEAL_MIN_TEMP = 25

    THIRST_DECAY = 1
    HUNGER_DECAY = 1

    BIRD_VISION = 7
    BIRD_VISION_DEVIATION = 1

    def __init__(self, loc):
        """Creates a Chicken, which is hungary, thirsty and sensitive to temperature

        loc: tuple coordinates
        """

        self.loc = tuple(loc)
        self.thirst = 100
        self.hunger = 25
        self.temperature = np.random.randint(Chicken.IDEAL_MIN_TEMP, Chicken.IDEAL_MAX_TEMP)
        self.search_angle = np.nan

        self.vision = self.BIRD_VISION * np.random.randint(0, 3) - self.BIRD_VISION_DEVIATION

    def step(self, env):
        """Look around, move, and harvest.

        env: Barn
        """
        self.loc = env.look_and_move(self.loc, self.vision)
        self.thirst += env.waterlines.get_resource(self.loc) - Chicken.THIRST_DECAY
        # self.hunger += env.eat(self.loc)
        # self.temperature += env.temp(self.loc)

    def search_for_resource(self, env) -> tuple[int, int]:
        """Searches for a resource in the barn

        env: Barn
        """
        if np.isnan(self.search_angle):
            self.search_angle = random() * 2 * pi
        else:
            self.search_angle += (random() - 0.5) * pi / 2
        target_point = (self.loc[0] + self.vision * cos(self.search_angle),
                        self.loc[1] + self.vision * sin(self.search_angle))

        return target_point
