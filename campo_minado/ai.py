class MinesweeperAI:
    def __init__(self, board):
        self.board = board
        self.safe_moves = set()
        self.mine_flags = set()

    def analyze(self):
        self.safe_moves.clear()
        self.mine_flags.clear()

        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.grid[row][col]

                if cell.is_revealed and cell.adjacent_mines > 0:
                    neighbors = self.board.get_neighbors(row, col)
                    hidden = [n for n in neighbors if not n.is_revealed and not n.is_flagged]
                    flagged = [n for n in neighbors if n.is_flagged]

                    # Se já marcou todas as minas ao redor, o resto é seguro
                    if len(flagged) == cell.adjacent_mines:
                        for n in hidden:
                            self.safe_moves.add((n.row, n.col))

                    # Se o total de ocultos + sinalizados é igual ao número de minas, todos ocultos são minas
                    if len(hidden) + len(flagged) == cell.adjacent_mines:
                        for n in hidden:
                            self.mine_flags.add((n.row, n.col))

        return self.safe_moves, self.mine_flags
