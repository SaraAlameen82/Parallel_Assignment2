"""
Main entry point for the maze runner game.
"""

import argparse
from src.game import run_game
from tasks import run_explorer_task 


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
        num_explorers = 4  
        async_results = []
    
        print(f"Sending {num_explorers} tasks to Celery workers...")
        
        # Loop to create and send tasks to Celery workers
        for i in range(num_explorers):
            # Using .delay() to queue the tasks asynchronously. 
            async_result = run_explorer_task.delay(args.width, args.height, args.type, args.visualize)
            # Adding the task results to the results list.
            async_results.append((i, async_result))
            
            
        if args.wait:
            all_results = []
            for i, result in async_results:
                # waiting for each task to finish and get the result.
                res = result.get(timeout=60)
                all_results.append(res)
                print(f"Explorer {i} solved in:\n Time: {res['time_taken']:.2f}s,\n Moves: {res['moves']}")

            # getting the best result from all explorers (minimum number of moves). 
            # lambda function is used to extract the 'moves' key from each result dictionary.
            best = min(all_results, key=lambda x: x['moves'])
            print(f"\nBest Explorer: {best['moves']} moves in {best['time_taken']:.2f}s")
        else:
            for i, result in async_results:
                print(f"Explorer {i} task ID: {result.id}")
            
    else: 
        # Run the interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
