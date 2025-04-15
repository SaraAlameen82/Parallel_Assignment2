"""
Main entry point for the maze runner game.
"""

import argparse
from src.game import run_game
from tasks import bfs_task
# from tasks import run_explorer_task, a_star_task


def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    # Added a wait argument to wait for the celery task to finish
    parser.add_argument("--wait", action="store_true", 
                        help="Wait for Celery task result (if running in auto mode)")
    
    args = parser.parse_args()
    
    
    if args.auto:
        # Number of explorers to run in parallel
        # num_explorers = 4  
        
        # List to store the results of each explorer
        results = []
    
        print(f"Sending one task of each explorer Celery workers...")
        
        # Send A* explorer task to a Celery worker
        # a_star_result = a_star_task.delay(args.width, args.height, args.type, args.visualize)
        # results.append(("A*_Explorer", a_star_result))

        # Send BFS explorer task to a Celery worker
        bfs_result = bfs_task.delay(args.width, args.height, args.type, args.visualize)
        results.append(("bfs_task", bfs_result))
        
        # Loop to create and send tasks to Celery workers
        """
        for i in range(num_explorers):
            # Using .delay() to queue the tasks asynchronously. 
            async_result = run_explorer_task.delay(args.width, args.height, args.type, args.visualize)
            # Adding the task results to the results list.
            results.append((i, async_result))
        """
            
        if args.wait:
            all_results = []
            for label, result in results:
                # waiting for each task to finish and get the result.
                res = result.get(timeout=60)
                all_results.append((label, res))
                # Printing the result of each explorer.
                print(f"{label} solved the maze in:\n\t Time: {res['time_taken']:.2f}s,\n\t Moves: {res['moves']}")

            # getting the best result from all explorers (minimum number of moves). 
            # lambda function is used to extract the 'moves' key from each result dictionary.
            best = min(all_results, key=lambda x: x[1]['moves'])
            print(f"\nBest Explorer: {best[0]} with {best[1]['moves']} moves in {best[1]['time_taken']:.2f} seconds")
        else:
            # If not waiting, just print the task IDs of the explorers.
            for label, result in results:
                print(f"Explorer {label} task ID: {result.id}")
            
    else: 
        # Run the interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
