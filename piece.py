class Coord:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
class Piece(ABC):
    def __init__(self, x, y, is_whites):
        self.pos = Coord(x,y)
        self.is_alive = True

        if is_whites: self.team = 0
        else: self.team = 1
    
    def is_whites():
        return self.team == 0
    
    def is_blacks():
        return self.team == 1

    def kill():
        self.pos = Coord(-1,-1)
        self.is_alive = False
    
    def revive_to(coord):
        self.pos = coord.copy()
        self.is_alive = True

    def move(self,coord):
        self.pos = coord.copy()
