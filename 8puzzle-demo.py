"""
    Bài làm mô phỏng bài toán N-Puzzle, với giá trị N được truyền vào class Puzzle để giải quyết bài toán
    Là bài ví dụ tiền đề cho minh hoạt trên tkinter và streamlit
"""

"""
    Khởi tạo Node - một Node sẽ đại diện cho một trạng thái trong bảng 8-Puzzle
    biến data: Lưu ma trận hiện tại của bảng
    biến level: lưu số bước đi từ trạng thái bắt đầu đến trạng thái hiện tại (g-score)
    fval: Hàm heuristic tính tổng f(x) = g(x) + h(x) 
                                  Với h(x) là số ô bị sai so với trạng thái mục tiêu (Goal State)
                                  Và g(x) là số nút đã duyệt (Nếu như mới khởi tại -> g(x) = 0)
"""


class Node:
    def __init__(self, data, level, fval):
        """Initialize the node with data, level of the node, and calculated fvalue."""
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        """Generate child nodes from the given node by moving the blank space
           in the four directions: up, down, left, right."""
        x, y = self.find(self.data, '_')
        # List of possible positions to move the blank space: [up, down, left, right]
        val_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """Move the blank space in the specified direction. Return None if out of bounds."""
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp_puz[x2][y2], temp_puz[x1][y1] = temp_puz[x1][y1], temp_puz[x2][y2]
            return temp_puz
        else:
            return None

    def copy(self, root):
        """Create a copy of the given matrix."""
        return [row[:] for row in root]

    def find(self, puz, x):
        """Find the position of the blank space."""
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if puz[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, size):
        """Initialize the puzzle size, open list, and closed list."""
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """Accepts the puzzle matrix input from the user."""
        puz = []
        for i in range(self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self, start, goal):
        """Heuristic function: f(x) = h(x) + g(x)"""
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        """Calculate heuristic value by counting misplaced tiles."""
        temp = 0
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def process(self):
        """Accept start and goal puzzle states and solve the puzzle."""
        print("Enter the start state matrix:")
        start = self.accept()
        print("Enter the goal state matrix:")
        goal = self.accept()

        start_node = Node(start, 0, 0)
        start_node.fval = self.f(start_node, goal)
        self.open.append(start_node)

        while True:
            cur = self.open[0]
            print("\nCurrent state:\n")
            for row in cur.data:
                print(" ".join(row))

            # Goal check
            if self.h(cur.data, goal) == 0:
                print("Goal reached!")
                break

            # Generate and add child nodes to open list
            for child in cur.generate_child():
                child.fval = self.f(child, goal)
                self.open.append(child)
            self.closed.append(cur)
            del self.open[0]

            # Sort open list based on f values
            self.open.sort(key=lambda x: x.fval)


# Example usage
puz = Puzzle(3)
puz.process()
