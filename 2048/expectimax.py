# expectimax.py
import random
from game_2048 import move_left, move_right, move_up, move_down

def get_possible_moves(board):
    moves = {
        'left': move_left,
        'right': move_right,
        'up': move_up,
        'down': move_down
    }
    valid_moves = {}
    for direction, func in moves.items():
        new_board, moved = func(board)
        if moved:
            valid_moves[direction] = new_board
    return valid_moves

def evaluate_board(board):
    # Heurística simples: soma dos valores + maior valor
    return sum(sum(row) for row in board) + max(max(row) for row in board)

def expectimax(board, depth, is_max=True):
    if depth == 0:
        return evaluate_board(board)

    if is_max:
        max_score = float('-inf')
        for _, new_board in get_possible_moves(board).items():
            score = expectimax(new_board, depth - 1, is_max=False)
            max_score = max(max_score, score)
        return max_score
    else:
        # Expectativa dos próximos estados com tiles 2 e 4
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if not empty_cells:
            return evaluate_board(board)

        total_score = 0
        for i, j in empty_cells:
            for value, prob in [(2, 0.9), (4, 0.1)]:
                board[i][j] = value
                total_score += prob * expectimax(board, depth - 1, is_max=True)
                board[i][j] = 0
        return total_score / len(empty_cells)

def get_expectimax_move(board, depth=3):
    moves = get_possible_moves(board)
    move_scores = {}

    for move, new_board in moves.items():
        score = expectimax(new_board, depth - 1, is_max=False)
        move_scores[move] = score

    if not move_scores:
        return None, 0, {}

    best_move = max(move_scores, key=move_scores.get)
    return best_move, move_scores[best_move], move_scores
