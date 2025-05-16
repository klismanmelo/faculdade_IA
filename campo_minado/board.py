import random

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

class Board:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

        self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mines_positions = random.sample(positions, self.num_mines)
        for r, c in mines_positions:
            self.grid[r][c].is_mine = True

    def _calculate_adjacent_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c].is_mine:
                    neighbors = self.get_neighbors(r, c)
                    count = sum(1 for n in neighbors if n.is_mine)
                    self.grid[r][c].adjacent_mines = count

    def get_neighbors(self, row, col):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if (dr != 0 or dc != 0) and 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append(self.grid[nr][nc])
        return neighbors

    def reveal_cell(self, row, col):
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        # Se não tiver minas adjacentes, revela os vizinhos recursivamente
        if cell.adjacent_mines == 0 and not cell.is_mine:
            for neighbor in self.get_neighbors(row, col):
                if not neighbor.is_revealed and not neighbor.is_mine:
                    self.reveal_cell(neighbor.row, neighbor.col)
