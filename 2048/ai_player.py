# ai_player.py
from config import ALGORITHM
from maxmin import get_maxmin_move
from expectimax import get_expectimax_move
from montecarlo import get_montecarlo_move

def get_ai_move(board, depth=3):
    if ALGORITHM == "maxmin":
        return get_maxmin_move(board, depth)
    elif ALGORITHM == "expectimax":
        return get_expectimax_move(board, depth)
    elif ALGORITHM == "montecarlo":
        return get_montecarlo_move(board)
    else:
        raise ValueError("Algoritmo inválido selecionado.")
