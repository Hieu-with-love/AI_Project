import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import random
import time
from functools import partial
from search import astar_search, EightPuzzle
import sys
import os

# Ensure the proper path is set for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Initial state of the puzzle
state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
puzzle = EightPuzzle(tuple(state))
solution = None
solution_states = []  # List to store the solution states

# UI components
b = [None] * 9

# Load and process image
image = cv2.imread('22110139.jpeg')
parse_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pil_image = Image.fromarray(parse_image)

# Size of each piece
piece_width = pil_image.width // 3
piece_height = pil_image.height // 3

# Array to store the puzzle pieces
pieces = []
state_pieces = {}

# White piece (empty space)
white = Image.new('RGB', (piece_width, piece_height), (255, 255, 255))
piece_number = 0

# Create puzzle pieces
for row in range(3):
    for col in range(3):
        upper = row * piece_height
        lower = upper + piece_height
        left = col * piece_width
        right = left + piece_width

        if col == 2 and row == 2:
            break  # Skip the last piece (white)

        piece = pil_image.crop((left, upper, right, lower))
        pieces.append(piece)
        state_pieces[piece_number] = piece
        piece_number += 1

pieces.append(white)
pieces = pieces[1:] + [pieces[0]]

# Initialize the main Tkinter window
root = tk.Tk()
root.title('8 Puzzle')


# Scramble the puzzle
def scramble():
    global state, state_pieces, pieces, puzzle
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    scramble_moves = [random.choice(possible_actions) for _ in range(60)]

    for move in scramble_moves:
        if move in puzzle.actions(state):
            state = list(puzzle.result(state, move))
    
    puzzle = EightPuzzle(tuple(state))
    state_pieces = {state[i]: pieces[i] for i in range(9)}
    create_GUI()
    print("Scrambled state:", state)


# Solve the puzzle using A* search
def problem_solve():
    return astar_search(puzzle).solution()


def solve_steps():
    global state, solution, puzzle, state_pieces, pieces, solution_states
    solution = problem_solve()
    solution_states = []  # Reset solution states
    print("Solution steps:", solution)

    for move in solution:
        state = list(puzzle.result(state, move))
        solution_states.append(list(state))  # Save the state after each move
        puzzle = EightPuzzle(tuple(state))
        state_pieces = {state[i]: pieces[i] for i in range(9)}
        create_GUI()
        root.update()
        time.sleep(0.75)


# Exchange tiles
def exchange(index):
    global state, solution, puzzle, state_pieces, pieces
    zero_ix = state.index(0)
    actions = puzzle.actions(state)

    i_diff = index // 3 - zero_ix // 3
    j_diff = index % 3 - zero_ix % 3
    current_action = ''

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
        state = list(puzzle.result(state, current_action))
        state_pieces[zero_ix], state_pieces[index] = state_pieces[index], state_pieces[zero_ix]
        puzzle = EightPuzzle(tuple(state))
        create_GUI()


# Create buttons for the puzzle grid
def create_GUI():
    new_size = (150, 200)
    for i, piece in state_pieces.items():
        piece.thumbnail(new_size)
        tk_piece = ImageTk.PhotoImage(piece)

        b[i] = tk.Button(root, image=tk_piece, width=150, command=partial(exchange, i))
        b[i].grid(row=i // 3, column=i % 3)
        b[i].image = tk_piece


# Create static buttons (Scramble, Solve, Show Solution)
def create_function_buttons():
    scramble_btn = ttk.Button(root, text='Scramble', width=8, command=scramble)
    scramble_btn.grid(row=3, column=0, ipady=10, sticky=tk.EW)

    run_btn = ttk.Button(root, text='Run', width=8, command=solve_steps)
    run_btn.grid(row=3, column=2, ipady=10, sticky=tk.EW)

    show_solution_btn = ttk.Button(root, text='Show Solution', width=8, command=show_solution)
    show_solution_btn.grid(row=4, column=1, ipady=10, sticky=tk.EW)


# Function to display the solution
def show_solution():
    global solution_states
    if solution_states:
        for state in solution_states:
            print("State:", state)
            # Here, you could also display each state visually if desired
            # For now, we are just printing the states
            time.sleep(1)
    else:
        print("No solution available")


# Initialize the puzzle
def init():
    global state, solution, puzzle, pieces, state_pieces
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    scramble()
    create_GUI()
    create_function_buttons()


# Start the application
init()
root.mainloop()
