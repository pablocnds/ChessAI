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
    def __init__(self,width=8,height=8,pieces=None,silent=False):
        self.size = piece.Vec2(width, height)

        # Table object with the references to the pieces
        self.table = np.full((width,height),None)

        if pieces is None and (width, height) == (8,8):
            pcs = Board.starting_pieces()
            self.pieces = np.array(pcs)
            self.redo_table()
        else: self.pieces = np.array(pieces)

        self.silent = silent
        self.playing = 'W'      # Playing 'W' for whites, 'B' for blacks
        self.turn = 0
        self.is_check = False
        self.forward = piece.Vec2(0,1)
    
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

        #TODO piece capture

        self.move_piece(from_coord,to_coord)

        #TODO is check / checkmate

        self.turn += 1
        self.forward.y *= -1
        if self.playing == 'W': self.playing = 'B'
        else: self.playing = 'W'

        return True


    def is_legal_movement(self, from_coord, to_coord):
        """Checks if the coordinate to start move has a valid piece on turn"""
        if not self.is_in_boundaries(from_coord):
            if not self.silent: print("Invalid move: This move is outside the boundaries!")
            return False
        if not self.is_piece_on_turn(from_coord):
            if not self.silent: print("Invalid move: Wrong turn!")
            return False
        if from_coord == to_coord:
            if not self.silent: print("Invalid move: Can't move to the same square!")
            return False
        if not self.is_valid_piece_movement(from_coord, to_coord):
            if not self.silent: print("Ilegal move: This piece can't do that!")
            return False
        # TODO
        #if not self.check_misc_rules(from_coord, to_coord):
            #if not self.silent: print("Ilegal move: This move can't be done.")
            #return False

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
    

    def is_valid_piece_movement(self, from_coord, to_coord):
        """Returns True if the movement can be done with the specific piece and is in boundaries."""
        if not self.is_in_boundaries(to_coord):
            return False
        
        p = self.get_piece_at(from_coord)
        if self.get_piece_at(to_coord) is not None:
            if self.get_piece_at(to_coord).team == p.team:  # Moving to a same team piece
                # TODO check if its castling
                return False

        movement = to_coord - from_coord
        piece_type = p.piece_type
        
        # BISHOP
        if piece_type == 'B':
            return (abs(movement.x) == abs(movement.y) and 
                self.check_in_path(from_coord, piece.Vec2(movement.x/abs(movement.x), movement.y/abs(movement.x)), abs(movement.x)))
        
        # KNIGHT
        if piece_type == 'H':
            absolute = piece.Vec2(abs(movement.x), abs(movement.y))
            return ((absolute.x == 1 or absolute.x == 2)
                and (absolute.y == 1 or absolute.y == 2)
                and (absolute.x != absolute.y))
        
        # ROOK
        if piece_type == 'T':
            absolute = piece.Vec2(abs(movement.x), abs(movement.y))
            leng = movement.x + movement.y
            unit = piece.Vec2(movement.x/movement.x,0) if movement.x != 0 else piece.Vec2(0,movement.y/movement.y)
            if ((absolute.x == 0 or absolute.y == 0)
                and (absolute.x > 0 or absolute.y > 0)):
                length = absolute.x + absolute.y
                step = piece.Vec2(movement.x/length,movement.y/length)
                return self.check_in_path(from_coord, step, length)
        
        # QUEEN
        if piece_type == 'Q':
            absolute = piece.Vec2(abs(movement.x), abs(movement.y))
            if absolute.x == absolute.y:
                return self.check_in_path(from_coord, piece.Vec2(movement.x/absolute.x, movement.y/absolute.x), absolute.x)
            elif ((absolute.x == 0 or absolute.y == 0) and (absolute.x > 0 or absolute.y > 0)):
                length = absolute.x + absolute.y
                step = piece.Vec2(movement.x/length,movement.y/length)
                return self.check_in_path(from_coord, step, length)

        # KING
        if piece_type == 'K':
            absolute = piece.Vec2(abs(movement.x), abs(movement.y))
            return (absolute.x + absolute.y == 1) or (absolute.x == 1 and absolute.y == 1)
            #TODO Check castling
        
        # PAWN
        if piece_type == 'P':
            if movement == self.forward:    # 1 forward move
                return self.get_piece_at(to_coord) is None

            elif movement.y == self.forward.y and abs(movement.x) == 1: # Diagonal capture movement
                return self.get_piece_at(to_coord) is not None

            elif movement == (self.forward * 2):    # 2 forward initial move
                return (((p.is_whites() and from_coord.y == 1)
                    or (p.is_blacks() and from_coord.y == self.size.y - 2))
                    and self.get_piece_at(to_coord) is None)
            
            #TODO check "en passant" case

            else: return False
        
        return False
    

    def check_in_path(self, start, vec_step, num_steps):
        """Given a start, a step vector and a number of steps, returns True if there is no piece in the calculated path"""
        print("Trying " + str(start) + " using " + str(vec_step) + " " + str(num_steps) + " times")
        current = start
        for i in range(1, num_steps):
            current += vec_step
            if self.get_piece_at(current) is not None:
                return False
        return True

    
    def get_piece_at(self, coord):
        """*coord*: can be a tuple or a Vec2"""
        if type(coord) is tuple: return self.table[coord]
        return self.table[coord.tup()]


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
    