from typing import Optional, TYPE_CHECKING

from customtkinter import CTkCanvas

from vimaze.animator import MazeAnimator
from vimaze.configs import maze_animator_options
from vimaze.display import MazeDisplay
from vimaze.generator import MazeGraphGenerator
from vimaze.solver import MazeSolver
from vimaze.timer import Timer

if TYPE_CHECKING:
    from vimaze.ds.graph import Graph
    from vimaze.ds.graph import Node
    from vimaze.app import SolverApp


class Maze:
    def __init__(self, maze_canvas: CTkCanvas, app: 'SolverApp'):
        self.maze_canvas = maze_canvas

        self.app = app

        self.graph: Optional['Graph'] = None

        self.gen_algorithm: Optional[str] = None
        self.solving_algorithm: Optional[str] = None

        self.cols: Optional[int] = None
        self.rows: Optional[int] = None

        self.timer = Timer(self)
        self.displayer = MazeDisplay(self.maze_canvas)
        self.animator = MazeAnimator(self.maze_canvas, self.displayer, self)
        self.generator = MazeGraphGenerator(self.animator, self.timer)
        self.solver = MazeSolver(self.animator, self.timer)

    def gen_algo_maze(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.graph = self.generator.generate_maze_graph(rows, cols, self.gen_algorithm)

    def set_maze_gen_algorithm(self, value: str):
        self.gen_algorithm = value

    def set_maze_solving_algorithm(self, value: str):
        self.solving_algorithm = value

    def display_maze(self):
        self.displayer.display_maze(self)

    def display_path(self, nodes: list['Node']):
        self.displayer.display_path(nodes, maze_animator_options['solving']['defaults']['path_color'],
                                    maze_animator_options['solving']['defaults']['start_color'],
                                    maze_animator_options['solving']['defaults']['end_color'])

    def solve_maze(self, start_pos: tuple[int, int], end_pos: tuple[int, int]):
        self.solver.solve_maze(start_pos, end_pos, self.solving_algorithm, self.graph)
