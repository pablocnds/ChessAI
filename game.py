import board

def mov_to_coord(movement):
    if type(movement) is not str or len(movement) != 2:
        return None
    
    y = int(movement[1]) - 1
    x = ord(movement[0].upper()) - ord('A')

    if x<0 or x>7 or y<0 or y>7:
        print(x,y)
        return None
    
    return (x,y)


game = board.Board()
print(game.to_string() + "\n")

action = ""
while action != "exit":
    print("Chose a move: ")
    action = raw_input()
    
    if action == "exit":
        continue
    if len(action) != 8:
        print(len(action))
        print("Wrong input. Use the correct format or \"exit\":\n\tExample: \"2C -> 3C\"\n")
        continue
    
    c1 = mov_to_coord(action[:2])
    c2 = mov_to_coord(action[6:])
    if c1 is None or c2 is None:
        print("Wrong input. Use the correct format or \"exit\":\n\tExample: \"2C -> 3C\"\n")
        continue

    if game.attempt_movement(c1,c2) is False:
        print("Invalid move!\n")
        continue

    print(game.to_string() + "\n")
