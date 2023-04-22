from enum import Enum
from math import pi

import numpy as np

from utilities.chicken_utils import CENTIMETERS_PER_PIXEL


def generate_random_angle() -> float:
    """Generates a random angle that is uniform in radians."""
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

    def __init__(self, loc: tuple[int, int]) -> None:
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
        """ Sets the need of the chicken based on its current state.

        """
        if self.thirst < self.THIRST_TRIGGER:
            self.need = ChickenNeed.THIRST
        elif self.hunger < 0:
            self.need = ChickenNeed.HUNGER
        elif self.temperature < Chicken.IDEAL_MIN_TEMP or self.temperature > Chicken.IDEAL_MAX_TEMP:
            self.need = ChickenNeed.TEMPERATURE
        else:
            self.need = ChickenNeed.HAPPY

    def __evaluate_thirst(self, env) -> None:
        """ Sets the need of the chicken based on its current state.

        """
        thirst_addition = 0
        if self.need == ChickenNeed.THIRST:
            thirst_addition = env.waterlines.get_resource(self.loc)
        self.thirst += thirst_addition - Chicken.THIRST_DECAY
        if thirst_addition != 0:
            self.search_angle = generate_random_angle()

    def __evaluate_hunger(self, env) -> None:
        """ Gets the bird to eat and evaluate hunger"""

        hunger_addition = 0
        if self.need == ChickenNeed.HUNGER:
            hunger_addition = env.feedlines.get_resource(self.loc)
        self.hunger += hunger_addition - Chicken.HUNGER_DECAY
        if hunger_addition != 0:
            self.search_angle = generate_random_angle()

    def step(self, env) -> None:
        """Look around, move, and harvest.

        env: Barn
        """
        thirst_addition = 0
        self.__evaluate_need()
        self.loc = env.look_and_move(self.loc, self.vision, self.need, generate_random_angle())
        self.__evaluate_thirst(env)
        self.__evaluate_hunger(env)
        # self.temperature += env.temp(self.loc)
