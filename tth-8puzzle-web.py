import streamlit as st
from PIL import Image
import cv2
import numpy as np
import random
from search import astar_search, EightPuzzle
import time

# Load and process the image
def load_image():
    image = cv2.imread('22110139.jpeg')
    parse_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(parse_image)
    return pil_image

# Initialize the puzzle pieces
def initialize_pieces():
    pil_image = load_image()
    piece_width = pil_image.width // 3
    piece_height = pil_image.height // 3
    pieces = []
    white = Image.new('RGB', (piece_width, piece_height), (255, 255, 255))  # Blank piece

    # Cut image pieces
    for row in range(3):
        for col in range(3):
            if row == 2 and col == 2:
                break  # Skip the last piece (white space)
            upper = row * piece_height
            lower = upper + piece_height
            left = col * piece_width
            right = left + piece_width
            piece = pil_image.crop((left, upper, right, lower))
            pieces.append(piece)

    # Add the blank piece at the end
    pieces.append(white)
    return pieces

# Initialize session state
if "state" not in st.session_state:
    st.session_state.state = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # Blank at the end (index 8)
if "puzzle" not in st.session_state:
    st.session_state.puzzle = EightPuzzle(tuple(st.session_state.state))
if "pieces" not in st.session_state:
    st.session_state.pieces = initialize_pieces()
if "state_pieces" not in st.session_state:
    st.session_state.state_pieces = {
        st.session_state.state[i]: st.session_state.pieces[i] for i in range(9)
    }

# Render the puzzle
def render_puzzle():
    piece_width, piece_height = st.session_state.pieces[0].size
    canvas = Image.new("RGB", (piece_width * 3, piece_height * 3), (255, 255, 255))

    # Bước 1: Đưa key 0 lên đầu dãy
    # Hoán đổi ảnh của key 0 và key 1
    st.session_state.state_pieces[0], st.session_state.state_pieces[1] = st.session_state.state_pieces[1], st.session_state.state_pieces[0]

    # Bước 2: Thực hiện hoán đổi giá trị ảnh theo quy trình vòng lặp
    # Tạo một bản sao của dãy ảnh ban đầu để dễ dàng hoán đổi
    temp_pieces = st.session_state.state_pieces.copy()
    
    for i in range(9):
        # Hoán đổi ảnh theo thứ tự: key 0 -> ảnh 8, key 1 -> ảnh 2, ..., key 8 -> ảnh 0
        st.session_state.state_pieces[i] = temp_pieces[(i + 1) % 9]

    st.session_state.state_pieces[0], st.session_state.state_pieces[8] = st.session_state.state_pieces[8], st.session_state.state_pieces[0]

    for i, piece in st.session_state.state_pieces.items():
        x, y = i % 3, i // 3
        canvas.paste(piece, (x * piece_width, y * piece_height))

    return canvas

# Scramble the puzzle
def scramble():
    possible_actions = ["UP", "DOWN", "LEFT", "RIGHT"]
    scramble_moves = [random.choice(possible_actions) for _ in range(60)]  # Randomize moves

    for move in scramble_moves:
        if move in st.session_state.puzzle.actions(st.session_state.state):
            st.session_state.state = list(
                st.session_state.puzzle.result(st.session_state.state, move)
            )

    st.session_state.puzzle = EightPuzzle(tuple(st.session_state.state))  # Update puzzle state
    st.session_state.state_pieces = {
        st.session_state.state[i]: st.session_state.pieces[i] for i in range(9)
    }  # Update the state of the pieces
    st.rerun()  # Refresh the page to update the state

# Solve the puzzle step-by-step
def solve_steps():
    solution = astar_search(st.session_state.puzzle).solution()
    for move in solution:
        st.session_state.state = list(
            st.session_state.puzzle.result(st.session_state.state, move)
        )
        st.session_state.puzzle = EightPuzzle(tuple(st.session_state.state))
        st.session_state.state_pieces = {
            st.session_state.state[i]: st.session_state.pieces[i] for i in range(9)
        }

        # Show the puzzle after each step
        st.subheader("Puzzle Grid")
        puzzle_image = render_puzzle()
        st.image(puzzle_image, caption="Current Puzzle State")
        time.sleep(0.75)  # Simulate step-by-step solving delay

# Move tiles manually
def exchange(index):
    zero_ix = st.session_state.state.index(0)
    actions = st.session_state.puzzle.actions(st.session_state.state)

    i_diff = index // 3 - zero_ix // 3
    j_diff = index % 3 - zero_ix % 3
    current_action = ""

    if i_diff == 1:
        current_action += "DOWN"
    elif i_diff == -1:
        current_action += "UP"
    if j_diff == 1:
        current_action += "RIGHT"
    elif j_diff == -1:
        current_action += "LEFT"

    if abs(i_diff) + abs(j_diff) != 1:
        current_action = ""  # Invalid move if not adjacent

    if current_action in actions:
        st.session_state.state = list(
            st.session_state.puzzle.result(st.session_state.state, current_action)
        )
        st.session_state.state_pieces[zero_ix], st.session_state.state_pieces[index] = (
            st.session_state.state_pieces[index],
            st.session_state.state_pieces[zero_ix],
        )
        st.session_state.puzzle = EightPuzzle(tuple(st.session_state.state))

# Streamlit app
st.title("8-Puzzle Solver")

# Display the puzzle
st.subheader("Trần Trung Hiếu - 22110139")
puzzle_image = render_puzzle()
st.image(puzzle_image, caption="Current Puzzle State")

st.sidebar.title("Functionality:")

# Scramble Button
if st.sidebar.button("Scramble"):
    scramble()  # Perform the scramble when clicked

if st.sidebar.button("Solve"):
    solve_steps()

if st.sidebar.button("Reset"):
    st.session_state.state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    st.session_state.puzzle = EightPuzzle(tuple(st.session_state.state))
    st.session_state.state_pieces = {
        st.session_state.state[i]: st.session_state.pieces[i] for i in range(9)
    }

# Manual exchange
st.sidebar.subheader("Click a tile to move it")
# Create a grid of buttons in the sidebar
rows = 3
cols = 3
buttons = []
for i in range(rows):
    # Create a row with 3 columns
    col1, col2, col3 = st.sidebar.columns(3)
    
    # Place the buttons in each column for the current row
    for j in range(cols):
        idx = i * 3 + j  # Calculate the index of the tile
        if st.session_state.state[idx] != 0:  # Don't show a button for the blank space
            if j == 0:
                col1.button(f"Tile {st.session_state.state[idx]}", key=f"tile_{idx}", on_click=lambda idx=idx: exchange(idx))
            elif j == 1:
                col2.button(f"Tile {st.session_state.state[idx]}", key=f"tile_{idx}", on_click=lambda idx=idx: exchange(idx))
            else:
                col3.button(f"Tile {st.session_state.state[idx]}", key=f"tile_{idx}", on_click=lambda idx=idx: exchange(idx))
        else:
            if j == 0:
                col1.button("Blank", key="blank")  # Button for the blank space
            elif j == 1:
                col2.button("Blank", key="blank")  # Button for the blank space
            else:
                col3.button("Blank", key="blank")  # Button for the blank space
