import pygame
import sys
import config

if config.ALGORITHM == "A*":
    from astar import astar as pathfinding
    USE_COST = True
elif config.ALGORITHM == "BFS":
    from bfs import bfs as pathfinding
    USE_COST = False
else:
    raise ValueError("Algoritmo inválido em config.py")

pygame.init()
TILE_SIZE = 40

# Mapa com dois caminhos válidos para E, um mais curto com blocos difíceis (.)
MAP = [
    "####################",
    "#S    #        #   #",
    "# ###.# ###### # # #",
    "#   #.#        # # #",
    "### #.###### # #   #",
    "#   #........#   # #",
    "# #### ######### # #",
    "#  .........   ... #",
    "###### # ### ##### #",
    "#      #   # -----E#",
    "####################"
]

COST_MAP = {
    " ": 1,
    ".": 5,
    "-": 3,
    "S": 1,
    "E": 1
}

ROWS = len(MAP)
COLS = len(MAP[0])
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + 40  # espaço extra para HUD

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirinto com Energia")
font = pygame.font.SysFont(None, 30)

def find_pos(char):
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile == char:
                return x, y
    return None

player_x, player_y = find_pos('S')
end_pos = find_pos('E')
path = []
path_index = 0
auto_move = False
energy = 100

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
            elif tile == '.':
                pygame.draw.rect(screen, (150, 150, 255), rect)  # azul claro para blocos difíceis
            elif tile == '-':
                pygame.draw.rect(screen, (50, 250, 255), rect)  # azul claro para blocos menos difíceis
            else:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

def move_player(dx, dy):
    global player_x, player_y, energy
    new_x = player_x + dx
    new_y = player_y + dy

    if MAP[new_y][new_x] != '#':
        cost = get_cost(new_x, new_y)
        if energy >= cost:
            player_x = new_x
            player_y = new_y
            energy -= cost


def draw_path(path):
    for pos in path:
        if pos != (player_x, player_y) and pos != end_pos:
            pygame.draw.rect(screen, YELLOW, (pos[0]*TILE_SIZE, pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def get_cost(x, y):
    tile = MAP[y][x]
    return COST_MAP.get(tile, 1)

def draw_energy():
    text = font.render(f"ENERGIA: {energy}", True, BLACK)
    screen.blit(text, (10, HEIGHT - 35))

while True:
    clock.tick(10)
    screen.fill(WHITE)

    draw_map()
    if path:
        draw_path(path)

    pygame.draw.rect(screen, BLUE, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    draw_energy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Espaço inicia o caminho automático
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if USE_COST:
                    path = pathfinding(MAP, COST_MAP, (player_x, player_y), end_pos)
                else:
                    path = pathfinding(MAP, (player_x, player_y), end_pos)
                if path:
                    path_index = 1
                    auto_move = True
                    energy = 100  # reseta energia

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

    if auto_move and path_index < len(path):
        next_x, next_y = path[path_index]
        cost = get_cost(next_x, next_y)
        if energy >= cost:
            energy -= cost
            player_x, player_y = next_x, next_y
            path_index += 1
        else:
            auto_move = False  # ficou sem energia
    elif auto_move and path_index >= len(path):
        auto_move = False  # chegou ao fim

    pygame.display.flip()
