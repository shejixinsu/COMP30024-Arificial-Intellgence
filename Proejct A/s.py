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


def find_exit(colour):
    if colour=="red":
        return [[3,-3],[3,-2],[3,-1],[3,0]]
    elif colour=="green":
        return [[-3,3],[-2,3],[-1,3],[0,3]]
    else:
        return [[0,-3],[1,-3],[2,-3],[3,-3]]
    


def iterative_deepening_search(initial,exits,blocks,pieces):
    for depth_limit in range(MAX_DEPTH):
        track=depth_limit_search(initial,exits,blocks,depth_limit,pieces)
        if not (track is None):
            break
    return track

def depth_limit_search(initial,exits,blocks,depth_limit,pieces):
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
            stack+=child_nodes(current,blocks,visited,pieces);
            depth+=1
    return None
"""
passed unit test
return all the possible next move from the current coordinate, considering blocks
"""
def child_nodes(current,blocks,visited,pieces):
    nodes=[]
    for node in surrounding(current):
        if (node not in blocks) and (node not in visited) and (node not in pieces) and in_board(node):
            nodes.append(node)
        elif (node in blocks) and (jump_to(current,node) not in blocks) and (jump_to(current,node) not in visited) and (jump_to(current,node) not in pieces) and (node in pieces)and in_board(jump_to(current,node)):
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
    pieces2=data[0]["pieces"].copy()
    for piece in data[0]["pieces"]:
        print("aaa")
        routes=iterative_deepening_search(piece,exits,data[0]["blocks"],pieces2)
        if routes is not None:
            route+=routes
        pieces2.pop(0)
    print_result(route,exits)
    file.close()

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()