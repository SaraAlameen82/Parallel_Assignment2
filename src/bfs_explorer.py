import time
from collections import deque


class BFSExplorer:
    """
    BFS Explorer for solving mazes using the Breadth-First Search algorithm.
    """

    def __init__(self, maze, start, end, visualize=False):
        """
        Initialize the BFS explorer.

        Args:
            maze (Maze): The maze instance to explore.
            start (tuple): Starting coordinate (row, col).
            end (tuple): Goal coordinate (row, col).
            visualize (bool): Whether to visualize the exploration step-by-step.
        """
        self.maze = maze
        self.start = start
        self.end = end
        self.visualize = visualize
        self.visited = set()
        self.came_from = {}
        self.path = []

    def get_neighbors(self, pos):
        """
        Get valid neighboring cells of the current position.

        Args:
            pos (tuple): The current position (row, col).

        Returns:
            list: List of valid neighboring positions.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = pos[0] + dr, pos[1] + dc
            if self.maze.in_bounds((nr, nc)) and self.maze.is_open((nr, nc)):
                neighbors.append((nr, nc))
        return neighbors

    def reconstruct_path(self, current):
        """
        Reconstruct the path from start to end.

        Args:
            current (tuple): The goal position.

        Returns:
            list: The reconstructed path from start to current.
        """
        path = []
        while current != self.start:
            path.append(current)
            current = self.came_from[current]
        path.append(self.start)
        path.reverse()
        return path

    def run(self):
        """
        Run the BFS algorithm to explore the maze.

        Returns:
            dict: A dictionary with the time taken and number of moves.
        """
        start_time = time.time()
        queue = deque()
        queue.append(self.start)
        self.visited.add(self.start)

        while queue:
            current = queue.popleft()

            if current == self.end:
                self.path = self.reconstruct_path(current)
                break

            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.came_from[neighbor] = current
                    queue.append(neighbor)

            if self.visualize:
                self.maze.update_visual(current)

        end_time = time.time()
        time_taken = end_time - start_time
        num_moves = len(self.path)

        return {
            "time_taken": time_taken,
            "moves": num_moves,
            "path": self.path,
        }
