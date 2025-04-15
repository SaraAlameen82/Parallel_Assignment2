"""
Main entry point for the maze runner game.
"""

import argparse
from src.game import run_game
from tasks import bfs_task 


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
    parser.add_argument("--wait", action="store_true", 
                        help="Wait for Celery task result (if running in auto mode)")
    
    args = parser.parse_args()

    if args.auto:
        print("Sending BFS task to Celery worker...")
        results = []

        # Send BFS explorer task
        bfs_result = bfs_task.delay(args.width, args.height, args.type, args.visualize)
        results.append(("BFS_Explorer", bfs_result))

        if args.wait:
            all_results = []
            for label, result in results:
                res = result.get(timeout=60)
                all_results.append((label, res))
                print(f"{label} solved the maze in:\n\t Time: {res['time_taken']:.2f}s,\n\t Moves: {res['moves']}")
        else:
            for label, result in results:
                print(f"{label} task ID: {result.id}")

    else:
        run_game(maze_type=args.type, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
