class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def tup(self):
        return (self.x,self.y)
    def copy(self):
        return Vec2(self.x,self.y)
    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)
    def __sub__(self, o):
        return Vec2(self.x - o.x, self.y - o.y)
    def __mul__(self, o):
        if type(o) is int:
            return Vec2(self.x * o, self.y * o)
        return Vec2(self.x * o.x, self.y - o.y)
    def __div__(self, o):
        return Vec2(self.x / o.x, self.y / o.y)
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y
    def __abs__(self, o):
        return Vec2(abs(self.x), abs(self.y))
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
class Piece:
    """
    Contains the basic information and methods to define a piece.
    The methods don't check if the actions are legal.

    piece_type should be 'P'(pawn), 'R'(rook), 'H'(horse/knight), 'B'(Bishop), 'Q'(Queen) or 'K'(King)
    """
    def __init__(self, x, y, piece_type, is_whites):
        self.pos = Vec2(x,y)
        self.is_alive = True
        self.piece_type = piece_type

        if is_whites: self.team = 0
        else: self.team = 1
    
    def is_whites(self):
        return self.team == 0
    
    def is_blacks(self):
        return self.team == 1

    def kill(self):
        self.pos = Vec2(-1,-1)
        self.is_alive = False
    
    def revive_to(self, coord):
        self.pos = coord.copy()
        self.is_alive = True

    def move(self,coord):
        """
        Move the piece to the indicated coordinates without checking if the move is legal.

        The coord must be a Vec2 element.
        """
        self.pos = coord.copy()
