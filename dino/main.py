import pygame
import random
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 400
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do Dinossauro")
RELOGIO = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.SysFont(None, 36)

# Dino
dino = pygame.Rect(100, 300, 60, 60)  # Aumentado
dino_vel_y = 0
pulo = False
abaixado = False

# Obstáculos
obstaculos = []
tempo_obstaculo = 0

# Velocidade
velocidade = 10
velocidade_max = 50

# Distância percorrida
distancia = 0

def desenhar_tela():
    TELA.fill(BRANCO)
    pygame.draw.rect(TELA, PRETO, dino)
    for obs in obstaculos:
        pygame.draw.rect(TELA, PRETO, obs)
    texto_distancia = fonte.render(f"Distância: {distancia} px", True, PRETO)
    texto_velocidade = fonte.render(f"Velocidade: {velocidade} px", True, PRETO)
    TELA.blit(texto_distancia, (10, 10))
    TELA.blit(texto_velocidade, (10, 40))
    pygame.display.flip()

def fim_jogo():
    TELA.fill(BRANCO)
    texto = fonte.render(f"Game Over! Distância total: {distancia} px", True, PRETO)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not pulo:
                dino_vel_y = -15
                pulo = True
            if evento.key == pygame.K_DOWN and not pulo:
                abaixado = True
                dino.height = 35  # proporcional ao novo tamanho
                dino.y = 325
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_DOWN:
                abaixado = False
                dino.height = 60
                dino.y = 300

    # Física do pulo
    dino_vel_y += 1
    dino.y += dino_vel_y
    if dino.y >= (325 if abaixado else 300):
        dino.y = 325 if abaixado else 300
        pulo = False

    # Obstáculos
    tempo_obstaculo += 1
    if tempo_obstaculo > 60:
        tempo_obstaculo = 0
        tipo = random.choice(["chao", "aereo"])
        if tipo == "chao":
            altura = random.randint(40, 60)
            obstaculo = pygame.Rect(LARGURA, 360 - altura, 20, altura)
        else:  # aéreo (pássaro)
            altura = random.randint(10, 15)
            y_pos = random.choice([200, 220])
            obstaculo = pygame.Rect(LARGURA, y_pos, 30, altura)
        obstaculos.append(obstaculo)

    for obs in list(obstaculos):
        obs.x -= velocidade
        if obs.right < 0:
            obstaculos.remove(obs)
        if dino.colliderect(obs):
            fim_jogo()

    # Aumentar dificuldade
    distancia += velocidade
    if distancia % 200 == 0 and velocidade < velocidade_max:
        velocidade += 2

    desenhar_tela()
    RELOGIO.tick(30)
