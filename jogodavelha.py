import pygame
import sys
import copy

class JogoDaVelhaIA:
    def __init__(self, ia_comeca=True):
        pygame.init()
        self.tamanho = 600
        self.tela = pygame.display.set_mode((self.tamanho, self.tamanho))
        pygame.display.set_caption("Jogo da Velha - IA (X) vs Humano (O)")

        self.fonte = pygame.font.SysFont(None, 100)
        self.jogador_humano = "O"
        self.jogador_ia = "X"
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]
        self.celula_tamanho = self.tamanho // 3

        self.debug_info = []

        self.jogo_ativo = True
        if ia_comeca:
            self.jogada_ia()

        self.loop_principal()

    def loop_principal(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN and self.jogo_ativo:
                    x, y = evento.pos
                    linha = y // self.celula_tamanho
                    coluna = x // self.celula_tamanho
                    if self.tabuleiro[linha][coluna] == "":
                        self.tabuleiro[linha][coluna] = self.jogador_humano
                        if self.verificar_fim(self.jogador_humano):
                            continue
                        self.jogada_ia()

            self.desenhar_tabuleiro()
            pygame.display.flip()

    def desenhar_tabuleiro(self):
        self.tela.fill((255, 255, 255))
        # Linhas
        for i in range(1, 3):
            pygame.draw.line(self.tela, (0, 0, 0), (0, i * self.celula_tamanho), (self.tamanho, i * self.celula_tamanho), 5)
            pygame.draw.line(self.tela, (0, 0, 0), (i * self.celula_tamanho, 0), (i * self.celula_tamanho, self.tamanho), 5)

        # X e O
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] != "":
                    texto = self.fonte.render(self.tabuleiro[i][j], True, (0, 0, 0))
                    rect = texto.get_rect(center=(j * self.celula_tamanho + self.celula_tamanho // 2,
                                                  i * self.celula_tamanho + self.celula_tamanho // 2))
                    self.tela.blit(texto, rect)

    def jogada_ia(self):
        melhor_pontuacao = float('-inf')
        melhor_jogada = None
        self.debug_info.clear()

        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == "":
                    self.tabuleiro[i][j] = self.jogador_ia
                    pontuacao = self.minimax(self.tabuleiro, 0, False, float('-inf'), float('inf'), f"{i},{j}")
                    self.tabuleiro[i][j] = ""
                    self.debug_info.append((f"Raiz {i},{j}", pontuacao))

                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = (i, j)

        self.exibir_debug()

        if melhor_jogada:
            i, j = melhor_jogada
            self.tabuleiro[i][j] = self.jogador_ia
            self.verificar_fim(self.jogador_ia)

    def minimax(self, tab, profundidade, maximizando, alfa, beta, caminho):
        if self.verificar_vitoria_simulada(tab, self.jogador_ia):
            self.debug_info.append((f"{caminho} (vitória IA)", 10 - profundidade))
            return 10 - profundidade
        elif self.verificar_vitoria_simulada(tab, self.jogador_humano):
            self.debug_info.append((f"{caminho} (vitória jogador)", profundidade - 10))
            return profundidade - 10
        elif self.verificar_empate_simulado(tab):
            self.debug_info.append((f"{caminho} (empate)", 0))
            return 0

        if maximizando:
            melhor = float('-inf')
            for i in range(3):
                for j in range(3):
                    if tab[i][j] == "":
                        tab[i][j] = self.jogador_ia
                        valor = self.minimax(tab, profundidade + 1, False, alfa, beta, caminho + f" -> {i},{j}")
                        tab[i][j] = ""
                        melhor = max(melhor, valor)
                        alfa = max(alfa, valor)
                        if beta <= alfa:
                            break
            return melhor
        else:
            pior = float('inf')
            for i in range(3):
                for j in range(3):
                    if tab[i][j] == "":
                        tab[i][j] = self.jogador_humano
                        valor = self.minimax(tab, profundidade + 1, True, alfa, beta, caminho + f" -> {i},{j}")
                        tab[i][j] = ""
                        pior = min(pior, valor)
                        beta = min(beta, valor)
                        if beta <= alfa:
                            break
            return pior

    def verificar_fim(self, jogador):
        if self.verificar_vitoria_simulada(self.tabuleiro, jogador):
            print(f"\n{'IA' if jogador == self.jogador_ia else 'Você'} venceu!")
            self.jogo_ativo = False
            pygame.time.delay(1500)
            self.reiniciar_jogo()
            return True
        elif self.verificar_empate_simulado(self.tabuleiro):
            print("\nEmpate!")
            self.jogo_ativo = False
            pygame.time.delay(1500)
            self.reiniciar_jogo()
            return True
        return False

    def verificar_vitoria_simulada(self, tab, jogador):
        for i in range(3):
            if all(tab[i][j] == jogador for j in range(3)):
                return True
            if all(tab[j][i] == jogador for j in range(3)):
                return True
        if all(tab[i][i] == jogador for i in range(3)):
            return True
        if all(tab[i][2 - i] == jogador for i in range(3)):
            return True
        return False

    def verificar_empate_simulado(self, tab):
        return all(tab[i][j] != "" for i in range(3) for j in range(3))

    def reiniciar_jogo(self):
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]
        self.debug_info.clear()
        self.jogo_ativo = True
        self.jogada_ia()

    def exibir_debug(self):
        print("\nÁrvore de decisão da IA (Minimax com Alfa-Beta):")
        for caminho, score in self.debug_info:
            print(f"{caminho}: {score}")

if __name__ == "__main__":
    JogoDaVelhaIA(ia_comeca=True)
