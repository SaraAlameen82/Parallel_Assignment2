from celery import Celery, group
from src.maze import create_maze
from src.explorer import Explorer


app = Celery('maze_tasks', broker='redis://localhost:6379/0')

@app.task
def run_explorer_task(width, height, maze_type, visualize=False):
    """This function will run the explorer task in a distributed manner.
    It will first create a maze of the maze type passed in the arguments. 
    Then it will create an explorer object and call the solve method on it.
    The solve method will return the time taken and the moves taken to solve the maze.
    The time taken, number of moves, and the maze type will be returned as a dictionary.

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
