from celery import Celery
from src.maze import create_maze
from src.explorer import Explorer  
from src.bfs_explorer import BFSExplorer  

# Create a Celery app instance with Redis as broker and backend
app = Celery('maze_tasks', 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')


@app.task
def run_explorer_task(width, height, maze_type, visualize=False, strategy="default"):
    """
    This function runs a maze exploration task in a distributed way using Celery.
    It supports two strategies: default (stack-based, DFS-style) and bfs (queue-based BFS).

    Args:
        width (int): Maze width.
        height (int): Maze height.
        maze_type (str): Type of maze to generate ('random' or 'static').
        visualize (bool): If True, visualize the maze solving (optional).
        strategy (str): Strategy to use: 'default' or 'bfs'.

    Returns:
        dict: Dictionary containing time taken, number of moves, maze type, and strategy used.
    """
    maze = create_maze(width, height, maze_type)

    # Choose solver based on strategy
    if strategy == "bfs":
        explorer = BFSExplorer(maze, visualize=False)
    else:
        explorer = Explorer(maze, visualize=False)

    time_taken, moves = explorer.solve()

    return {
        'time_taken': time_taken,
        'moves': len(moves),
        'type': maze_type,
        'strategy': strategy
    }
