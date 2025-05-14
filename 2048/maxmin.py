# maxmin.py
import copy
from game_2048 import move_left, move_right, move_up, move_down

def simulate_move(board, direction):
    move_funcs = {
        'left': move_left,
        'right': move_right,
        'up': move_up,
        'down': move_down
    }
    if direction in move_funcs:
        return move_funcs[direction](copy.deepcopy(board))
    return board, False

def get_available_moves(board):
    moves = []
    for direction in ['left', 'right', 'up', 'down']:
        new_board, moved = simulate_move(board, direction)
        if moved:
            moves.append((direction, new_board))
    return moves

def evaluate(board):
    empty_cells = sum(row.count(0) for row in board)
    max_tile = max(max(row) for row in board)
    total = sum(sum(row) for row in board)
    return empty_cells * 10 + max_tile + total * 0.1

def maxmin(board, depth):
    if depth == 0:
        return None, evaluate(board), {}

    best_score = float('-inf')
    best_move = None
    move_scores = {}

    for direction, new_board in get_available_moves(board):
        _, score, _ = maxmin(new_board, depth - 1)
        move_scores[direction] = score
        if score > best_score:
            best_score = score
            best_move = direction

    return best_move, best_score, move_scores

def get_maxmin_move(board, depth=2):
    move, score, move_scores = maxmin(board, depth)
    return move, score, move_scores
