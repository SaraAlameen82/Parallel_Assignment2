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
                        help="Run automated maze exploration using Celery tasks")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    parser.add_argument("--wait", action="store_true", 
                        help="Wait for Celery task result (if running in auto mode)")
    parser.add_argument("--strategy", choices=["default", "bfs"], default="default",
                        help="Strategy used to explore the maze: 'default' (stack/DFS) or 'bfs'")

    args = parser.parse_args()

    if args.auto:
        num_explorers = 4
        async_results = []

        print(f"Sending {num_explorers} tasks to Celery workers using strategy '{args.strategy}'...")

        for i in range(num_explorers):
            # Send task to Celery worker
            async_result = run_explorer_task.delay(
                args.width, args.height, args.type, args.visualize, args.strategy)
            async_results.append((i, async_result))

        if args.wait:
            all_results = []
            for i, result in async_results:
                res = result.get(timeout=60)
                all_results.append(res)
                print(f"Explorer {i} solved using {res['strategy']} strategy:\n"
                      f"  Time: {res['time_taken']:.2f}s\n"
                      f"  Moves: {res['moves']}")
            
            # Determine best result by fewest moves
            best = min(all_results, key=lambda x: x['moves'])
            print(f"\n🏆 Best Explorer used '{best['strategy']}' strategy:"
                  f" {best['moves']} moves in {best['time_taken']:.2f}s")
        else:
            for i, result in async_results:
                print(f"Explorer {i} task ID: {result.id}")
    else:
        # Run interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)


if __name__ == "__main__":
    main()
