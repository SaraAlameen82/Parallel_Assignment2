"""
Breadth-First Search (BFS) maze explorer implementation.
"""

from collections import deque
import time
from src.constants import MAZE_WIDTH, MAZE_HEIGHT

class BFSExplorer:
    def __init__(self, maze, start, goal, visualizer=None):
        """
        Initialize the BFS explorer.
        
        Args:
            maze: The maze grid.
            start: Starting coordinate as (row, col).
            goal: Goal coordinate as (row, col).
            visualizer: Optional visualizer function or object for step visualization.
        """
        self.maze = maze
        self.start = start
        self.goal = goal
        self.visualizer = visualizer
        self.visited = [[False for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        self.parent = [[None for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]

    def get_neighbors(self, position):
        """
        Return all valid neighboring cells for a given position.
        """
        row, col = position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < MAZE_HEIGHT and 0 <= c < MAZE_WIDTH:
                if self.maze[r][c] != 1:  # not a wall
                    neighbors.append((r, c))
        return neighbors

    def reconstruct_path(self):
        """
        Reconstruct the path from goal to start using parent links.
        """
        path = []
        current = self.goal
        while current is not None:
            path.append(current)
            current = self.parent[current[0]][current[1]]
        path.reverse()
        return path

    def explore(self):
        """
        Run the BFS algorithm to explore the maze.
        
        Returns:
            dict: Contains 'moves' and 'time_taken'.
        """
        start_time = time.time()
        queue = deque([self.start])
        self.visited[self.start[0]][self.start[1]] = True

        while queue:
            current = queue.popleft()

            if self.visualizer:
                self.visualizer(current)

            if current == self.goal:
                break

            for neighbor in self.get_neighbors(current):
                r, c = neighbor
                if not self.visited[r][c]:
                    self.visited[r][c] = True
                    self.parent[r][c] = current
