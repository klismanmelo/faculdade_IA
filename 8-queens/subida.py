import random
import time

def gerar_estado_inicial():
    # Gera um vetor de 8 colunas com linhas aleatórias (1 rainha por coluna)
    return [random.randint(0, 7) for _ in range(8)]

def calcular_heuristica(estado):
    # Conta quantas rainhas estão se atacando (pares de conflito)
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            # Mesma linha ou mesma diagonal
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def vizinhos(estado):
    # Gera todos os vizinhos possíveis movendo 1 rainha para outra linha
    vizinhos = []
    for col in range(8):
        for row in range(8):
            if estado[col] != row:
                novo_estado = estado.copy()
                novo_estado[col] = row
                vizinhos.append(novo_estado)
    return vizinhos

def subida_de_encosta_com_reinicio():
    inicio_tempo = time.time()
    iteracoes = 0
    reinicios = 0

    while True:
        estado_atual = gerar_estado_inicial()
        heuristica_atual = calcular_heuristica(estado_atual)

        while True:
            iteracoes += 1
            vizinhos_estado = vizinhos(estado_atual)
            melhor_vizinho = estado_atual
            melhor_heuristica = heuristica_atual

            # Busca o vizinho com menor heurística
            for viz in vizinhos_estado:
                h = calcular_heuristica(viz)
                if h < melhor_heuristica:
                    melhor_vizinho = viz
                    melhor_heuristica = h

            if melhor_heuristica == 0:
                fim_tempo = time.time()
                print("✅ Solução encontrada!")
                print("Estado final:", melhor_vizinho)
                print("Número de reinícios:", reinicios)
                print("Número total de iterações:", iteracoes)
                print("Qualidade antes da solução final:", heuristica_atual)
                print("Tempo de execução: %.4f segundos" % (fim_tempo - inicio_tempo))
                return melhor_vizinho

            if melhor_heuristica >= heuristica_atual:
                # Ficou preso em ótimo local, faz reinício
                reinicios += 1
                break  # sai do loop interno e reinicia com novo estado

            estado_atual = melhor_vizinho
            heuristica_atual = melhor_heuristica

if __name__ == "__main__":
    subida_de_encosta_com_reinicio()
