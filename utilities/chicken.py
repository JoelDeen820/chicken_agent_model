
class Chicken:

    IDEAL_TEMP = 20

    def __init__(self, loc, params):
        """Creates a Chicken, which is hungary, thirsty and sensitive to temperature

        loc: tuple coordinates
        params: dictionary of parameters
        """

        self.loc = tuple(loc)
        self.thirst = 0
        self.hunger = 0
        self.temperature = Chicken.IDEAL_TEMP

        self.vision = 1.0
