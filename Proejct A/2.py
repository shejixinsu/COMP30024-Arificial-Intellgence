"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
Shizhan Xu 771900
Shangqian Li 908462
"""

import sys
import json


def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    
    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)

def find_exit(colour):
    if colour=="red":
        return [[3,-3],[3,-2],[3,-1],[3,0]]
    elif colour=="green":
        return [[-3,3],[-2,3],[-1,3],[0,3]]
    else:
        return [[0,-3],[1,-3],[2,-3],[3,-3]]
    


def iterative_deepening_search(initial,exits,blocks,MAX_DEPTH):
    for depth_limit in range(MAX_DEPTH):
        track=depth_limit_search(initial,exits,blocks,depth_limit)
        if not (track is None):
            break
    return track

def depth_limit_search(initial,exits,blocks,depth_limit):
    depth=0
    pieces=initial
    track=[]
    stack=child_nodes(pieces,blocks,exits)
    while stack:
        current=stack.pop()
        track.append(current)
        if not (current is None) and len(current)==1:
            pieces.remove(current[0])
            depth+=1
            if len(pieces)==0:
                return track
            continue
        # a None is used as a sentinel to the last node in one depth level
        elif current is None:
            # first pop None, then pop the wrong choice of node and restore this move
            track.pop()
            last_move=track.pop()
            pieces=make_move([last_move[1],last_move[0]], pieces)
            depth-=1
            continue
        elif depth==depth_limit:
            track.pop()
            continue
        else:
            # add a sentinel for the end of this depth
            stack.append(None)
            pieces=make_move(current,pieces)
            stack+=child_nodes(pieces,blocks,exits);
            depth+=1
    return None
"""
passed unit test
return all the possible next move from the current coordinate, considering blocks
"""
def child_nodes(pieces,blocks,exits):
    moves=[]
    for piece in pieces:
        if piece in exits:
            moves.append([piece])
            continue
        for node in surrounding(piece):
            if (node not in blocks) and (node not in pieces) and in_board(node):
                moves.append([piece,node])
            elif (node in blocks or node in pieces) and (jump_to(piece,node) not in blocks) and (jump_to(piece,node) not in pieces) and in_board(jump_to(piece,node)):
                moves.append([piece,jump_to(piece,node)])
    return moves
    
def make_move(current,pieces):
    new=pieces
    for i in range(len(new)):
        if pieces[i]==current[0]:
            pieces[i]=current[1]
            break
    return new

"""
passed unit test
return if the coordinate is within the board
"""
def in_board(coor):
    if (coor[0]==-3 and coor[1] in range(0,4))\
        or (coor[0]==-2 and coor[1] in range (-1,4))\
        or (coor[0]==-1 and coor[1] in range (-2,4))\
        or (coor[0]==0 and coor[1] in range (-3,4))\
        or (coor[0]==1 and coor[1] in range (-3,3))\
        or (coor[0]==2 and coor[1] in range (-3,2))\
        or (coor[0]==3 and coor[1] in range (-3,1)):
        return True
    return False

"""
passed united test
return the 6 coordinates that surrounds the given one
"""
def surrounding(coor):
    top_left=[coor[0],coor[1]-1]
    top_right=[coor[0]+1,coor[1]-1]
    left=[coor[0]-1,coor[1]]
    right=[coor[0]+1,coor[1]]
    bot_left=[coor[0]-1,coor[1]+1]
    bot_right=[coor[0],coor[1]+1]
    return [top_left,top_right,left,right,bot_left,bot_right]
    
"""
passed united test
return the destination of a jump
"""
def jump_to(current,jump):
    return [jump[0]+jump[0]-current[0],jump[1]+jump[1]-current[1]]

def print_result(track):
    for move in track:
        if len(move)==1:
            print("EXIT from (%d, %d)." % (move[0][0], move[0][1]))
            continue
        elif move[1] in surrounding(move[0]):
            print("MOVE from (%d, %d) to (%d, %d)." % (move[0][0], move[0][1], move[1][0], move[1][1]))
        else:
            print("JUMP from (%d, %d) to (%d, %d)." % (move[0][0], move[0][1], move[1][0], move[1][1]))
            
def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    exits=find_exit(data[0].get("colour"))
    pieces=data[0]["pieces"]
    blocks=data[0]["blocks"]
    MAX_DEPTH=37*len(pieces)
    track=iterative_deepening_search(pieces, exits, blocks,MAX_DEPTH)
    print_result(track)
    file.close()

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()