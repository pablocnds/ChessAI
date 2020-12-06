# ChessAI

Work in progress implementation of **chess for AI / ML**. 

By default it only simulates the moves without displaying them in order to boost the performance during the AI training, but the board state can be shown using the to_string method which will output a string representation of the board with its pieces.

The implementation is focused on keeping an abstracted code structure, but performance is also taken into account.

This is a **personal project** for learning and demonstration purposes and doesn't stand out from other chess simulators, but I've put the code under a MIT license in case someone wants to use it.


## How Testing is done

To have an easy and quick testing phase in such a complex game, many instances of **real games are downloaded, encoded and simulated** with this program. Then, if an error pops up during the simulation of one game or the final game state is unexpected, the error is tracked and fixed in case of it being a bug. This method has its flaws, but is sufficient for the scope of this project.


## How to implement an AI and get the Game State

To implement an AI working in this simulator, it can be done in a new module using the game state from the *board.py* module. See the *game.py* module as an example of manual play.

The game runs in the *board.Board* object. There are two easy ways of getting the game state:
- Use *board_object.get_pieces()* to get a numpy array of references of all the piece objects with its corresponding coordinates, piece type and state. If a piece is dead, it will be represented in its *is_alive* variable, and will be positioned in the (-1, -1) coordinate.
- Use *board_object.get_table()* to get a reference of the numpy array with dimensions 8 by 8 with all the squares in the board. This squares can contain a None reference, or a piece object.

Note that **this methods return references of objects** and modifying those objects will directly alter the game state in an unintended way. To train a ML algorithm, extracting/copying the information from these references is generally recomended.

To perform an action, use the method *board_object.attempt_movement(from_coord, to_coord)* using tuples or *Vec2* objects as coordinates. The method will return False if the movement is illegal or impossible.