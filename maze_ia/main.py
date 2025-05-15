import pygame
import sys
import config

if config.ALGORITHM == "A*":
    from astar import astar as pathfinding
elif config.ALGORITHM == "BFS":
    from bfs import bfs as pathfinding
else:
    raise ValueError("Algoritmo inválido em config.py")

# Inicialização
pygame.init()
TILE_SIZE = 40

MAP = [
    "####################",
    "#S   #         #   #",
    "# ### # ###### # # #",
    "#   # #      # # # #",
    "### # ###### # ### #",
    "#   #        #     #",
    "# #### ########### #",
    "#      #     #     #",
    "###### # ### # #####",
    "#      #   #       E",
    "####################"
]

ROWS = len(MAP)
COLS = len(MAP[0])
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Labirinto")

def find_pos(char):
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == char:
                return x, y
    return None

player_x, player_y = find_pos('S')
end_pos = find_pos('E')
path = []

clock = pygame.time.Clock()

def draw_map():
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == '#':
                pygame.draw.rect(screen, BLACK, rect)
            elif tile == 'S':
                pygame.draw.rect(screen, GREEN, rect)
            elif tile == 'E':
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

def move_player(dx, dy):
    global player_x, player_y
    new_x = player_x + dx
    new_y = player_y + dy

    if MAP[new_y][new_x] != '#':
        player_x = new_x
        player_y = new_y

def draw_path(path):
    for pos in path:
        if pos != (player_x, player_y) and pos != end_pos:
            pygame.draw.rect(screen, YELLOW, (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
path_index = 0
auto_move = False

while True:
    clock.tick(10)  # controle de FPS (10 é bom para movimento visível)
    screen.fill(WHITE)

    draw_map()

    if path:
        draw_path(path)

    pygame.draw.rect(screen, BLUE, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pressionar espaço gera o caminho e inicia o movimento automático
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = pathfinding(MAP, (player_x, player_y), end_pos)
                if path:
                    path_index = 1  # começa do 1 (0 é onde o player já está)
                    auto_move = True

    keys = pygame.key.get_pressed()
    if not auto_move:
        if keys[pygame.K_UP]:
            move_player(0, -1)
        elif keys[pygame.K_DOWN]:
            move_player(0, 1)
        elif keys[pygame.K_LEFT]:
            move_player(-1, 0)
        elif keys[pygame.K_RIGHT]:
            move_player(1, 0)

    # Movimentação automática seguindo o caminho
    if auto_move and path_index < len(path):
        next_x, next_y = path[path_index]
        player_x, player_y = next_x, next_y
        path_index += 1
    elif auto_move and path_index >= len(path):
        auto_move = False  # terminou o caminho

    pygame.display.flip()

while True:
    clock.tick(60)
    screen.fill(WHITE)

    draw_map()

    if path:
        draw_path(path)

    pygame.draw.rect(screen, BLUE, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gera o caminho ao pressionar espaço
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = pathfinding(MAP, (player_x, player_y), end_pos)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move_player(0, -1)
    elif keys[pygame.K_DOWN]:
        move_player(0, 1)
    elif keys[pygame.K_LEFT]:
        move_player(-1, 0)
    elif keys[pygame.K_RIGHT]:
        move_player(1, 0)

    pygame.display.flip()
