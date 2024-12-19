class IntVector2:
    def __init__(self, x: float | int = 0, y: float | int = 0):
        self.x: int = int(x)
        self.y: int = int(y)


    def __add__(self, other):
        if isinstance(other, IntVector2):
            return IntVector2(self.x + other.x, self.y + other.y)
        raise TypeError("Unsupported operand type(s)")


    def __sub__(self, other):
        if isinstance(other, IntVector2):
            return IntVector2(self.x - other.x, self.y - other.y)
        raise TypeError("Unsupported operand type(s)")


    def __repr__(self):
        return f"IntVector2({self.x}, {self.y})"
