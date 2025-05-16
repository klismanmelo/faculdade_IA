# montecarlo.py
import random
import copy
from game_2048 import (
    move_left, move_right, move_up, move_down,
    add_random_tile, has_moves
)

def simulate_move(board, direction):
    funcs = {
        'left': move_left,
        'right': move_right,
        'up': move_up,
        'down': move_down
    }
    return funcs[direction](copy.deepcopy(board))

def get_valid_moves(board):
    directions = ['left', 'right', 'up', 'down']
    valid = []
    for direction in directions:
        new_board, moved = simulate_move(board, direction)
        if moved:
            valid.append((direction, new_board))
    return valid

def evaluate(board):
    empty_cells = sum(row.count(0) for row in board)
    max_tile = max(max(row) for row in board)
    corner_bonus = 0
    if board[0][0] == max_tile or board[0][3] == max_tile or board[3][0] == max_tile or board[3][3] == max_tile:
        corner_bonus = 50

    return (
        max_tile * 1.0 +
        empty_cells * 5 +
        corner_bonus +
        sum(sum(row) for row in board) * 0.01
    )

def guided_rollout(board, max_depth=100):
    board = copy.deepcopy(board)
    for _ in range(max_depth):
        if not has_moves(board):
            break
        moves = get_valid_moves(board)
        if not moves:
            break

        # Estratégia: priorizar esquerda > cima > direita > baixo
        priority = ['left', 'up', 'right', 'down']
        best = None
        for p in priority:
            for d, new_b in moves:
                if d == p:
                    best = (d, new_b)
                    break
            if best:
                break
        if not best:
            best = random.choice(moves)

        board = best[1]
        add_random_tile(board)

    return evaluate(board)

def get_montecarlo_move(board, simulations=100):
    valid_moves = get_valid_moves(board)
    if not valid_moves:
        return None, 0, {}

    move_scores = {}
    for direction, move_board in valid_moves:
        total_score = 0
        for _ in range(simulations):
            sim_board = copy.deepcopy(move_board)
            add_random_tile(sim_board)
            total_score += guided_rollout(sim_board)
        average_score = total_score / simulations
        move_scores[direction] = average_score

    best_move = max(move_scores, key=move_scores.get)
    return best_move, move_scores[best_move], move_scores
