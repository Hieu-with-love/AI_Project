import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import time
from functools import partial
from search import astar_search
from search import EightPuzzle

class Puzzle:
    def __init__(self, size):
        self.n = size
        self.puzzle = None
        self.goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # Trạng thái mục tiêu của 8-Puzzle

    def accept(self, start_state):
        """Chấp nhận trạng thái bắt đầu từ người dùng."""
        self.puzzle = EightPuzzle(tuple(start_state))

    def solve(self):
        """Giải quyết bài toán với thuật toán A*."""
        print("Giải quyết bài toán với A*...")
        solution = astar_search(self.puzzle)
        steps = [state for state in solution.path()]
        return steps


class PuzzleGUI:
    def __init__(self, root, puzzle):
        self.root = root
        self.puzzle = puzzle
        self.b = [None] * 9
        self.state = puzzle.goal
        self.steps = []
        self.current_step = 0
        self.create_gui()

    def scramble(self):
        """Chức năng trộn trạng thái puzzle."""
        self.state = [list(range(1, 9)) + [0]]
        random.shuffle(self.state)
        self.create_gui()

    def solve_steps(self):
        """Giải quyết bài toán."""
        self.steps = self.puzzle.solve()
        self.current_step = 0
        self.display_step()

    def display_step(self):
        """Hiển thị từng bước di chuyển."""
        if self.current_step < len(self.steps):
            self.state = self.steps[self.current_step]
            self.current_step += 1
            self.create_gui()
            self.root.after(500, self.display_step)  # Tự động chuyển sang bước tiếp theo sau 500ms

    def create_gui(self):
        """Tạo giao diện hiển thị trạng thái."""
        for i in range(9):
            row = i // 3
            col = i % 3
            if self.state[row][col] != 0:  # 0 là khoảng trống, không hiển thị
                self.b[i] = tk.Button(self.root, text=str(self.state[row][col]), width=10, height=3,
                                      command=partial(self.move_tile, i))
                self.b[i].grid(row=row, column=col)

    def move_tile(self, index):
        """Xử lý di chuyển các mảnh khi người dùng nhấn vào."""
        zero_index = self.state.index(0)
        row, col = index // 3, index % 3
        zero_row, zero_col = zero_index // 3, zero_index % 3

        # Kiểm tra xem mảnh có thể di chuyển với khoảng trống không
        if abs(row - zero_row) + abs(col - zero_col) == 1:
            # Swap mảnh với khoảng trống
            self.state[zero_row][zero_col], self.state[row][col] = self.state[row][col], self.state[zero_row][zero_col]
            self.create_gui()

    def reset(self):
        """Khôi phục trạng thái ban đầu."""
        self.state = self.puzzle.goal
        self.create_gui()


def start_app():
    """Khởi tạo ứng dụng Tkinter."""
    root = tk.Tk()
    root.title("8-Puzzle")

    puzzle = Puzzle(3)
    puzzle.accept([[1, 2, 3], [4, 5, 6], [7, 8, 0]])  # Trạng thái bắt đầu

    gui = PuzzleGUI(root, puzzle)

    # Tạo các nút chức năng
    scramble_button = ttk.Button(root, text="Scramble", width=8, command=gui.scramble)
    scramble_button.grid(row=3, column=0, ipady=10, sticky=tk.EW)

    solve_button = ttk.Button(root, text="Solve", width=8, command=gui.solve_steps)
    solve_button.grid(row=3, column=1, ipady=10, sticky=tk.EW)

    reset_button = ttk.Button(root, text="Reset", width=8, command=gui.reset)
    reset_button.grid(row=3, column=2, ipady=10, sticky=tk.EW)

    root.mainloop()


# Chạy ứng dụng
start_app()
