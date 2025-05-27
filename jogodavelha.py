import pygame
import sys

# Classe principal do jogo da velha com IA
class JogoDaVelhaIA:
    def __init__(self, ia_comeca=True):
        # Inicializa o pygame
        pygame.init()
        self.tamanho = 600  # Tamanho da janela (600x600 pixels)
        self.tela = pygame.display.set_mode((self.tamanho, self.tamanho))  # Cria a janela do jogo
        pygame.display.set_caption("Jogo da Velha - IA (X) vs Humano (O)")  # Título da janela

        # Define fontes para os textos (X/O e mensagens)
        self.fonte = pygame.font.SysFont(None, 100)
        self.fonte_mensagem = pygame.font.SysFont(None, 60)

        # Define os símbolos dos jogadores
        self.jogador_humano = "O"
        self.jogador_ia = "X"

        # Tamanho de cada célula (divisão por 3 do tamanho total)
        self.celula_tamanho = self.tamanho // 3

        # Lista para exibir informações de debug do algoritmo
        self.debug_info = []

        # Define quem começa jogando
        self.turno_inicial_ia = ia_comeca

        # Estado do jogo (ativo ou finalizado)
        self.jogo_ativo = True

        # Inicializa o tabuleiro (3x3 vazio)
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]

        # Se a IA começar, faz a primeira jogada
        if self.turno_inicial_ia:
            self.jogada_ia()

        # Inicia o loop principal do jogo
        self.loop_principal()

    def loop_principal(self):
        # Loop principal do jogo
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Encerra o jogo ao fechar a janela
                    pygame.quit()
                    sys.exit()

                # Trata cliques do mouse (jogada do humano)
                if evento.type == pygame.MOUSEBUTTONDOWN and self.jogo_ativo:
                    x, y = evento.pos  # Posição do clique
                    linha = y // self.celula_tamanho
                    coluna = x // self.celula_tamanho

                    # Se a célula clicada estiver vazia, faz a jogada do humano
                    if self.tabuleiro[linha][coluna] == "":
                        self.tabuleiro[linha][coluna] = self.jogador_humano
                        if self.verificar_fim(self.jogador_humano):
                            continue  # Se o jogo terminou, não continua
                        self.jogada_ia()  # Chama jogada da IA

            # Atualiza a tela
            self.desenhar_tabuleiro()
            pygame.display.flip()

    def desenhar_tabuleiro(self):
        # Preenche o fundo com branco
        self.tela.fill((255, 255, 255))

        # Desenha as linhas do tabuleiro
        for i in range(1, 3):
            # Linhas horizontais
            pygame.draw.line(self.tela, (0, 0, 0), (0, i * self.celula_tamanho), (self.tamanho, i * self.celula_tamanho), 5)
            # Linhas verticais
            pygame.draw.line(self.tela, (0, 0, 0), (i * self.celula_tamanho, 0), (i * self.celula_tamanho, self.tamanho), 5)

        # Desenha os símbolos "X" e "O" no tabuleiro
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] != "":
                    texto = self.fonte.render(self.tabuleiro[i][j], True, (0, 0, 0))
                    rect = texto.get_rect(center=(j * self.celula_tamanho + self.celula_tamanho // 2,
                                                  i * self.celula_tamanho + self.celula_tamanho // 2))
                    self.tela.blit(texto, rect)

    def exibir_mensagem_final(self, mensagem):
        # Mostra mensagem final (vitória ou empate)
        texto = self.fonte_mensagem.render(mensagem, True, (0, 128, 0))
        rect = texto.get_rect(center=(self.tamanho // 2, self.tamanho // 2))
        self.tela.blit(texto, rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Espera 2 segundos

    def jogada_ia(self):
        melhor_pontuacao = float('-inf')  # Melhor pontuação inicial
        melhor_jogada = None  # Melhor jogada a ser encontrada
        self.debug_info.clear()

        # Itera sobre todas as posições possíveis
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == "":
                    self.tabuleiro[i][j] = self.jogador_ia  # Simula jogada da IA
                    pontuacao = self.minimax(self.tabuleiro, 0, False, float('-inf'), float('inf'), f"{i},{j}")
                    self.tabuleiro[i][j] = ""  # Desfaz jogada simulada
                    self.debug_info.append((f"Raiz {i},{j}", pontuacao))

                    if pontuacao > melhor_pontuacao:
                        melhor_pontuacao = pontuacao
                        melhor_jogada = (i, j)

        self.exibir_debug()  # Mostra árvore de decisão no terminal

        if melhor_jogada:
            i, j = melhor_jogada
            self.tabuleiro[i][j] = self.jogador_ia  # Faz a melhor jogada encontrada
            self.verificar_fim(self.jogador_ia)

    def minimax(self, tab, profundidade, maximizando, alfa, beta, caminho):
        # Verifica se há vitória ou empate no estado atual
        if self.verificar_vitoria_simulada(tab, self.jogador_ia):
            return 10 - profundidade
        elif self.verificar_vitoria_simulada(tab, self.jogador_humano):
            return profundidade - 10
        elif self.verificar_empate_simulado(tab):
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
                            break  # Poda alfa-beta
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
                            break  # Poda alfa-beta
            return pior

    def verificar_fim(self, jogador):
        # Verifica se houve vitória ou empate e mostra mensagem
        if self.verificar_vitoria_simulada(self.tabuleiro, jogador):
            vencedor = "IA venceu!" if jogador == self.jogador_ia else "Você venceu!"
            print(f"\n{vencedor}")
            self.jogo_ativo = False
            self.exibir_mensagem_final(vencedor)
            self.reiniciar_jogo()
            return True
        elif self.verificar_empate_simulado(self.tabuleiro):
            print("\nEmpate!")
            self.jogo_ativo = False
            self.exibir_mensagem_final("Empate!")
            self.reiniciar_jogo()
            return True
        return False

    def verificar_vitoria_simulada(self, tab, jogador):
        # Verifica linhas, colunas e diagonais para ver se o jogador venceu
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
        # Verifica se todas as células estão preenchidas (empate)
        return all(tab[i][j] != "" for i in range(3) for j in range(3))

    def reiniciar_jogo(self):
        # Reinicia o tabuleiro e alterna o jogador inicial
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]
        self.debug_info.clear()
        self.jogo_ativo = True
        self.turno_inicial_ia = not self.turno_inicial_ia
        if self.turno_inicial_ia:
            self.jogada_ia()

    def exibir_debug(self):
        # Mostra no terminal a árvore de decisão do minimax
        print("\nÁrvore de decisão da IA (Minimax com Alfa-Beta):")
        for caminho, score in self.debug_info:
            print(f"{caminho}: {score}")

# Executa o jogo
if __name__ == "__main__":
    JogoDaVelhaIA(ia_comeca=True)
