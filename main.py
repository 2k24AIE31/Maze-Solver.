#!/usr/bin/env python3
"""
Main entry point for the Maze Solver using A* Search.
"""

import argparse
import sys
import os

# Ensure the script's directory is in the path (fixes module imports on Windows)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from maze import Maze, MazeGenerator
from astar import AStarSolver
from visualizer import MazeVisualizer
from utils import print_maze_console, compare_heuristics, benchmark_mazes
from examples.example_mazes import get_example_mazes


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Maze Solver using A* Search Algorithm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                  # Run with default maze
  python main.py --custom         # Run with custom interactive maze
  python main.py --example spiral # Run with spiral maze
  python main.py --compare        # Compare Manhattan vs Euclidean heuristics
  python main.py --benchmark      # Run performance benchmark
        """
    )

    parser.add_argument(
        '--custom', '-c',
        action='store_true',
        help='Create a custom maze interactively'
    )

    parser.add_argument(
        '--example', '-e',
        type=str,
        choices=['simple', 'spiral', 'obstacle', 'open'],
        default='simple',
        help='Example maze to run (default: simple)'
    )

    parser.add_argument(
        '--heuristic', '-H',
        type=str,
        choices=['manhattan', 'euclidean'],
        default='manhattan',
        help='Heuristic function (default: manhattan)'
    )

    parser.add_argument(
        '--diagonal', '-d',
        action='store_true',
        help='Allow 8-directional movement (diagonal)'
    )

    parser.add_argument(
        '--compare', '-C',
        action='store_true',
        help='Compare Manhattan vs Euclidean heuristics'
    )

    parser.add_argument(
        '--benchmark', '-B',
        action='store_true',
        help='Run performance benchmark'
    )

    parser.add_argument(
        '--save', '-s',
        type=str,
        help='Save visualization to file'
    )

    parser.add_argument(
        '--no-show',
        action='store_true',
        help="Don't show visualization (for benchmarking)"
    )

    return parser.parse_args()


def run_example_maze(maze_type: str, heuristic: str, allow_diagonal: bool,
                     save_path: str = None, show: bool = True):
    """Run a predefined example maze."""
    mazes = get_example_mazes()

    if maze_type not in mazes:
        print(f"❌ Unknown maze type: {maze_type}")
        return

    maze = mazes[maze_type]()
    print(f"\n🧩 Example Maze: {maze_type.capitalize()}")
    print_maze_console(maze)

    # Solve
    solver = AStarSolver(maze, heuristic=heuristic, allow_diagonal=allow_diagonal)
    path = solver.solve()

    if path:
        print_maze_console(maze, path)
        solver.print_statistics()

        if show:
            visualizer = MazeVisualizer(maze)
            visualizer.visualize(
                path=path,
                explored=solver.explored,
                title=f"Maze Solver - A* ({heuristic.capitalize()} Heuristic)",
                save_path=save_path
            )
    else:
        print("❌ No path found!")
        solver.print_statistics()

        if show:
            visualizer = MazeVisualizer(maze)
            visualizer.visualize(
                path=None,
                explored=solver.explored,
                title=f"Maze Solver - No Path Found ({heuristic.capitalize()} Heuristic)",
                save_path=save_path
            )


def create_custom_maze():
    """Create a maze interactively."""
    print("\n" + "=" * 50)
    print("🧩 CUSTOM MAZE CREATOR")
    print("=" * 50)

    try:
        rows = int(input("Enter number of rows (5-20): "))
        cols = int(input("Enter number of columns (5-20): "))

        if rows < 5 or rows > 20 or cols < 5 or cols > 20:
            print("❌ Dimensions must be between 5 and 20")
            return None

        maze = Maze(rows, cols)

        choice = input("Add random walls? (y/n): ").lower()
        if choice == 'y':
            probability = float(input("Enter wall probability (0.1-0.5): "))
            maze = MazeGenerator.random_maze(rows, cols, probability)

        print(f"\nMaze created: {rows}x{cols}")
        print_maze_console(maze)

        return maze

    except ValueError as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main execution function."""
    args = parse_arguments()

    print("""
    +===========================================+
    |   MAZE SOLVER - A* SEARCH ALGORITHM       |
    |       Artificial Intelligence Project     |
    +===========================================+
    """)

    # Handle special modes
    if args.benchmark:
        sizes = [(10, 10), (15, 15), (20, 20), (30, 30)]
        benchmark_mazes(sizes)
        return

    if args.compare:
        maze = MazeGenerator.random_maze(15, 15, wall_probability=0.3)
        print("📊 Comparing Heuristics on Random Maze:")
        print_maze_console(maze)
        compare_heuristics(maze)
        return

    # Handle custom maze
    if args.custom:
        maze = create_custom_maze()
        if maze is None:
            return
    else:
        run_example_maze(
            args.example,
            args.heuristic,
            args.diagonal,
            args.save,
            not args.no_show
        )
        return

    # Solve custom maze
    solver = AStarSolver(maze, heuristic=args.heuristic, allow_diagonal=args.diagonal)
    path = solver.solve()

    if path:
        print_maze_console(maze, path)
        solver.print_statistics()

        if not args.no_show:
            visualizer = MazeVisualizer(maze)
            visualizer.visualize(
                path=path,
                explored=solver.explored,
                title=f"Maze Solver - A* ({args.heuristic.capitalize()} Heuristic)",
                save_path=args.save
            )
    else:
        print("❌ No path found!")
        solver.print_statistics()

        if not args.no_show:
            visualizer = MazeVisualizer(maze)
            visualizer.visualize(
                path=None,
                explored=solver.explored,
                title=f"Maze Solver - No Path Found ({args.heuristic.capitalize()} Heuristic)",
                save_path=args.save
            )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)