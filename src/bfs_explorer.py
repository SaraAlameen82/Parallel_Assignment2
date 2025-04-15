import time
from collections import deque

def get_neighbors(pos, maze):
    """
        Finds the neighboring positions that are not walls.
        Args:
            pos: Current position (x, y).
            maze: 2D list representing the maze.
        Returns:
            A list of neighboring (x, y) positions that are not walls.
    """
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    neighbors = []
    for dr, dc in directions:
        # Check all neighbors for walls
        nr, nc = r + dr, c + dc
        # Check if the neighbor is within bounds and not a wall
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1:
            # 
            neighbors.append((nr, nc))
    return neighbors

def bfs_explorer(maze, visualize=False):
    """
        Implementing BFS to explore the maze.
        Args:
            maze: 2D list representing the maze.
            visualize: Boolean to visualize the maze exploration. Defaults to False.
        Returns:
            time_taken: Time taken to explore the maze.
            moves: Number of moves taken to explore the maze.
    """
    start_time = time.time()

    # Defining start and end (gaol) positions
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)

    # Initiating the queue for BFS
    queue = deque([start])
    visited = set([start])
    # Dictionary to keep track of previous nodes to reconstruct the final path
    previous_nodes = {}

    while queue:
        # Dequeue the current position from the front of the queue.
        current = queue.popleft()

        # stop exploring if the goal is reached.
        if current == end:
            break

        # Check if each neighbor is valid and not visited.
        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                # Mark the neighbor as visited and enqueue it.
                visited.add(neighbor)
                queue.append(neighbor)
                # Add the current node to the previous nodes dictionary.
                previous_nodes[neighbor] = current


    # Reconstruct path
    moves = 0
    current = end
    
    # Finding the final shortest path by backtracking from the end node.
    # And then reversing the list to get the correct order.
    while current in previous_nodes:
        current = previous_nodes[current]
        moves += 1

    time_taken = time.time() - start_time
    return time_taken, moves
