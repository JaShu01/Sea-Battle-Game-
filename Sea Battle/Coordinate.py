

class Coordinate:
    def __init__(self, x_achse, y_achse):  #  Koordinatenparameter festlegen
        self.x = x_achse
        self.y = y_achse

    def left(self):
        return Coordinate(self.x - 1, self.y)

    def right(self):
        return Coordinate(self.x + 1, self.y)

    def up(self):
        return Coordinate(self.x, self.y - 1)

    def down(self):
        return Coordinate(self.x, self.y + 1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"