import math

class Vector():
    """if empty it will be 0,0, use Vector(x,y) or Vector((x,y))"""
    def __init__(self, *args):
        self.x, self.y = 0,0
        if len(args) == 0:
            pass
        elif len(args) == 1:
            self.x, self.y = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            raise ValueError("expected no more than 2 arguments")

    def xy(self):
        return (self.x, self.y)

    def distance(self, other: Vector):
        return math.sqrt(abs((self.x - other.x)**2 + (self.y - other.y)**2))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)


    def __str__(self):
        return f"({self.x}, {self.y})"