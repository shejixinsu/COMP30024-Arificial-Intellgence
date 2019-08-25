"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
Shizhan Xu 771900
Shangqian Li 908462
"""

import sys
import json
## the maximum depth we can have is defined as the number of places on the board
MAX_DEPTH=37


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

# function to find the exit path for each color
def find_exit(colour):
    if colour=="red":
        return [[3,-3],[3,-2],[3,-1],[3,0]]
    elif colour=="green":
        return [[-3,3],[-2,3],[-1,3],[0,3]]
    else:
        return [[0,-3],[1,-3],[2,-3],[3,-3]]
    

# the function to present iterative deepening search
def iterative_deepening_search(initial,exits,blocks):
    
# within depth below max_depth, iterate to find the path
    for depth_limit in range(MAX_DEPTH):
        track=depth_limit_search(initial,exits,blocks,depth_limit)
        #stop looping if search find a path to the exit
        if not (track is None):
            break
    return track
# function for searching
def depth_limit_search(initial,exits,blocks,depth_limit):
    depth=0
    track=[]
    stack=[initial]
    visited=[]
    while stack:
        current=stack.pop()
        track.append(current)
        visited.append(current)
        if current in exits:
            return track
        # a None is used as a sentinel to the last node in one depth level
        elif current is None:
            # first pop None, then pop the wrong choice of node
            track.pop()
            track.pop()
            visited.pop()
            depth-=1
            continue
        elif depth==depth_limit:
            track.pop()
            continue
        else:
            # add a sentinel for the end of this depth
            stack.append(None)
            stack+=child_nodes(current,blocks,visited);
            depth+=1
    return None
"""
passed unit test
return all the possible next move from the current coordinate, considering blocks
"""
def child_nodes(current,blocks,visited):
    nodes=[]
    for node in surrounding(current):
        if (node not in blocks) and (node not in visited) and in_board(node):
            nodes.append(node)
        elif (node in blocks) and (jump_to(current,node) not in blocks) and (jump_to(current,node) not in visited) and in_board(jump_to(current,node)):
            nodes.append(jump_to(current,node))
    return nodes
    
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

def print_result(route,exits):
    for i in range(len(route)):
        if route[i] in exits:
            print("EXIT from (%d, %d)." % (route[i][0], route[i][1]))
            continue
        elif route[i+1] in surrounding(route[i]):
            print("MOVE from (%d, %d) to (%d, %d)." % (route[i][0], route[i][1], route[i+1][0], route[i+1][1]))
        else:
            print("JUMP from (%d, %d) to (%d, %d)." % (route[i][0], route[i][1], route[i+1][0], route[i+1][1]))
            
def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    exits=find_exit(data[0].get("colour"))
    route=[]
    blocks=data[0]["blocks"].copy()
    no_path=[]
    
    for piece in data[0]["pieces"]:
        blocks.append(piece)
    for piece in data[0]["pieces"]:
        routes=iterative_deepening_search(piece,exits,blocks)
        if routes is not None:
            route+=routes
            blocks.remove(piece)
        else:
            no_path.append(piece)
    for piece in no_path:
        routes=iterative_deepening_search(piece,exits,blocks)
        if routes is not None:
            route+=routes
            blocks.remove(piece)
            
    print_result(route,exits)
    file.close()

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()