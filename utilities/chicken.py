from enum import Enum
from math import pi, sin, cos
from random import random

import numpy as np

from utilities.chicken_utils import CENTIMETERS_PER_PIXEL

def generate_random_angle():
    return np.random.random() * 2 * pi - pi

class ChickenNeed(Enum):
    HAPPY = 0
    THIRST = 1
    HUNGER = 2
    TEMPERATURE = 3

class Chicken:
    BASE_HUNGER = 25
    AVG_THIRST = 75
    STD_THIRST = 10
    THIRST_TRIGGER = 50

    IDEAL_MAX_TEMP = 25
    IDEAL_MIN_TEMP = 20

    THIRST_DECAY = 1
    HUNGER_DECAY = 1

    BIRD_VISION = int(33 // CENTIMETERS_PER_PIXEL)
    BIRD_VISION_DEVIATION = 1

    def __init__(self, loc):
        """Creates a Chicken, which is hungary, thirsty and sensitive to temperature

        loc: tuple coordinates
        """

        self.loc = tuple(loc)
        self.thirst = int(np.random.normal(self.AVG_THIRST, self.STD_THIRST))
        self.hunger = 25
        self.temperature = np.random.randint(Chicken.IDEAL_MIN_TEMP, Chicken.IDEAL_MAX_TEMP)
        self.search_angle = generate_random_angle()
        self.need = ChickenNeed.HAPPY

        self.vision = self.BIRD_VISION



    def __evaluate_need(self) -> None:
        """Returns the need of the chicken

        """
        if self.thirst < self.THIRST_TRIGGER:
            self.need = ChickenNeed.THIRST
        elif self.hunger < 0:
            self.need = ChickenNeed.HUNGER
        elif self.temperature < Chicken.IDEAL_MIN_TEMP or self.temperature > Chicken.IDEAL_MAX_TEMP:
            self.need = ChickenNeed.TEMPERATURE
        else:
            self.need = ChickenNeed.HAPPY

    def step(self, env):
        """Look around, move, and harvest.

        env: Barn
        """
        thirst_addition = 0
        self.__evaluate_need()
        self.loc = env.look_and_move(self.loc, self.vision, self.need, self.search_angle)
        if self.need == ChickenNeed.THIRST:
            thirst_addition = env.waterlines.get_resource(self.loc)
        self.thirst += thirst_addition - Chicken.THIRST_DECAY
        if thirst_addition != 0:
            self.search_angle = generate_random_angle()
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
