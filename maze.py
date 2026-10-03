"""
Maze class for creating and managing grid-based mazes.
"""

import numpy as np
from typing import List, Tuple


class Maze:
    """
    Represents a grid-based maze with walls, start, and goal positions.
    """

    def __init__(self, rows: int, cols: int):
        """
        Initialize maze with given dimensions.

        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)  # 0 = empty, 1 = wall
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)
        self._validate_positions()

    def _validate_positions(self):
        """Ensure start and goal positions are valid."""
        if not self._is_valid_position(*self.start):
            raise ValueError(f"Invalid start position: {self.start}")
        if not self._is_valid_position(*self.goal):
            raise ValueError(f"Invalid goal position: {self.goal}")
        if self.start == self.goal:
            raise ValueError("Start and goal cannot be the same position")

    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is within maze bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _is_walkable(self, row: int, col: int) -> bool:
        """Check if a position is walkable (not a wall and within bounds)."""
        if not self._is_valid_position(row, col):
            return False
        return self.grid[row, col] == 0

    def add_wall(self, row: int, col: int):
        """
        Add a wall at the specified position.

        Args:
            row: Row index
            col: Column index
        """
        if not self._is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        if (row, col) == self.start:
            raise ValueError("Cannot place wall at start position")
        if (row, col) == self.goal:
            raise ValueError("Cannot place wall at goal position")
        self.grid[row, col] = 1

    def add_walls(self, positions: List[Tuple[int, int]]):
        """
        Add multiple walls at once.

        Args:
            positions: List of (row, col) positions
        """
        for row, col in positions:
            self.add_wall(row, col)

    def remove_wall(self, row: int, col: int):
        """Remove a wall at the specified position."""
        if not self._is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        self.grid[row, col] = 0

    def set_start(self, row: int, col: int):
        """Set the start position."""
        if not self._is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        if self.grid[row, col] == 1:
            raise ValueError("Cannot set start on a wall")
        self.start = (row, col)

    def set_goal(self, row: int, col: int):
        """Set the goal position."""
        if not self._is_valid_position(row, col):
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        if self.grid[row, col] == 1:
            raise ValueError("Cannot set goal on a wall")
        self.goal = (row, col)

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get all walkable neighbors of a position (4-directional).

        Args:
            row: Row index
            col: Column index

        Returns:
            List of (row, col) tuples for valid neighbors
        """
        neighbors = []
        # 4-directional movement: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self._is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col))

        return neighbors

    def get_neighbors_with_diagonal(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get all walkable neighbors including diagonals.

        Args:
            row: Row index
            col: Column index

        Returns:
            List of (row, col) tuples for valid neighbors
        """
        neighbors = []
        # 8-directional movement
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self._is_walkable(new_row, new_col):
                # Check if diagonal movement is blocked by walls
                if dr != 0 and dc != 0:
                    # Check if both adjacent cells are walkable
                    if not self._is_walkable(row + dr, col) or not self._is_walkable(row, col + dc):
                        continue
                neighbors.append((new_row, new_col))

        return neighbors

    def __str__(self) -> str:
        """String representation of the maze."""
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if (i, j) == self.start:
                    row.append('S')
                elif (i, j) == self.goal:
                    row.append('G')
                elif self.grid[i, j] == 1:
                    row.append('#')
                else:
                    row.append('.')
            result.append(' '.join(row))
        return '\n'.join(result)

    def get_size(self) -> Tuple[int, int]:
        """Return the dimensions of the maze."""
        return (self.rows, self.cols)


class MazeGenerator:
    """Utility class for generating different types of mazes."""

    @staticmethod
    def random_maze(rows: int, cols: int, wall_probability: float = 0.3) -> Maze:
        """
        Generate a random maze with walls.

        Args:
            rows: Number of rows
            cols: Number of columns
            wall_probability: Probability of a cell being a wall (0-1)

        Returns:
            Maze object with random walls
        """
        maze = Maze(rows, cols)
        for i in range(rows):
            for j in range(cols):
                if np.random.random() < wall_probability:
                    try:
                        maze.add_wall(i, j)
                    except ValueError:
                        # Skip if start or goal
                        continue
        return maze

    @staticmethod
    def spiral_maze(rows: int, cols: int) -> Maze:
        """Generate a spiral pattern maze."""
        maze = Maze(rows, cols)

        # Create a simple spiral pattern
        top, bottom = 0, rows - 1
        left, right = 0, cols - 1

        while top < bottom and left < right:
            # Top row
            for j in range(left, right + 1):
                if (top, j) != maze.start and (top, j) != maze.goal:
                    maze.add_wall(top, j)
            top += 1

            # Right column
            for i in range(top, bottom + 1):
                if (i, right) != maze.start and (i, right) != maze.goal:
                    maze.add_wall(i, right)
            right -= 1

            # Bottom row
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    if (bottom, j) != maze.start and (bottom, j) != maze.goal:
                        maze.add_wall(bottom, j)
                bottom -= 1

            # Left column
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    if (i, left) != maze.start and (i, left) != maze.goal:
                        maze.add_wall(i, left)
                left += 1

        return maze

    @staticmethod
    def maze_with_obstacles(rows: int, cols: int) -> Maze:
        """Create a maze with specific obstacle patterns."""
        maze = Maze(rows, cols)

        # Add vertical wall
        for i in range(rows // 3, 2 * rows // 3):
            if (i, cols // 2) != maze.start and (i, cols // 2) != maze.goal:
                maze.add_wall(i, cols // 2)

        # Add horizontal wall
        for j in range(cols // 3, 2 * cols // 3):
            if (rows // 2, j) != maze.start and (rows // 2, j) != maze.goal:
                maze.add_wall(rows // 2, j)

        return maze