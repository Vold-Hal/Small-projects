import random

# Grid map, where 1-space, 0-wall
grid_strings = [
    "11111",
    "10111",
    "10011",
    "11111"
]


def generateGrid():
    # Convert binary strings to a two-dimensional int array
    grid = [[int(char) for char in string] for string in grid_strings]
    # Convert integer values to boolean
    grid = [[bool(num) for num in row] for row in grid]
    return grid

FINISH = [1, 4]     #Coordinates of finish. IMPORTANT: ALL COORDINATES ARE IN [y, x] FORMATE
PIT = [2, 4]       
FINISH_REWARD = 10    
LIVING_REWARD = -0.5
PIT_REWARD = -10
EPSILON = 0.01 # Convergence threshold

# Checks all neighbors and returns possible moves
def possibleMoves(cell, grid):
    possible_moves = []
    y = cell[0]
    x = cell[1]
    # UP
    if y > 0 and grid[y - 1][x]:
        possible_moves.append([y - 1, x])
    # RIGHT
    if x < len(grid[y]) - 1 and grid[y][x + 1]:
        possible_moves.append([y, x + 1])
    # DOWN
    if y < len(grid) - 1 and grid[y+1][x]:
        possible_moves.append([y + 1, x])
    # LEFT
    if x > 0 and grid[y][x - 1]:
        possible_moves.append([y, x - 1])
    return possible_moves

def displayMoves(moves):
    print(moves)
    display_array = generateGrid()
    for y in range(len(display_array)):
        for x in range(len(display_array[0])):
            if display_array[y][x]:
                display_array[y][x] = "00000"
                for move in moves:
                    if [y, x] == move[0]:
                        display_array[y][x] = move[1]
                        break
            else: display_array[y][x] = "WWWWW"
    for row in display_array:
        print(" ".join("{:<5.2f}".format(element) if isinstance(element, float) else "{:<5}".format(str(element)) for element in row))

def displayV(V_dict, iterations):
    print("=========V values=========")
    display_array = generateGrid()
    for y in range(len(display_array)):
        for x in range(len(display_array[0])):
            if display_array[y][x]:
                display_array[y][x] = V_dict[str([y,x])]
                if [y,x] == FINISH:
                    display_array[y][x] = FINISH_REWARD
                elif [y,x] == PIT:
                    display_array[y][x] = PIT_REWARD
            else: display_array[y][x] = "WWWWW"
    for row in display_array:
        print(" ".join("{:<5.2f}".format(element) if isinstance(element, float) else "{:<5}".format(str(element)) for element in row))
    print("Iterations:", iterations)

def startModelFree():
    grid = generateGrid()
    
    V_dict = {}

    #Initialising starting grid of V values
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            V_dict[str([y, x])] = []

    
    
    iterations = 0
    
    delta = float("inf")
    while delta > EPSILON:
        moves = [] #list of nodes passed by agent and rewards for them
        delta = 0
        grid = generateGrid()
        #Choosing a random place to start
        while True:
            y = random.randint(0, len(grid) - 1)
            x = random.randint(0, len(grid[0]) - 1)
            if grid[y][x] and [y, x] != FINISH and [y, x] != PIT:
                moves.append([[y, x], 0])
                grid[y][x] = False
                break

        is_finished = False
        while not is_finished:
            possible_moves = possibleMoves(moves[-1][0], grid)
            if not possible_moves:
                break
            next_move = random.choice(possible_moves)
            reward = 0
            if next_move == FINISH:
                reward = FINISH_REWARD
                is_finished = True
            elif next_move == PIT:
                reward = PIT_REWARD
                is_finished = True
            reward += LIVING_REWARD 

            moves.append([next_move, reward])
            grid[next_move[0]][next_move[1]] = False
        displayMoves(moves)

        value = 0
        prev_V = sum(V_dict.get([str([y, x])]), 0) / len(V_dict[str([y, x])])
        while moves:
            move = moves.pop()
            value += move[1]
            V_dict[str(move[0])].append(value)
        new_V = sum(V_dict.get([str([y, x])]), 0) / len(V_dict[str([y, x])])
        delta = max(delta, abs(new_V - prev_V))
        iterations += 1 
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            V_dict[str([y, x])] = sum(V_dict[str([y, x])]) / len(V_dict[str([y, x])])
    displayV(V_dict, iterations)




startModelFree()