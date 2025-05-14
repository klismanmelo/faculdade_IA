import pygame
import sys
##from visulize_ai_choice import show_move_evaluation

import os
import json
import matplotlib.pyplot as plt
from pygame import image as pg_image


from game_2048 import (
    init_board, draw_board, add_random_tile,
    move_left, move_right, move_up, move_down,
    has_2048, has_moves
)
from ai_player import get_ai_move

pygame.init()

SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = SIZE * (TILE_SIZE + MARGIN) + MARGIN
HEIGHT = WIDTH

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 AI (Espaço para jogar)')
clock = pygame.time.Clock()

def apply_move(board, move):
    if move == 'left':
        return move_left(board)
    elif move == 'right':
        return move_right(board)
    elif move == 'up':
        return move_up(board)
    elif move == 'down':
        return move_down(board)
    return board, False

import time

def main():
    board = init_board()
    log_data = {
        "timeline_scores": [],
        "chosen_moves": [],
        "board_snapshots": [],
    }

    draw_board(board)
    last_move_time = time.time()
    delay = 0.2  # tempo em segundos entre jogadas

    while True:
        clock.tick(60)  # mantém 60 FPS para suavidade

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Jogada automática da IA a cada `delay` segundos
        if time.time() - last_move_time >= delay:
            move, score, move_scores = get_ai_move(board, depth=3)

            if move:
                #show_move_evaluation(move_scores, move)

                new_board, moved = apply_move(board, move)
                if moved:
                    board = new_board
                    add_random_tile(board)
                    draw_board(board)
                    log_data["timeline_scores"].append(score)
                    log_data["chosen_moves"].append(move)
                    log_data["board_snapshots"].append([row[:] for row in board])  # cópia do estado

                    print(f"IA jogou: {move}, score esperado: {score}")
                else:
                    print(f"Jogada '{move}' não teve efeito.")

            else:
                print("Sem jogadas válidas.")

            # Atualiza o tempo da última jogada
            last_move_time = time.time()

            # Checagens de fim de jogo
            if has_2048(board):
                save_game_log(log_data, board)
                print("Pressione qualquer tecla para sair...")
                wait_for_key()
                pygame.quit()
                sys.exit()

            elif not has_moves(board):
                save_game_log(log_data, board)
                print("IA perdeu! Sem movimentos possíveis.")
                print("Pressione qualquer tecla para sair...")
                wait_for_key()
                pygame.quit()
                sys.exit()


def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return


def save_game_log(log_data, board):
    os.makedirs("logs", exist_ok=True)

    # Salvar gráfico da timeline
    plt.figure(figsize=(8, 4))
    plt.plot(log_data["timeline_scores"], marker='o', color='blue')
    plt.title("Timeline de decisões da IA")
    plt.xlabel("Jogada")
    plt.ylabel("Score da heurística")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig("logs/timeline.png")
    plt.close()

    # Salvar print do estado final do tabuleiro
    pg_image.save(screen, "logs/final_board.png")

    # Salvar resumo da partida
    highest_tile = max(max(row) for row in board)
    summary = {
        "total_jogadas": len(log_data["chosen_moves"]),
        "maior_tile": highest_tile,
        "movimentos": log_data["chosen_moves"]
    }

    with open("logs/summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("\n🏁 Jogo finalizado.")
    print(f"🔢 Maior número alcançado: {highest_tile}")
    print("🧾 Logs salvos em: logs/")


if __name__ == "__main__":
    main()
