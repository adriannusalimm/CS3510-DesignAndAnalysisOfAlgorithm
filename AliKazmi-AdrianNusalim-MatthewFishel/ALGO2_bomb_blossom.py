import sys
import json
import random
from queue import PriorityQueue
import datetime

"""
Helper Functions
"""
def priority(num):
    return -1 * num


def squareVal(board, coord):
    return board[coord[1]][coord[0]]


def getNeighbors(board, cur):
    x_width = len(board[0])
    y_height = len(board)
    neighbors = []
    row = cur[0]
    col = cur[1]

    for j in range(3):
        j_prime = j - 1
        if col + j_prime >= 0 and col + j_prime < y_height:
            for i in range(3):
                i_prime = i - 1
                if row + i_prime >= 0 and row + i_prime < x_width:
                    if i_prime == 0 and j_prime == 0:
                        continue
                    else:
                        u = (row + i_prime, col + j_prime)
                        if u[0] >= 0 and u[0] < x_width and u[1] >= 0 and u[1] < y_height:
                            neighbors.append(u)
    return neighbors		

def getPriorityElem(board, coord):
    val = priority(squareVal(board, coord))
    elem = (val, coord)
    return elem

def pickRandom(square_set):
    if len(square_set) == 0:
        return None
    square_list = list(square_set)
    rand_index = random.randrange(len(square_set))
    return square_list[rand_index]


"""
initializations
"""

filename = sys.argv[1]

try:
    fullbool=int(sys.argv[2])
except: 
    fullbool=0 
#if fullbool=1, full output. If not, output for our graphs (csv)

if(fullbool==1):
        print(filename)

with open(filename, 'r') as file:
    file_json = file.read()

# game state initializations
real_bomb_set = set()
boardState = []
x_dim = None
y_dim = None
safe_square = None
num_bombs = None

"""
code for parsing input JSON into ints, tuples, etc. sets boardState[]
"""
initial_state = json.loads(file_json)
if(fullbool==1): 
	print("\ninput data:")
	print(initial_state)

dimensions = initial_state['dim'].split(',', 10)
x_dim = int(dimensions[0])
y_dim = int(dimensions[1])
all_squares_set = set()

for j in range(y_dim):
    start_index = j*x_dim
    end_index = j*x_dim + x_dim
    row_string = initial_state['board'][start_index:end_index]
    row_list = []
    for i in range(len(row_string)):
        square_val = int(row_string[i])
        row_list.append(square_val)
        coord = (i, j)
        all_squares_set.add(coord)
        if square_val == 9:
            bomb_coord = (i, j)
            real_bomb_set.add(bomb_coord)
    boardState.append(row_list)

num_bombs = int(initial_state['bombs'])
safe_xy = initial_state['safe'].split(',', 10)
safe_x = int(safe_xy[0])
safe_y = int(safe_xy[1])
safe_square = (safe_x, safe_y)

"""
find bombs
"""
dig_count_total = 0
delta_total = 0

for i in range(5):
    startTime = datetime.datetime.now()

    dig_count = 1
    found_bombs_set = set()
    explored_set = set()  # these are squares that have been 'dug'
    expanded_set = set()  # these are squares that have had their neighbors added to the priority queue
    explored_set.add(safe_square)
    num_squares = x_dim * y_dim

    q = PriorityQueue()
    q.put(getPriorityElem(boardState, safe_square))

    while dig_count < num_squares:
        if len(found_bombs_set) == num_bombs:
            # terminate and give results
            break
        elif q.empty():
            # pick random to add to q, just in case there is nothing in the q.
            # note, this only happens when a square has *only* bomb neighbors. Fairly rare.
            random_square = pickRandom(all_squares_set.difference(explored_set))
            explored_set.add(random_square)
            dig_count += 1
            elem = getPriorityElem(boardState, random_square)
            q.put(elem)
        else:
            # run the algo.
            cur = q.get()[1]
            if cur in expanded_set:
                continue
            allNeighbors = getNeighbors(boardState, cur)
            for neighbor in allNeighbors:
                # if bomb
                if neighbor not in explored_set:
                    explored_set.add(neighbor)
                    dig_count += 1
                if squareVal(boardState, neighbor) == 9:
                    if neighbor not in found_bombs_set:
                        found_bombs_set.add(neighbor)
                else:
                    # not bomb
                    if neighbor in expanded_set:
                        continue
                    else:
                        elem = getPriorityElem(boardState, neighbor)
                        q.put(elem)
            expanded_set.add(cur)
    endTime = datetime.datetime.now()

    delta = int ((endTime - startTime).total_seconds() * 1000)
    dig_count_total += dig_count
    delta_total += delta

if fullbool==1:
    print("\n\nRESULTS:\n")
    print('squares: {}'.format(num_squares))
    print('average digs: {}'.format(dig_count_total/5.0))
    print("found bombs:")
    print(found_bombs_set)
    print("real bombs:")
    print(real_bomb_set)
    mismatches = 0
    for bomb in found_bombs_set:
        if bomb not in real_bomb_set:
            mismatches += 1
    print('wrong bombs: {} of {}'.format(mismatches, len(real_bomb_set)))
    #for parsing
if fullbool==0:
    print(str(num_squares)+' '+str(dig_count_total/5.0)+' '+str(num_bombs)+' '+str(delta_total/5.0))







