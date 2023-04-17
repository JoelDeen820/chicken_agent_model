from utilities.chicken import ChickenNeed


class NeedNotFoundException(Exception):
    def __init__(self, need: ChickenNeed):
        self.need = need

    def __str__(self):
        return "Need not found: {}".format(self.need)
