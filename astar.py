"""
A* Search Algorithm implementation for maze solving.
"""

import heapq
import time
import math
from typing import List, Tuple, Optional, Dict, Set
from maze import Maze


class AStarSolver:
    """
    A* search algorithm for finding shortest path in a maze.
    """
    
    def __init__(self, maze: Maze, heuristic: str = 'manhattan', allow_diagonal: bool = False):
        """
        Initialize A* solver.
        
        Args:
            maze: Maze object to solve
            heuristic: Type of heuristic ('manhattan' or 'euclidean')
            allow_diagonal: Whether to allow diagonal movement
        """
        self.maze = maze
        self.heuristic_type = heuristic
        self.allow_diagonal = allow_diagonal
        self.explored = []  # Track explored nodes for visualization
        self.path = []
        self.nodes_explored = 0
        self.execution_time = 0
        self.path_length = 0
        self._heuristic_func = self._get_heuristic_function()
    
    def _get_heuristic_function(self):
        """Return the appropriate heuristic function."""
        if self.heuristic_type == 'manhattan':
            return self._manhattan_distance
        elif self.heuristic_type == 'euclidean':
            return self._euclidean_distance
        else:
            raise ValueError(f"Unknown heuristic: {self.heuristic_type}")
    
    def _manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Manhattan distance between two points."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def _euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get walkable neighbors based on movement configuration."""
        if self.allow_diagonal:
            return self.maze.get_neighbors_with_diagonal(pos[0], pos[1])
        else:
            return self.maze.get_neighbors(pos[0], pos[1])
    
    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], 
                          current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct the path from start to goal."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def solve(self, verbose: bool = True) -> Optional[List[Tuple[int, int]]]:
        """
        Solve the maze using A* search algorithm.
        
        Args:
            verbose: Whether to print progress information
            
        Returns:
            Path from start to goal as list of (row, col) tuples, or None if no path exists
        """
        start_time = time.time()
        
        start = self.maze.start
        goal = self.maze.goal
        
        # Priority queue: (f_score, counter, position)
        open_set = [(0, 0, start)]
        counter = 1
        
        # Track where each node came from
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        # g_score: cost from start to node
        g_score: Dict[Tuple[int, int], float] = {start: 0}
        
        # f_score: g_score + heuristic
        f_score: Dict[Tuple[int, int], float] = {start: self._heuristic_func(start, goal)}
        
        # Track explored nodes for visualization
        self.explored = []
        closed_set: Set[Tuple[int, int]] = set()
        
        if verbose:
            print("\n🧩 Starting A* Search...")
            print(f"📏 Heuristic: {self.heuristic_type.capitalize()}")
            print(f"📐 Movement: {'8-directional' if self.allow_diagonal else '4-directional'}")
            print(f"📍 Start: {start}")
            print(f"🎯 Goal: {goal}")
            print("-" * 40)
        
        while open_set:
            # Get node with lowest f_score
            current_f, _, current = heapq.heappop(open_set)
            
            # Skip if already processed
            if current in closed_set:
                continue
            
            # Record explored node
            if current not in self.explored:
                self.explored.append(current)
            self.nodes_explored += 1
            
            # Check if we reached the goal
            if current == goal:
                self.path = self._reconstruct_path(came_from, current)
                self.path_length = len(self.path) - 1
                self.execution_time = time.time() - start_time
                
                if verbose:
                    print(f"\n✅ Path Found!")
                    print(f"📊 Path Length: {self.path_length} steps")
                    print(f"🔍 Nodes Explored: {self.nodes_explored}")
                    print(f"⏱️  Execution Time: {self.execution_time:.4f} seconds")
                
                return self.path
            
            closed_set.add(current)
            
            # Explore neighbors
            for neighbor in self._get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g_score
                # For diagonal movement, cost is sqrt(2), otherwise 1
                if self.allow_diagonal:
                    dr = abs(neighbor[0] - current[0])
                    dc = abs(neighbor[1] - current[1])
                    if dr == 1 and dc == 1:
                        cost = math.sqrt(2)
                    else:
                        cost = 1
                else:
                    cost = 1
                
                tentative_g = g_score[current] + cost
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    # This is a better path
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic_func(neighbor, goal)
                    
                    # Add to open set
                    heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                    counter += 1
            
            if verbose and self.nodes_explored % 100 == 0:
                print(f"📊 Explored {self.nodes_explored} nodes...")
        
        # No path found
        self.execution_time = time.time() - start_time
        if verbose:
            print(f"\n❌ No Path Found!")
            print(f"🔍 Nodes Explored: {self.nodes_explored}")
            print(f"⏱️  Execution Time: {self.execution_time:.4f} seconds")
        
        return None
    
    def get_statistics(self) -> Dict:
        """
        Get detailed statistics about the search.
        
        Returns:
            Dictionary containing search statistics
        """
        return {
            'nodes_explored': self.nodes_explored,
            'path_length': self.path_length,
            'execution_time': self.execution_time,
            'heuristic': self.heuristic_type,
            'path_found': bool(self.path),
            'maze_size': self.maze.get_size(),
            'allow_diagonal': self.allow_diagonal
        }
    
    def print_statistics(self):
        """Print formatted statistics."""
        stats = self.get_statistics()
        print("\n" + "=" * 50)
        print("📊 SEARCH STATISTICS")
        print("=" * 50)
        print(f"📍 Maze Size: {stats['maze_size'][0]}x{stats['maze_size'][1]}")
        print(f"📏 Heuristic: {stats['heuristic'].capitalize()}")
        print(f"📐 Movement: {'8-directional' if stats['allow_diagonal'] else '4-directional'}")
        print(f"✅ Path Found: {stats['path_found']}")
        if stats['path_found']:
            print(f"🛤️  Path Length: {stats['path_length']} steps")
        print(f"🔍 Nodes Explored: {stats['nodes_explored']}")
        print(f"⏱️  Execution Time: {stats['execution_time']:.4f} seconds")
        print("=" * 50)