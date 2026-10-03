"""
Visualization module for maze and search results.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import List, Tuple, Optional
from maze import Maze


class MazeVisualizer:
    """
    Visualize maze, search process, and final path.
    """
    
    def __init__(self, maze: Maze, figsize: Tuple[int, int] = (10, 10)):
        """
        Initialize visualizer.
        
        Args:
            maze: Maze object to visualize
            figsize: Figure size (width, height)
        """
        self.maze = maze
        self.figsize = figsize
        self.fig = None
        self.ax = None
        
        # Color scheme
        self.colors = {
            'empty': 'white',
            'wall': 'black',
            'start': 'green',
            'goal': 'red',
            'explored': 'lightblue',
            'path': 'yellow',
            'frontier': 'orange'
        }
    
    def _setup_plot(self):
        """Setup the matplotlib figure and axes."""
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.5, self.maze.cols - 0.5)
        self.ax.set_ylim(-0.5, self.maze.rows - 0.5)
        self.ax.grid(True, linestyle='-', linewidth=0.5, color='gray')
        self.ax.set_facecolor('white')
    
    def _draw_cell(self, row: int, col: int, color: str, alpha: float = 1.0, 
                   edgecolor: str = 'lightgray', linewidth: float = 0.5):
        """Draw a single cell with given color."""
        rect = patches.Rectangle(
            (col - 0.5, row - 0.5), 1, 1,
            facecolor=color,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=alpha
        )
        self.ax.add_patch(rect)
    
    def _draw_maze_background(self):
        """Draw the maze background with walls."""
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                if self.maze.grid[i, j] == 1:
                    self._draw_cell(i, j, self.colors['wall'])
                else:
                    self._draw_cell(i, j, self.colors['empty'])
    
    def _draw_start_goal(self):
        """Draw start and goal positions."""
        start_row, start_col = self.maze.start
        goal_row, goal_col = self.maze.goal
        
        # Start
        rect = patches.Rectangle(
            (start_col - 0.5, start_row - 0.5), 1, 1,
            facecolor=self.colors['start'],
            edgecolor='darkgreen',
            linewidth=2
        )
        self.ax.add_patch(rect)
        self.ax.text(start_col, start_row, 'S', 
                    ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Goal
        rect = patches.Rectangle(
            (goal_col - 0.5, goal_row - 0.5), 1, 1,
            facecolor=self.colors['goal'],
            edgecolor='darkred',
            linewidth=2
        )
        self.ax.add_patch(rect)
        self.ax.text(goal_col, goal_row, 'G', 
                    ha='center', va='center', fontsize=12, fontweight='bold')
    
    def _draw_explored(self, explored: List[Tuple[int, int]]):
        """Draw explored nodes."""
        for row, col in explored:
            if (row, col) != self.maze.start and (row, col) != self.maze.goal:
                if self.maze.grid[row, col] == 0:  # Only draw empty cells
                    self._draw_cell(row, col, self.colors['explored'], alpha=0.5)
    
    def _draw_path(self, path: List[Tuple[int, int]]):
        """Draw the final path."""
        for row, col in path:
            if (row, col) != self.maze.start and (row, col) != self.maze.goal:
                self._draw_cell(row, col, self.colors['path'])
    
    def visualize(self, path: Optional[List[Tuple[int, int]]] = None,
                  explored: Optional[List[Tuple[int, int]]] = None,
                  show_explored: bool = True,
                  title: str = "Maze Solver - A* Search",
                  save_path: Optional[str] = None,
                  show_legend: bool = True):
        """
        Visualize the maze with path and explored nodes.
        
        Args:
            path: Path from start to goal
            explored: List of explored nodes
            show_explored: Whether to show explored nodes
            title: Plot title
            save_path: Path to save the figure (optional)
            show_legend: Whether to show legend
        """
        self._setup_plot()
        
        # Draw maze background
        self._draw_maze_background()
        
        # Draw explored nodes
        if explored and show_explored:
            self._draw_explored(explored)
        
        # Draw path
        if path:
            self._draw_path(path)
        
        # Draw start and goal (on top)
        self._draw_start_goal()
        
        # Add title
        self.ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add legend
        if show_legend:
            legend_elements = [
                patches.Patch(facecolor=self.colors['start'], label='Start'),
                patches.Patch(facecolor=self.colors['goal'], label='Goal'),
                patches.Patch(facecolor=self.colors['wall'], label='Wall'),
                patches.Patch(facecolor=self.colors['empty'], label='Empty'),
                patches.Patch(facecolor=self.colors['explored'], alpha=0.5, label='Explored'),
                patches.Patch(facecolor=self.colors['path'], label='Path')
            ]
            self.ax.legend(handles=legend_elements, loc='upper right', 
                          bbox_to_anchor=(1.15, 1))
        
        # Add statistics text if path exists
        if path:
            stats_text = f"Path Length: {len(path)-1} steps\nNodes Explored: {len(explored) if explored else 0}"
            self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes,
                        fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        
        # Save figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📁 Figure saved to: {save_path}")
        
        plt.show()
    
    def visualize_search_step(self, explored: List[Tuple[int, int]], 
                             frontier: List[Tuple[int, int]],
                             step: int,
                             save_path: Optional[str] = None):
        """
        Visualize a step in the search process.
        
        Args:
            explored: List of explored nodes
            frontier: List of frontier nodes (in open set)
            step: Step number
            save_path: Path to save the figure (optional)
        """
        self._setup_plot()
        
        # Draw maze background
        self._draw_maze_background()
        
        # Draw explored nodes
        for row, col in explored:
            if (row, col) != self.maze.start and (row, col) != self.maze.goal:
                if self.maze.grid[row, col] == 0:
                    self._draw_cell(row, col, self.colors['explored'], alpha=0.5)
        
        # Draw frontier
        for row, col in frontier:
            if (row, col) != self.maze.start and (row, col) != self.maze.goal:
                if self.maze.grid[row, col] == 0:
                    self._draw_cell(row, col, self.colors['frontier'], alpha=0.7)
        
        # Draw start and goal
        self._draw_start_goal()
        
        # Add title
        self.ax.set_title(f"Search Step {step}", fontsize=14, fontweight='bold', pad=20)
        
        # Add legend
        legend_elements = [
            patches.Patch(facecolor=self.colors['start'], label='Start'),
            patches.Patch(facecolor=self.colors['goal'], label='Goal'),
            patches.Patch(facecolor=self.colors['wall'], label='Wall'),
            patches.Patch(facecolor=self.colors['explored'], alpha=0.5, label='Explored'),
            patches.Patch(facecolor=self.colors['frontier'], alpha=0.7, label='Frontier')
        ]
        self.ax.legend(handles=legend_elements, loc='upper right', 
                      bbox_to_anchor=(1.15, 1))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_animated_gif(self, steps: List[Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]],
                           output_path: str = "search_animation.gif",
                           fps: int = 5):
        """
        Create an animated GIF of the search process.
        
        Args:
            steps: List of (explored, frontier) tuples for each step
            output_path: Path to save the GIF
            fps: Frames per second
        """
        try:
            from PIL import Image
            import io
            
            images = []
            for i, (explored, frontier) in enumerate(steps):
                self._setup_plot()
                self._draw_maze_background()
                
                # Draw explored nodes
                for row, col in explored:
                    if (row, col) != self.maze.start and (row, col) != self.maze.goal:
                        if self.maze.grid[row, col] == 0:
                            self._draw_cell(row, col, self.colors['explored'], alpha=0.5)
                
                # Draw frontier
                for row, col in frontier:
                    if (row, col) != self.maze.start and (row, col) != self.maze.goal:
                        if self.maze.grid[row, col] == 0:
                            self._draw_cell(row, col, self.colors['frontier'], alpha=0.7)
                
                self._draw_start_goal()
                self.ax.set_title(f"Search Step {i+1}", fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                
                # Save to buffer
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                images.append(Image.open(buf))
                plt.close()
            
            # Save as GIF
            if images:
                images[0].save(output_path, save_all=True, append_images=images[1:],
                              duration=1000//fps, loop=0)
                print(f"🎬 Animation saved to: {output_path}")
                
        except ImportError:
            print("❌ PIL not installed. Install with: pip install pillow")
        except Exception as e:
            print(f"❌ Error creating animation: {e}")