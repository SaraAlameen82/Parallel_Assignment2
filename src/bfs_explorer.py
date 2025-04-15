from collections import deque
import time

class BFSExplorer:
    """
    Explorer that solves the maze using Breadth-First Search (BFS).
    Guarantees the shortest path in an unweighted maze.
    """

    def __init__(self, maze, visualize=False):
        self.maze = maze
        self.visualize = visualize
        self.start = maze.start
        self.end = maze.end
        self.visited = set()

    def get_neighbors(self, position):
        """Returns all valid neighbors from a given cell."""
        x, y = position
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.maze.is_valid(nx, ny) and (nx, ny) not in self.visited:
                neighbors.append((nx, ny))
        return neighbors

    def solve(self):
        """Runs BFS to find the shortest path from start to end."""
        start_time = time.time()
        queue = deque()
        queue.append((self.start, [self.start]))
        self.visited.add(self.start)

        while queue:
            current, path = queue.popleft()
            if current == self.end:
                time_taken = time.time() - start_time
                return time_taken, path

            for neighbor in self.get_neighbors(current):
                self.visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        time_taken = time.time() - start_time
        return time_taken, []
