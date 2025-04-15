"""
Celery task definitions for maze explorers.
"""

from celery import Celery
from src.bfs_explorer import BFSExplorer 
import time

# Defining a Celery app instance
app = Celery("maze_tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@app.task
def bfs_task(width, height, maze_type, visualize):
    """
    Celery task to run the BFS Explorer.
    """
    explorer = BFSExplorer(width=width, height=height, maze_type=maze_type, visualize=visualize)
    
    start_time = time.time()
    moves = explorer.solve()
    end_time = time.time()
    
    return {
        "moves": moves,
        "time_taken": end_time - start_time
    }
