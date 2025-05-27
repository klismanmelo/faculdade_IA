import pygame
from game import Game  # Importa a classe Game que contém a lógica do jogo
import os

pygame.init()  # Inicializa o módulo pygame
WIN = pygame.display.set_mode((640, 640))  # Cria a janela do jogo com 640x640 pixels
pygame.display.set_caption("Problema das 8 Rainhas")  # Define o título da janela

# Carrega a imagem da rainha a partir do diretório relativo "./8-queens/"
queen_img = pygame.image.load(os.path.join("./8-queens/queen.png"))

def main():
    clock = pygame.time.Clock()  # Cria um relógio para controlar o FPS do jogo
    game = Game(WIN, queen_img)  # Instancia o objeto Game, passando a janela e a imagem da rainha

    running = True  # Flag para controlar o loop principal do jogo
    while running:
        clock.tick(60)  # Limita o jogo a 60 frames por segundo
        game.draw_board()  # Desenha o tabuleiro e o estado atual do jogo
        pygame.display.update()  # Atualiza a tela para mostrar o que foi desenhado

        # Loop para capturar eventos do pygame (teclado, mouse, fechar janela)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Se o jogador fechar a janela
                running = False  # Encerra o loop principal

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Se o mouse foi clicado
                pos = pygame.mouse.get_pos()  # Pega a posição do clique
                game.place_queen(pos)  # Tenta colocar uma rainha na posição clicada

            elif event.type == pygame.KEYDOWN:  # Se uma tecla foi pressionada
                if event.key == pygame.K_t:  # Tecla 'T' para testar conflitos entre rainhas
                    conflitos = game.testar_colisoes()  # Verifica quantas rainhas estão se atacando
                    print(f"⚔️ Rainhas se atacando: {conflitos}")  # Imprime o resultado no console

                elif event.key == pygame.K_r:  # Tecla 'R' para resolver o problema automaticamente
                    game.resolver_com_algoritmo()  # Executa o algoritmo para resolver o problema

    pygame.quit()  # Encerra o pygame e fecha a janela

if __name__ == "__main__":
    main()  # Executa a função principal quando o script é rodado diretamente
