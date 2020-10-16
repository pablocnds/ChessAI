import piece

import numpy as np


class Board:
    """
    Chess board.

    Width and height are 8x8 by default.

    Pieces attribute is None by default, which means regular starting pieces by the chess rules.
    A list of pieces can be given to start the game with those, but the number and positions must be the same as default.
    There is no comprobation to check if the pieces are legal which can result in bugs as default behaviour will try to be applied.

    There is a redundancy in the internal data representation as there are two different data structures holding references to the pieces.
    This data redundancy is done for optimization purposes due to the way methods can perform in the implementation.
    """
    def __init__(self,width=8,height=8,pieces=None):
        self.size = piece.Vec2(width, height)

        # Table object with the references to the pieces
        self.table = np.full((width,height),None)

        if pieces is None and (width, height) == (8,8):
            pcs = Board.starting_pieces()
            self.pieces = np.array(pcs)
            self.redo_table()
        else: self.pieces = np.array(pieces)

        # Turn 'W' for whites, 'B' for blacks
        self.playing = 'W'
        self.turn = 0
    
    @staticmethod
    def starting_pieces():
        """
        Returns a list of Piece objects with the starting positions as in the chess rules.
        """
        pcs = []
        # Whites
        pcs.append(piece.Piece(4,0,'K',True)) # King
        pcs.append(piece.Piece(3,0,'Q',True)) # Queen

        pcs.append(piece.Piece(2,0,'B',True)) # Bishops
        pcs.append(piece.Piece(5,0,'B',True))
        pcs.append(piece.Piece(1,0,'H',True)) # Knights
        pcs.append(piece.Piece(6,0,'H',True))
        pcs.append(piece.Piece(0,0,'T',True)) # Towers
        pcs.append(piece.Piece(7,0,'T',True))

        for i in range(8): pcs.append(piece.Piece(i,1,'P',True)) # Pawns

        # Blacks
        pcs.append(piece.Piece(4,7,'K',False)) # King
        pcs.append(piece.Piece(3,7,'Q',False)) # Queen

        pcs.append(piece.Piece(2,7,'B',False)) # Bishops
        pcs.append(piece.Piece(5,7,'B',False))
        pcs.append(piece.Piece(1,7,'H',False)) # Knights
        pcs.append(piece.Piece(6,7,'H',False))
        pcs.append(piece.Piece(0,7,'T',False)) # Towers
        pcs.append(piece.Piece(7,7,'T',False))

        for i in range(8): pcs.append(piece.Piece(i,6,'P',False)) # Pawns

        return pcs
    

    def redo_table(self):
        """
        This method completely updates the reference table from the list of pieces.
        """
        self.table = np.full(self.size.tup(),None)
        for p in self.pieces:
                self.table[p.pos.x,p.pos.y] = p


    def attempt_movement(self,from_coord,to_coord):
        """
        Returns True if the movement has been performed. Otherwise return False and the movement attempted is ilegal.
        If the movement is performed, the turn changes.

        from_coord and to_coord are tuples or Vec2 objects.
        """
        if type(from_coord) is tuple:
            from_coord = piece.Vec2(from_coord[0],from_coord[1])
        if type(to_coord) is tuple:
            to_coord = piece.Vec2(to_coord[0],to_coord[1])

        if not self.is_legal_movement(from_coord, to_coord):
            return False

        self.move_piece(from_coord,to_coord)

        self.turn += 1
        if self.playing == 'W': self.playing = 'B'
        else: self.playing = 'W'

        return True


    def is_legal_movement(self, from_coord, to_coord):
        """Checks if the coordinate to start move has a valid piece on turn"""
        if not self.is_in_boundaries(from_coord):
            return False
        if not self.is_piece_on_turn(from_coord):
            return False
        #TODO rules

        return True

    
    def is_piece_on_turn(self, coord):
        """Only returns true if there is a moveable piece in the coordinate given in the turn."""
        p = self.table[coord.tup()]
        if p is None:
            return False
        if p.is_whites() and self.playing == 'W':
            return True
        elif p.is_blacks() and self.playing == 'B':
            return True
        
        return False


    def move_piece(self, from_coord, to_coord):
        """
        Changes the position of a piece regardless of wheter its legal or not.
        If the coordinates of the piece are outside of the board, it is excluded from the table.

        Any movement in a piece INSIDE the table (to inside or outside) should be done using this method.

        from_coord and to_coord are Vec2 objects.
        """
        piece = self.table[from_coord.x,from_coord.y]
        self.table[from_coord.x,from_coord.y] = None
        piece.move(to_coord)
        if self.is_in_boundaries(to_coord):
            self.table[to_coord.x,to_coord.y] = piece
    

    def is_in_boundaries(self, coord):
        return not ((coord.x >= self.size.x) or (coord.y >= self.size.y) or (coord.x < 0) or (coord.y < 0))
    

    def kill_at(self, coord):
        """The given coordinate must be inside the table"""
        elem = self.table[coord.tup()]
        self.table[coord.tup()] = None
        elem.kill()


    def to_string(self):
        """
        Returns a string with a simple representation of the board.
        Uppercase for whites, lowercase for blacks.
        """
        sd = "Dead=["
        for e in self.pieces:
            if not e.is_alive == True:
                sd += e.piece_type + '|'
        s = '  1 2 3 4 5 6 7 8\n'
        for y in range(self.table.shape[0]):
            s += chr(ord('A')+y) + " "
            for x in range(self.table.shape[1]):
                elem = self.table[y,x]
                if elem is None:
                    s += "_|"
                else:
                    if elem.is_whites():
                        s += elem.piece_type + "|"
                    else:
                        s += elem.piece_type.lower() + "|"
            s += '\n'
        
        return ''.join(s) + sd + "]"
    