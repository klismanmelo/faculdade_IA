import random
import time

def gerar_estado_inicial():
    # Gera uma configuração inicial aleatória
    # Cada coluna tem exatamente uma rainha em uma linha aleatória (0 a 7)
    return [random.randint(0, 7) for _ in range(8)]

def calcular_heuristica(estado):
    # Calcula o número de pares de rainhas que se atacam
    # Ou seja, rainhas na mesma linha ou na mesma diagonal
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            # Verifica se rainhas estão na mesma linha
            # Ou na mesma diagonal (diferença entre linhas == diferença entre colunas)
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def vizinhos(estado):
    # Gera todos os estados vizinhos possíveis
    # Movendo uma rainha para qualquer outra linha na mesma coluna
    vizinhos = []
    for col in range(8):
        for row in range(8):
            if estado[col] != row:  # Evita gerar o estado atual novamente
                novo_estado = estado.copy()  # Copia o estado atual para modificar
                novo_estado[col] = row  # Move a rainha da coluna para a nova linha
                vizinhos.append(novo_estado)  # Adiciona o novo estado à lista
    return vizinhos

def subida_de_encosta_com_reinicio():
    inicio_tempo = time.time()  # Marca o tempo inicial para medir duração
    iteracoes = 0  # Conta o número total de iterações
    reinicios = 0  # Conta quantas vezes o algoritmo precisou reiniciar

    while True:
        estado_atual = gerar_estado_inicial()  # Gera um estado inicial aleatório
        heuristica_atual = calcular_heuristica(estado_atual)  # Calcula conflitos no estado atual

        while True:
            iteracoes += 1
            vizinhos_estado = vizinhos(estado_atual)  # Gera todos os vizinhos possíveis
            melhor_vizinho = estado_atual  # Inicializa melhor vizinho como o estado atual
            melhor_heuristica = heuristica_atual  # Inicializa melhor heurística com a atual

            # Procura entre os vizinhos o estado com menor número de conflitos
            for viz in vizinhos_estado:
                h = calcular_heuristica(viz)
                if h < melhor_heuristica:
                    melhor_vizinho = viz
                    melhor_heuristica = h

            if melhor_heuristica == 0:
                # Solução perfeita encontrada (nenhuma rainha se ataca)
                fim_tempo = time.time()
                print("✅ Solução encontrada!")
                print("Estado final:", melhor_vizinho)
                print("Número de reinícios:", reinicios)
                print("Número total de iterações:", iteracoes)
                print("Qualidade antes da solução final:", heuristica_atual)
                print("Tempo de execução: %.4f segundos" % (fim_tempo - inicio_tempo))
                return melhor_vizinho

            if melhor_heuristica >= heuristica_atual:
                # Ficou preso em um ótimo local (não melhorou)
                # Faz reinício gerando um novo estado inicial aleatório
                reinicios += 1
                break  # Sai do loop interno para reiniciar

            # Atualiza o estado atual para o melhor vizinho encontrado
            estado_atual = melhor_vizinho
            heuristica_atual = melhor_heuristica

if __name__ == "__main__":
    subida_de_encosta_com_reinicio()  # Executa o algoritmo quando rodar o arquivo
