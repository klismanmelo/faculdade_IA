# game.py

import pygame
from setting import ALGORITMO_SELECIONADO

# Importação condicional com base na escolha
if ALGORITMO_SELECIONADO == "subida":
    from subida import subida_de_encosta_com_reinicio
elif ALGORITMO_SELECIONADO == "tempera":
    from tempera import tempera_simulada
elif ALGORITMO_SELECIONADO == "genetico":
    from generico import algoritmo_genetico

# Dimensões
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Cores
WHITE = (255, 255, 255)
GRAY = (125, 135, 150)
BLUE = (100, 100, 255)

class Game:
    def __init__(self, win, queen_img):
        self.win = win
        self.queen_img = pygame.transform.scale(queen_img, (SQUARE_SIZE, SQUARE_SIZE))
        self.board = [-1 for _ in range(8)]  # Inicialmente sem rainhas

    def draw_board(self):
        self.win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = WHITE
                else:
                    color = GRAY
                pygame.draw.rect(self.win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                if self.board[col] == row:
                    self.win.blit(self.queen_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def place_queen(self, pos):
        x, y = pos
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        if self.board[col] == row:
            self.board[col] = -1
        else:
            self.board[col] = row

    def testar_colisoes(self):
        # Conta conflitos entre rainhas
        conflitos = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if self.board[i] == -1 or self.board[j] == -1:
                    continue
                if self.board[i] == self.board[j] or abs(self.board[i] - self.board[j]) == abs(i - j):
                    conflitos += 1
        return conflitos

    def resolver_com_algoritmo(self):
        if ALGORITMO_SELECIONADO == "subida":
            solucao = subida_de_encosta_com_reinicio()
        elif ALGORITMO_SELECIONADO == "tempera":
            solucao = tempera_simulada()
        elif ALGORITMO_SELECIONADO == "genetico":
            solucao = algoritmo_genetico()
        else:
            print("Algoritmo não reconhecido.")
            return

        self.board = solucao

