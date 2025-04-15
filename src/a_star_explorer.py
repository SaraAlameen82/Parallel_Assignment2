import time
import heapq

def heuristic(a, b):
    """
        Heuristic function to estimate the cost from the current node to the goal.
        
        args:
            a: current position (x, y)
            b: goal position (x, y) 
        returns:
            estimated cost to reach goal from current position 
    """
    # Manhattan distance 
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, maze):
    """ 
        This function returns the neighboring positions that are not walls.
        args:
            pos: current position (x, y)
            maze: 2D list representing the maze
        returns:
            A list of neighborings (x, y) that are not walls.
    """
    # Maze dimensions
    rows, cols = len(maze), len(maze[0])
    # Getting the current position
    r, c = pos
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    neighbors = []
    for dr, dc in directions:
        # Check all neighbors for non-blocked directions
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1: 
            # Add valid neighbors to the list
            neighbors.append((nr, nc))
    # Return the valid cells/neighbors
    return neighbors


def a_star_explorer(maze, visualize=False):
    """
    Implementing A* to explore the maze.
    args:
        maze: 2D list representing the maze
        visualize: boolean to visualize the maze exploration. Defaults to False.
    returns:
        time_taken: time taken to explore the maze
        moves: number of moves taken to explore the maze
    """
    start_time = time.time()

    # Defining start and end positions
    # Start position is top left corner (0, 0)
    start = (0, 0)
    # End position is bottom right corner (len(maze)-1, len(maze[0])-1)
    end = (len(maze) - 1, len(maze[0]) - 1)
    
    # Initiating the priority queue starting from priority 0, position 0.
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # Dictionary to keep track of the best path to each position
    previous_nodes = {}
    # Dictionary to keep track of the cost to reach each position
    g_score = {start: 0}
    # Set to keep track of visited positions, to avoid cycles.
    visited = set()
    
    while open_set:
        # Taking thenode with the lowest cost estimated
        _, current = heapq.heappop(open_set)

        # Skip visited nodes.
        if current in visited:
            continue
        
        # Add the current node to visited set.
        visited.add(current)

        # End exploration if the goal is reached.
        if current == end:
            break
        
        for neighbor in get_neighbors(current, maze):
            # Calculate the possible neighbors of the current node.
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                # Update the g_score for the neighbor if it's better than the current node.
                g_score[neighbor] = tentative_g
                # Calculate the priority based on the g_score and heuristic cost.
                priority = tentative_g + heuristic(neighbor, end)
                # Add the neighbor to the priority queue.
                heapq.heappush(open_set, (priority, neighbor))
                # Record the current node as the previous node for the neighbor.
                previous_nodes[neighbor] = current


    # Reconstructing the path.
    moves = 0
    current = end
    
    # Finding the final shortest path by backtracking from the end node.
    # And then reversing the list to get the correct order.
    while current in previous_nodes:
        current = previous_nodes[current]
        moves += 1

    time_taken = time.time() - start_time
    return time_taken, moves
