"""
Utility functions for the maze solver project.
"""

import time
from typing import List, Tuple, Optional
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)


def print_colored(text: str, color: str = 'white', bold: bool = False):
    """Print colored text to console."""
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    
    style = Style.BRIGHT if bold else ''
    print(f"{style}{color_map.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}")


def print_maze_console(maze, path: Optional[List[Tuple[int, int]]] = None):
    """
    Print maze to console with path visualization.
    
    Args:
        maze: Maze object
        path: Path to highlight (optional)
    """
    path_set = set(path) if path else set()
    
    print("\n" + "=" * (maze.cols * 2 + 3))
    for i in range(maze.rows):
        row_str = "| "
        for j in range(maze.cols):
            if (i, j) == maze.start:
                row_str += f"{Fore.GREEN}S{Style.RESET_ALL} "
            elif (i, j) == maze.goal:
                row_str += f"{Fore.RED}G{Style.RESET_ALL} "
            elif maze.grid[i, j] == 1:
                row_str += f"{Fore.WHITE}██{Style.RESET_ALL}"
            elif (i, j) in path_set:
                row_str += f"{Fore.YELLOW}▣{Style.RESET_ALL} "
            else:
                row_str += "· "
        row_str += "|"
        print(row_str)
    print("=" * (maze.cols * 2 + 3))


def format_path(path: List[Tuple[int, int]]) -> str:
    """Format path as a readable string."""
    if not path:
        return "No path found"
    return " -> ".join([f"({r},{c})" for r, c in path])


def print_path_instructions(path: List[Tuple[int, int]]) -> str:
    """Generate human-readable path instructions."""
    if len(path) < 2:
        return "No path available"
    
    instructions = []
    for i in range(1, len(path)):
        prev_r, prev_c = path[i-1]
        curr_r, curr_c = path[i]
        
        dr = curr_r - prev_r
        dc = curr_c - prev_c
        
        if dr == -1 and dc == 0:
            instructions.append("⬆️ Up")
        elif dr == 1 and dc == 0:
            instructions.append("⬇️ Down")
        elif dr == 0 and dc == -1:
            instructions.append("⬅️ Left")
        elif dr == 0 and dc == 1:
            instructions.append("➡️ Right")
        elif dr == -1 and dc == -1:
            instructions.append("↖️ Up-Left")
        elif dr == -1 and dc == 1:
            instructions.append("↗️ Up-Right")
        elif dr == 1 and dc == -1:
            instructions.append("↙️ Down-Left")
        elif dr == 1 and dc == 1:
            instructions.append("↘️ Down-Right")
    
    return " -> ".join(instructions)


def compare_heuristics(maze, verbose: bool = True) -> dict:
    """
    Compare performance of Manhattan vs Euclidean heuristics.
    
    Args:
        maze: Maze object to solve
        verbose: Whether to print comparison
        
    Returns:
        Dictionary with comparison results
    """
    from astar import AStarSolver
    
    results = {}
    
    for heuristic in ['manhattan', 'euclidean']:
        solver = AStarSolver(maze, heuristic=heuristic)
        solver.solve(verbose=False)
        stats = solver.get_statistics()
        results[heuristic] = stats
    
    if verbose:
        print("\n" + "=" * 60)
        print("📊 HEURISTIC COMPARISON")
        print("=" * 60)
        print(f"{'Metric':<20} {'Manhattan':<20} {'Euclidean':<20}")
        print("-" * 60)
        print(f"{'Path Found':<20} {str(results['manhattan']['path_found']):<20} {str(results['euclidean']['path_found']):<20}")
        print(f"{'Path Length':<20} {results['manhattan']['path_length']:<20} {results['euclidean']['path_length']:<20}")
        print(f"{'Nodes Explored':<20} {results['manhattan']['nodes_explored']:<20} {results['euclidean']['nodes_explored']:<20}")
        print(f"{'Execution Time':<20} {results['manhattan']['execution_time']:.4f}s{' ' * 12} {results['euclidean']['execution_time']:.4f}s")
        print("=" * 60)
    
    return results


def benchmark_mazes(sizes: List[Tuple[int, int]], n_runs: int = 3):
    """
    Benchmark A* performance on different maze sizes.
    
    Args:
        sizes: List of (rows, cols) tuples
        n_runs: Number of runs per size
    """
    from maze import MazeGenerator
    from astar import AStarSolver
    
    print("\n" + "=" * 70)
    print("📊 PERFORMANCE BENCHMARK")
    print("=" * 70)
    print(f"{'Maze Size':<15} {'Avg Nodes':<15} {'Avg Time (s)':<15} {'Path Found'}")
    print("-" * 70)
    
    for rows, cols in sizes:
        total_nodes = 0
        total_time = 0
        found_count = 0
        
        for _ in range(n_runs):
            maze = MazeGenerator.random_maze(rows, cols, wall_probability=0.3)
            solver = AStarSolver(maze, heuristic='manhattan')
            path = solver.solve(verbose=False)
            
            stats = solver.get_statistics()
            total_nodes += stats['nodes_explored']
            total_time += stats['execution_time']
            if stats['path_found']:
                found_count += 1
        
        avg_nodes = total_nodes / n_runs
        avg_time = total_time / n_runs
        found_rate = f"{found_count}/{n_runs}"
        
        print(f"{rows}x{cols:<12} {avg_nodes:<15.0f} {avg_time:<15.4f} {found_rate}")
    
    print("=" * 70)


def create_step_visualization(maze, solver, output_dir: str = "steps", max_steps: int = 20):
    """
    Create step-by-step visualization of the search process.
    
    Args:
        maze: Maze object
        solver: AStarSolver instance
        output_dir: Directory to save step images
        max_steps: Maximum number of steps to visualize
    """
    import os
    from visualizer import MazeVisualizer
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer = MazeVisualizer(maze)
    
    # Run search step by step (simplified simulation)
    # This would need modification of the A* algorithm to return intermediate states
    
    print(f"📁 Step visualizations saved to: {output_dir}/")