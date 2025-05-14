import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, END

class JogoDaVelhaIA:
    def __init__(self, root, ia_comeca=True):
        self.root = root
        self.root.title("Jogo da Velha - IA (X) vs Humano (O)")

        self.jogador_humano = "O"
        self.jogador_ia = "X"
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]
        self.botoes = [[None for _ in range(3)] for _ in range(3)]

        self.debug_info = []  # Aqui guardaremos os dados da árvore

        self.criar_interface()
        self.criar_janela_debug()

        if ia_comeca:
            self.jogada_ia()

    def criar_interface(self):
        for linha in range(3):
            for coluna in range(3):
                botao = tk.Button(self.root, text="", font=("Arial", 32), width=5, height=2,
                                  command=lambda l=linha, c=coluna: self.clique(l, c))
                botao.grid(row=linha, column=coluna)
                self.botoes[linha][coluna] = botao

    def criar_janela_debug(self):
        self.debug_window = Toplevel(self.root)
        self.debug_window.title("Árvore de Decisão da IA")
        self.debug_text = Text(self.debug_window, wrap="word", width=50, height=30)
        scrollbar = Scrollbar(self.debug_window, command=self.debug_text.yview)
        self.debug_text.configure(yscrollcommand=scrollbar.set)
        self.debug_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def clique(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == "":
            self.tabuleiro[linha][coluna] = self.jogador_humano
            self.botoes[linha][coluna].config(text=self.jogador_humano, state="disabled")

            if self.verificar_fim(self.jogador_humano):
                return

            self.jogada_ia()

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
            self.botoes[i][j].config(text=self.jogador_ia, state="disabled")
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
            messagebox.showinfo("Fim de jogo", f"{'IA' if jogador == self.jogador_ia else 'Você'} venceu!")
            self.reiniciar_jogo()
            return True
        elif self.verificar_empate_simulado(self.tabuleiro):
            messagebox.showinfo("Fim de jogo", "Empate!")
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
        for i in range(3):
            for j in range(3):
                self.botoes[i][j].config(text="", state="normal")
        self.debug_text.delete(1.0, END)
        self.jogada_ia()

    def exibir_debug(self):
        self.debug_text.delete(1.0, END)
        self.debug_text.insert(END, "Árvore de decisão da IA (Minimax com Alfa-Beta):\n\n")
        for caminho, score in self.debug_info:
            self.debug_text.insert(END, f"{caminho}: {score}\n")


if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelhaIA(root, ia_comeca=True)
    root.mainloop()
