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

FINISH = [1, 4]        # Coordinates of finish (y, x)
PIT = [2, 4]
FINISH_REWARD = 10
LIVING_REWARD = -0.5
PIT_REWARD = -10
EPSILON = 0.01         # Convergence threshold
GAMMA = 0.9            # Discount factor

# Checks all neighbors and returns possible moves
def possibleMoves(cell, grid):
    possible_moves = []
    y = cell[0]
    x = cell[1]
    # UP
    if y > 0 and grid[y - 1][x]:
        possible_moves.append([[y - 1, x], "up"])
    # RIGHT
    if x < len(grid[y]) - 1 and grid[y][x + 1]:
        possible_moves.append([[y, x + 1], "right"])
    # DOWN
    if y < len(grid) - 1 and grid[y+1][x]:
        possible_moves.append([[y + 1, x], "down"])
    # LEFT
    if x > 0 and grid[y][x - 1]:
        possible_moves.append([[y, x - 1], "left"])
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

def calculateV(state, possible_moves, V_dict, gamma=GAMMA):
    """Calculates the new V value for a state based on possible moves."""
    max_value = float('-inf')
    for next_move, _ in possible_moves:
        reward = LIVING_REWARD
        if next_move == FINISH:
            reward = FINISH_REWARD
        elif next_move == PIT:
            reward = PIT_REWARD
        value = reward + gamma * V_dict.get(str(next_move), 0)
        max_value = max(max_value, value)  # Find the maximum value among possible moves
    return max_value

def StartModelBased():
    V_dict = {}
    delta = float("inf")
    grid = generateGrid()

    # Initialize V values
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            V_dict[str([y, x])] = 0

    iterations = 0
    while delta > EPSILON:
        delta = 0
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if not grid[y][x] or [y, x] == FINISH or [y, x] == PIT:
                    continue  # Skip walls and terminal states

                state = [y, x]
                possible_moves = possibleMoves(state, grid)

                old_V = V_dict[str(state)]
                new_V = calculateV(state, possible_moves, V_dict)  
                delta = max(delta, abs(new_V - old_V))
                V_dict[str(state)] = new_V 

        iterations += 1
        displayV(V_dict, iterations)
    print("Iterations:", iterations)

StartModelBased()