import pygame
from setting import ALGORITMO_SELECIONADO  # Importa a configuração do algoritmo selecionado

# Importação condicional dos módulos de algoritmos com base no algoritmo escolhido
if ALGORITMO_SELECIONADO == "subida":
    from subida import subida_de_encosta_com_reinicio  # Algoritmo de subida de encosta com reinício
elif ALGORITMO_SELECIONADO == "tempera":
    from tempera import tempera_simulada  # Algoritmo de tempera simulada
elif ALGORITMO_SELECIONADO == "genetico":
    from generico import algoritmo_genetico  # Algoritmo genético

# Definição das dimensões da janela e do tabuleiro
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS  # Tamanho de cada casa no tabuleiro (80x80)

# Definição de cores usadas no tabuleiro
WHITE = (255, 255, 255)
GRAY = (125, 135, 150)
BLUE = (100, 100, 255)

class Game:
    def __init__(self, win, queen_img):
        self.win = win  # Janela onde o jogo será desenhado
        # Redimensiona a imagem da rainha para o tamanho de uma casa do tabuleiro
        self.queen_img = pygame.transform.scale(queen_img, (SQUARE_SIZE, SQUARE_SIZE))
        # Representação do tabuleiro: lista com a linha onde a rainha está em cada coluna
        # Inicialmente, nenhuma rainha está posicionada (representado por -1)
        self.board = [-1 for _ in range(8)]

    def draw_board(self):
        self.win.fill(WHITE)  # Preenche o fundo com branco
        # Desenha as casas do tabuleiro alternando as cores (branco e cinza)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = WHITE
                else:
                    color = GRAY
                pygame.draw.rect(self.win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Desenha a rainha na posição se existir no tabuleiro
                if self.board[col] == row:
                    self.win.blit(self.queen_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def place_queen(self, pos):
        x, y = pos  # Obtém a posição do clique do mouse
        col = x // SQUARE_SIZE  # Calcula em qual coluna o clique ocorreu
        row = y // SQUARE_SIZE  # Calcula em qual linha o clique ocorreu
        # Se já existe uma rainha nessa posição, remove-a (seta para -1)
        if self.board[col] == row:
            self.board[col] = -1
        else:
            # Caso contrário, posiciona a rainha na linha clicada naquela coluna
            self.board[col] = row

    def testar_colisoes(self):
        # Conta o número de conflitos (ataques) entre rainhas no tabuleiro
        conflitos = 0
        for i in range(8):
            for j in range(i + 1, 8):
                # Se não há rainha em alguma das colunas, ignora
                if self.board[i] == -1 or self.board[j] == -1:
                    continue
                # Conflito se duas rainhas estiverem na mesma linha
                # ou na mesma diagonal (diferença absoluta entre linhas == diferença entre colunas)
                if self.board[i] == self.board[j] or abs(self.board[i] - self.board[j]) == abs(i - j):
                    conflitos += 1
        return conflitos  # Retorna a quantidade total de conflitos

    def resolver_com_algoritmo(self):
        # Executa o algoritmo escolhido para resolver o problema das 8 rainhas
        if ALGORITMO_SELECIONADO == "subida":
            solucao = subida_de_encosta_com_reinicio()
        elif ALGORITMO_SELECIONADO == "tempera":
            solucao = tempera_simulada()
        elif ALGORITMO_SELECIONADO == "genetico":
            solucao = algoritmo_genetico()
        else:
            print("Algoritmo não reconhecido.")
            return

        # Atualiza o tabuleiro com a solução encontrada pelo algoritmo
        self.board = solucao
