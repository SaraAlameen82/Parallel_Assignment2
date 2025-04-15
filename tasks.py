from celery import Celery, group
from src.maze import create_maze
from src.explorer import Explorer
from src.a_star_explorer import a_star_explorer 
from src.bfs_explorer import bfs_explore 
import copy


# Creating a Celery app with Redis broker and backend
app = Celery('maze_tasks', 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def run_explorer_task(width, height, maze_type, visualize=False):
    """
        Celery function to run the original maze explorer task.

        Args:
            width (int): maze width
            height (int): maze height
            maze_type (str): maze type
            visualize (bool): the option to visualize the maze exploration. Defaults to False.

        Returns:
            dictionary: a dictionary containing the time taken, number of moves, and maze type.
    """
    maze = create_maze(width, height, maze_type)
    explorer = Explorer(maze, visualize=False) 
    time_taken, moves = explorer.solve()
    return {
        'time_taken': time_taken,
        'moves': len(moves),
        'type': maze_type
    }

@app.task
def a_star_explorer(width, height, maze_type, visualize=False):
    """
        Celery task for running A* algorithm on a generated maze.
        args:
            width (int): maze width
            height (int): maze height
            maze_type (str): maze type
            visualize (bool): the option to visualize the maze exploration. Defaults to False.
        returns:
            dictionary: a dictionary containing the time taken, number of moves, and maze type.
    """
    maze = create_maze(width, height, maze_type)
    # Creating a deep copy of the maze to avoid modifying the original maze
    maze_copy = copy.deepcopy(maze)
    # running the A* explorer on the copied maze
    time_taken, moves = a_star_explorer(maze_copy, visualize)
    return {
        'time_taken': time_taken,
        'moves': len(moves),
        'type': maze_type
    }

@app.task
def bfs_explorer(width, height, maze_type, visualize=False):
    """
        Celery task for running BFS algorithm on a generated maze.
        args:
            width (int): maze width
            height (int): maze height
            maze_type (str): maze type
            visualize (bool): the option to visualize the maze exploration. Defaults to False.
        returns:
            dictionary: a dictionary containing the time taken, number of moves, and maze type.
    """
    maze = create_maze(width, height, maze_type)
    # Creating a deep copy of the maze to avoid modifying the original maze
    maze_copy = copy.deepcopy(maze)
    # running the BFS explorer on the copied maze
    time_taken, moves = bfs_explore(maze_copy, visualize)
    return {
        'time_taken': time_taken,
        'moves': len(moves),
        'type': maze_type
    }
