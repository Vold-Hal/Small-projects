# Grid map, where 1-space, 0-wall
grid_strings = [
    "11111",
    "10111",
    "10011",
    "11111"
]

# Convert binary strings to a two-dimensional int array
grid = [[int(char) for char in string] for string in grid_strings]
# Convert integer values to boolean
grid = [[bool(num) for num in row] for row in grid]

# Creating an array of V values
V_values = [[-99 for value in row] for row in grid]
for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        if not grid[y][x]:
            V_values[y][x] = "WWWWW"


FINISH = [1, 4]  
PIT = [2, 4]       #Coordinates of finish. IMPORTANT: ALL COORDINATES ARE IN [y, x] FORMATE
FINALE_REWARD = 10    
LIVING_REWARD = -0.5

iterations_done = 0     #counts iterations for debug, no technical use 

# Checks all neighbors and returns possible moves
def possibleMoves(cell):
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

def iterate():
    global V_values
    #A new grid for updated V values
    new_V_values = [row[:] for row in V_values]

    #Checking every cell in the grid
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            if [y, x] == FINISH:
                new_V_values[y][x] = FINALE_REWARD
            elif grid[y][x]:
                possible_moves = possibleMoves([y, x])
                v_sum = 0
                length = 0
                for move in possible_moves:
                    if V_values[move[0]][move[1]] != -99:
                        v_sum += V_values[move[0]][move[1]]
                        length+=1
                if length > 0:
                        new_V_values[y][x] = v_sum / length + LIVING_REWARD
    V_values[:] = new_V_values


while True:
    for row in V_values:
        print(" ".join("{:<5.2f}".format(element) if isinstance(element, float) else "{:<5}".format(str(element)) for element in row))
    print("Total iterations:", iterations_done, "\n")
    iterations = input("Enter a number of iterations to perform or 'e' to exit:")
    try:
        iterations = int(iterations)
        for i in range(iterations):
            iterate()
        iterations_done += iterations
    except ValueError:
        break

