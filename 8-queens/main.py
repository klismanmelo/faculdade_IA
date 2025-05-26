# main.py

import pygame
from game import Game
import os

pygame.init()
WIN = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Problema das 8 Rainhas")

# Carregar imagem da rainha
queen_img = pygame.image.load(os.path.join("./8-queens/queen.png"))

def main():
    clock = pygame.time.Clock()
    game = Game(WIN, queen_img)

    running = True
    while running:
        clock.tick(60)
        game.draw_board()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.place_queen(pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    conflitos = game.testar_colisoes()
                    print(f"⚔️ Rainhas se atacando: {conflitos}")

                elif event.key == pygame.K_r:
                    game.resolver_com_algoritmo()

    pygame.quit()

if __name__ == "__main__":
    main()
