import sys
import json
import random
from queue import PriorityQueue
import datetime

"""
Helper Functions
"""


def getPriorityElem(board, coord):
    priority = squareVal(board, coord)
    elem = (priority, coord)
    return elem


def squareVal(board, coord):
    return board[coord[1]][coord[0]]


def getNeighbors(board, coord):
    x_width = len(board[0])
    y_height = len(board)
    neighbors = []
    row = coord[0]
    col = coord[1]

    for j in range(3):
        j_prime = j - 1
        if 0 <= col + j_prime < y_height:
            for i in range(3):
                i_prime = i - 1
                if 0 <= row + i_prime < x_width:
                    if i_prime == 0 and j_prime == 0:
                        continue
                    else:
                        u = (row + i_prime, col + j_prime)
                        if 0 <= u[0] < x_width and 0 <= u[1] < y_height:
                            neighbors.append(u)
    return neighbors


def pickRandom(square_set):
    if len(square_set) == 0:
        return None
    square_list = list(square_set)
    rand_index = random.randrange(len(square_set))
    return square_list[rand_index]


def pickStart(board, unexplored):
    zeroes = set()
    for coord in unexplored:
        if squareVal(board, coord) == 0:
            zeroes.add(coord)
    if len(zeroes) == 0:
        return None
    zeroes_list = list(zeroes)
    rand_index = random.randrange(len(zeroes))
    return zeroes_list[rand_index]


"""
initializations
"""

filename = sys.argv[1]

try:
    fullbool = int(sys.argv[2])
except:
    fullbool = 0
# if fullbool=1, full output. If not, output for our graphs (csv)

if fullbool == 1:
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
if (fullbool == 1):
    print("\ninput data:")
    print(initial_state)

dimensions = initial_state['dim'].split(',', 10)
x_dim = int(dimensions[0])
y_dim = int(dimensions[1])

for j in range(y_dim):
    start_index = j * x_dim
    end_index = j * x_dim + x_dim
    row_string = initial_state['board'][start_index:end_index]
    row_list = []
    for i in range(len(row_string)):
        square_val = int(row_string[i])
        row_list.append(square_val)
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
    # start time
    startTime = datetime.datetime.now()
    # 

    dig_count = 1
    guess_count = 0
    stepped_on_bombs = 0
    found_bombs_set = set()
    unexplored_set = set()  # initialized to all squares but starter square
    for j in range(y_dim):
        for i in range(x_dim):
            square = (i, j)
            if square != safe_square:
                unexplored_set.add(square)
    dug_set = set()  # these are squares that have been 'dug'
    expanded_set = set()  # these are squares that have had their neighbors added to the priority queue

    dug_set.add(safe_square)
    num_squares = x_dim * y_dim

    q = PriorityQueue()
    q.put(getPriorityElem(boardState, safe_square))


    while dig_count < num_squares:
        if len(found_bombs_set) == num_bombs:
            # terminate and give results
            break
        elif q.empty():
            # pick a random square from unexplored to dig if the q is empty
            random_square = pickRandom(unexplored_set)
            if random_square is not None:
                if squareVal(boardState, random_square) == 9:
                    if random_square not in found_bombs_set:
                        found_bombs_set.add(random_square)
                    stepped_on_bombs += 1
                else:
                    q.put(getPriorityElem(boardState, random_square))
                dug_set.add(random_square)
                dig_count += 1
                guess_count += 1
                unexplored_set.remove(random_square)
            else:
                print("somehow the q is empty and so is the unexplored set but we didn't find all the bombs")
                break
        else:
            # run the algo.
            cur = q.get()[1]  # each element in the q is ( priority, (x, y) )
            if cur in expanded_set:
                continue
            allNeighbors = getNeighbors(boardState, cur)
            bomb_neighbor_count = squareVal(boardState, cur)
            unopened_neighbors = set()
            known_neighbor_bombs = set()
            for neighbor in allNeighbors:
                if neighbor in unexplored_set:
                    unopened_neighbors.add(neighbor) # identify a neighbor as unopened
                if neighbor in found_bombs_set:
                    known_neighbor_bombs.add(neighbor) # identify a neighbor as a known bomb
            if bomb_neighbor_count == len(known_neighbor_bombs): # if all neighbor bombs have been discovered
                for neighbor in unopened_neighbors:
                    if neighbor in unexplored_set: # dig neighbor
                        dug_set.add(neighbor)
                        dig_count += 1
                        unexplored_set.remove(neighbor)
                        q.put(getPriorityElem(boardState, neighbor))  # put neighbor in q so we can expand the neighbor
            elif bomb_neighbor_count - len(known_neighbor_bombs) == len(unopened_neighbors):
                for neighbor in unopened_neighbors:
                    if neighbor not in found_bombs_set:
                        found_bombs_set.add(neighbor)
                    if neighbor in unexplored_set:
                        unexplored_set.remove(neighbor)  # no bomb expanding ...
            elif len(unopened_neighbors) > 0:
                # open all neighbors but expect bombs ...
                current_bomb_chance = (num_bombs - len(found_bombs_set)) / len(unexplored_set)
                if bomb_neighbor_count / len(unopened_neighbors) < current_bomb_chance:
                    # better chance of picking from neighbors than board at large
                    dig_square = pickRandom(unopened_neighbors)
                    if squareVal(boardState, dig_square) == 9:
                        if dig_square not in found_bombs_set:
                            found_bombs_set.add(dig_square)
                        stepped_on_bombs += 1
                    else:
                        q.put(getPriorityElem(boardState, dig_square))
                    dug_set.add(dig_square)
                    dig_count += 1
                    guess_count += 1
                    unexplored_set.remove(dig_square)
            expanded_set.add(cur)

    # time
    endTime = datetime.datetime.now()
    delta = int ((endTime - startTime).total_seconds() * 1000)
    #
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
