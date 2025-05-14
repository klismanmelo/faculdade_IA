import pygame
import random
import sys

# Cores
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH = SIZE * (TILE_SIZE + MARGIN) + MARGIN
HEIGHT = WIDTH
FONT_NAME = 'freesansbold.ttf'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
font = pygame.font.Font(FONT_NAME, 40)


def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            rect = pygame.Rect(
                col * (TILE_SIZE + MARGIN) + MARGIN,
                row * (TILE_SIZE + MARGIN) + MARGIN,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(screen, TILE_COLORS.get(value, EMPTY_COLOR), rect)
            if value != 0:
                text = font.render(str(value), True, (119, 110, 101))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    pygame.display.flip()


def add_random_tile(board):
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2 if random.random() < 0.9 else 4


def init_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_random_tile(board)
    add_random_tile(board)
    return board


def compress(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (SIZE - len(new_row))
    return new_row


def merge(row):
    for i in range(SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row


def move_left(board):
    moved = False
    new_board = []
    for row in board:
        compressed = compress(row)
        merged = merge(compressed)
        final = compress(merged)
        if final != row:
            moved = True
        new_board.append(final)
    return new_board, moved


def move_right(board):
    reversed_board = [list(reversed(row)) for row in board]
    new_board, moved = move_left(reversed_board)
    final_board = [list(reversed(row)) for row in new_board]
    return final_board, moved


def transpose(board):
    return [list(row) for row in zip(*board)]


def move_up(board):
    transposed = transpose(board)
    new_board, moved = move_left(transposed)
    return transpose(new_board), moved


def move_down(board):
    transposed = transpose(board)
    new_board, moved = move_right(transposed)
    return transpose(new_board), moved


def has_moves(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return True
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return True
    return False


def has_2048(board):
    return any(2048 in row for row in board)


def main():
    board = init_board()
    draw_board(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    board, moved = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    board, moved = move_right(board)
                elif event.key == pygame.K_UP:
                    board, moved = move_up(board)
                elif event.key == pygame.K_DOWN:
                    board, moved = move_down(board)

                if moved:
                    add_random_tile(board)
                    draw_board(board)

                if has_2048(board):
                    print("Você venceu! 2048 alcançado!")
                    pygame.quit()
                    sys.exit()

                if not has_moves(board):
                    print("Fim de jogo!")
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
    # --- Exportações para IA ---
    __all__ = [
        'move_left', 'move_right', 'move_up', 'move_down',
        'add_random_tile', 'init_board', 'draw_board', 'has_moves', 'has_2048'
    ]

