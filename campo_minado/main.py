import pygame
import sys
import time
from board import Board
from ai import MinesweeperAI

# Configurações
WIDTH, HEIGHT = 600, 700
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
NUM_MINES = 10

# Cores
GRAY = (189, 189, 189)
DARK_GRAY = (120, 120, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campo Minado")
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 32)

board = Board(ROWS, COLS, NUM_MINES)
global ai
ai = MinesweeperAI(board)

game_over = False
game_won = False
start_time = time.time()
ai_enabled = True


def reset_game():
    global board, ai, game_over, game_won, start_time, ai_enabled
    board = Board(ROWS, COLS, NUM_MINES)
    ai = MinesweeperAI(board)
    game_over = False
    game_won = False
    start_time = time.time()
    # ai_enabled = False  # descomente se quiser desligar IA ao reiniciar


def draw_board():
    safe_moves, mine_flags = ai.analyze()

    for row in range(ROWS):
        for col in range(COLS):
            cell = board.grid[row][col]
            x, y = col * CELL_SIZE, row * CELL_SIZE + 100

            # Base da célula
            if cell.is_revealed:
                pygame.draw.rect(screen, DARK_GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))

            # Contorno
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

            # Destaque das jogadas seguras da IA
            if (row, col) in safe_moves and not cell.is_revealed:
                highlight = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4))
                highlight.set_alpha(100)
                highlight.fill(YELLOW)
                screen.blit(highlight, (x + 2, y + 2))

            # Números, minas e bandeiras
            if cell.is_revealed:
                if cell.is_mine:
                    pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)
                elif cell.adjacent_mines > 0:
                    text = font.render(str(cell.adjacent_mines), True, BLUE)
                    screen.blit(text, (x + 10, y + 5))
            elif cell.is_flagged:
                flag = font.render("⚑", True, RED)
                screen.blit(flag, (x + 5, y + 2))

def check_victory():
    for row in board.grid:
        for cell in row:
            if not cell.is_mine and not cell.is_revealed:
                return False
    return True

def draw_ui():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 100))
    pygame.draw.line(screen, BLACK, (0, 100), (WIDTH, 100), 2)

    elapsed_time = int(time.time() - start_time)
    timer_text = font.render(f"⏱ Tempo: {elapsed_time}s", True, BLACK)
    screen.blit(timer_text, (20, 20))

    flags_used = sum(cell.is_flagged for row in board.grid for cell in row)
    flags_text = font.render(f"🚩 Bandeiras: {flags_used}/{NUM_MINES}", True, BLACK)
    screen.blit(flags_text, (20, 60))

    pygame.draw.rect(screen, GREEN, (WIDTH - 140, 30, 120, 40))
    restart_text = font.render("Reiniciar", True, WHITE)
    screen.blit(restart_text, (WIDTH - 120, 40))

    btn_color = (0, 200, 0) if ai_enabled else (200, 0, 0)  # verde se True, vermelho se False
    pygame.draw.rect(screen, btn_color, (WIDTH - 140, 80, 80, 20))
    ai_text = font.render("IA Jogando: ON" if ai_enabled else "IA Jogando: OFF", True, WHITE)
    screen.blit(ai_text, (WIDTH - 130, 90))

    if game_over:
        msg = big_font.render("💥 Fim de jogo!", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 10))
    elif game_won:
        msg = big_font.render("🏆 Você venceu!", True, GREEN)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 10))

def ai_play():
    global ai, game_over

    if ai is None:
        ai = MinesweeperAI(board)

    jogou_algo = False
    safe_moves, mine_flags = ai.analyze()

    # Marcar bandeiras nas minas detectadas
    for (row, col) in mine_flags:
        cell = board.grid[row][col]
        if not cell.is_flagged:
            cell.toggle_flag()
            jogou_algo = True

    while True:
        jogadas_seguros = [pos for pos in safe_moves if not board.grid[pos[0]][pos[1]].is_revealed and not board.grid[pos[0]][pos[1]].is_flagged]

        if not jogadas_seguros:
            break  # Não tem mais jogadas seguras, sai do loop

        for (row, col) in jogadas_seguros:
            cell = board.grid[row][col]
            board.reveal_cell(row, col)
            jogou_algo = True
            if cell.is_mine:
                game_over = True
                return True  # Sai imediatamente, fim do jogo

        # Atualiza o AI para o novo estado do tabuleiro
        ai = MinesweeperAI(board)
        safe_moves, mine_flags = ai.analyze()

        # Atualizar as bandeiras também, caso haja novas minas detectadas
        for (row, col) in mine_flags:
            cell = board.grid[row][col]
            if not cell.is_flagged:
                cell.toggle_flag()
                jogou_algo = True

    return jogou_algo



reset_game()

clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)
    draw_ui()
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 20 <= mx <= 180 and 110 <= my <= 150:
                ai_enabled = not ai_enabled


            if WIDTH - 140 <= mx <= WIDTH - 20 and 30 <= my <= 70:
                reset_game()

            if not game_over and not game_won and my >= 100:
                col = mx // CELL_SIZE
                row = (my - 100) // CELL_SIZE

                if 0 <= row < ROWS and 0 <= col < COLS:
                    cell = board.grid[row][col]

                    if event.button == 1:  # Clique esquerdo
                        board.reveal_cell(row, col)
                        if cell.is_mine:
                            game_over = True
                    elif event.button == 3:  # Clique direito
                        cell.toggle_flag()

                    ai = MinesweeperAI(board)

        if not game_over and not game_won:
            if ai_enabled:
                jogou = ai_play()
                if jogou:
                    ai = MinesweeperAI(board)

            game_won = check_victory()

    pygame.display.flip()
    clock.tick(10)  # controla a velocidade (10 frames por segundo)
