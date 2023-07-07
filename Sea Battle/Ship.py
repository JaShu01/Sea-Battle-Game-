import Coordinate

from func import *

class Ship:
    def __init__(self, type):
        self.name = type[0]  # Definition der Eigenschaften eines Schiffes
        self.length = type[1]
        self.code = type[2]
        self.orientation = None
        self.koords = []
        self.hits = 0

    def place(self, start_xachse, start_yachse, orientation):
        self.koords = []
        self.hits = 0
        # alle Koordinaten hinzufügen
        if orientation in horizontal:
            for x in range(self.length):
                self.koords.append(Coordinate(start_xachse + x, start_yachse))
        elif orientation in vertical:
            for y in range(self.length):
                self.koords.append(Coordinate(start_xachse, start_yachse + y))

    def is_destroyed(self):  # Definitoon des Destoryeds Boards
        return self.hits == self.length
