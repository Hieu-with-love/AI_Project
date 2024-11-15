import os.path
import random
import time
from functools import partial
from tkinter import *
from tkinter import ttk
import tkinter as tk
from search import astar_search, EightPuzzle
import sys

# Add the parent directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Initialize the GUI
root = Tk()
state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
puzzle = EightPuzzle(tuple(state))
solution = None
b = [None] * 9

root.title('8 Puzzle')
puzzle_gui = tk.Canvas(root, width=640, height=480, relief=tk.SUNKEN, border=1)

# TODO: Refactor into OOP, remove global variables

def scramble():
    """Scramble the puzzle by making random moves."""
    global state, puzzle
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    scramble = []

    for _ in range(60):
        scramble.append(random.choice(possible_actions))

    for move in scramble:
        if move in puzzle.actions(state):
            state = list(puzzle.result(state, move))

    puzzle = EightPuzzle(tuple(state))
    create_buttons()

def solve():
    """Solve the puzzle using the A* algorithm."""
    return astar_search(puzzle).solution()

def solve_steps():
    """Solve the puzzle step-by-step."""
    global puzzle, solution, state
    solution = solve()
    print(solution)

    for move in solution:
        state = puzzle.result(state, move)
        create_buttons()
        root.update()
        root.after(1, time.sleep(0.75))

def exchange(index):
    """Interchange the position of the selected tile with the zero tile under certain conditions."""
    global state, solution, puzzle

    zero_ix = list(state).index(0)
    actions = puzzle.actions(state)
    current_action = ''

    i_diff = index // 3 - zero_ix // 3
    j_diff = index % 3 - zero_ix % 3

    if i_diff == 1:
        current_action += 'DOWN'
    elif i_diff == -1:
        current_action += 'UP'

    if j_diff == 1:
        current_action += 'RIGHT'
    elif j_diff == -1:
        current_action += 'LEFT'

    if abs(i_diff) + abs(j_diff) != 1:
        current_action = ''

    if current_action in actions:
        b[zero_ix].grid_forget()
        b[zero_ix] = Button(
            root,
            text=f'{state[index]}',
            width=6,
            font=('Helvetica', 40, 'bold'),
            bg='lightyellow',
            command=partial(exchange, zero_ix)
        )
        b[zero_ix].grid(row=zero_ix // 3, column=zero_ix % 3, ipady=40)

        b[index].grid_forget()
        b[index] = Button(
            root,
            text=None,
            width=6,
            font=('Helvetica', 40, 'bold'),
            command=partial(exchange, index)
        )
        b[index].grid(row=index // 3, column=index % 3, ipady=40)

        state[zero_ix], state[index] = state[index], state[zero_ix]
        puzzle = EightPuzzle(tuple(state))

def create_buttons():
    """Create buttons for each tile in the puzzle."""
    for i in range(9):
        text = f'{state[i]}' if state[i] != 0 else None
        b[i] = Button(
            root,
            text=text,
            width=6,
            font=('Helvetica', 40, 'bold'),
            bg='lightyellow',
            command=partial(exchange, i)
        )
        b[i].grid(row=i // 3, column=i % 3, ipady=40)

def create_static_buttons():
    """Create static buttons for scramble and solve actions."""
    scramble_btn = ttk.Button(root, text='Scramble', width=8, command=scramble)
    scramble_btn.grid(row=3, column=0, ipady=10, sticky=tk.EW)

    run_btn = ttk.Button(root, text='Run', width=8, command=solve_steps)
    run_btn.grid(row=3, column=2, ipady=10, sticky=tk.EW)

def init():
    """Initialize the puzzle and the GUI."""
    global state, solution
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    scramble()
    create_buttons()
    create_static_buttons()

# Initialize and run the application
init()
root.mainloop()
