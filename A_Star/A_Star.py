from pyamaze import maze, agent, textLabel, COLOR
from queue import PriorityQueue
import random

MAZE_SIZE = [15, 30]
VARIABILITY = 0 #percents

def heuristic(cell1, cell2):
    # Manhattan distance heuristic
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def AStar(_maze):
    start = (_maze.rows, _maze.cols)#Starting cell is the last cell of a maze
    goal = (1, 1)

    previus_cell = {}
    g_cost = {}
    previus_cell[start] = None
    g_cost[start] = 0

    currentCells = PriorityQueue()
    currentCells.put(start, 0)

    searchPath=[start]

    while not currentCells.empty():
        current = currentCells.get()
        searchPath.append(current)
        if current == goal:
            break

        #Checking all four directions for available cells
        for direction in 'ESNW':
            if _maze.maze_map[current][direction]==True:
                if direction=='E':
                    next_cell=(current[0],current[1]+1)
                if direction=='W':
                    next_cell=(current[0],current[1]-1)
                if direction=='N':
                    next_cell=(current[0]-1,current[1])
                if direction=='S':
                    next_cell=(current[0]+1,current[1])

                new_g_cost = g_cost[current] + 1
                if next_cell not in g_cost or new_g_cost < g_cost[next_cell]:
                    g_cost[next_cell] = new_g_cost
                    priority = new_g_cost + heuristic(next_cell, goal)
                    currentCells.put(next_cell, priority)
                    previus_cell[next_cell] = current
    
    # Reconstruct path
    path = {}
    current = goal
    while current != start:
        path[previus_cell[current]] = current
        current = previus_cell[current]
    return path, searchPath


#Creating maze
from pyamaze import maze
main_maze = maze(MAZE_SIZE[0],MAZE_SIZE[1])
main_maze.CreateMaze(loopPercent=VARIABILITY)

#Running A*
path, searchPath = AStar(main_maze)


print(path)
print(searchPath)
#Drawing pathes 
search_agent=agent(main_maze,footprints=True,color=COLOR.blue,filled=True)
path_agent=agent(main_maze,shape='arrow',color=COLOR.red ,footprints=True)
delay = (int)(3000 / len(path))
main_maze.tracePath({search_agent:searchPath}, delay=delay)
main_maze.tracePath({path_agent:path}, delay=delay)
label = textLabel(main_maze, "A* Path Length", len(path) + 1)
main_maze.run()
