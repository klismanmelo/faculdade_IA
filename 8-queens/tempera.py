import random
import math
import time

def calcular_conflitos(estado):
    # Calcula o número total de pares de rainhas que estão se atacando
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            # Verifica se estão na mesma linha ou na mesma diagonal
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def gerar_vizinho(estado):
    # Gera um estado vizinho modificando a posição de uma rainha em uma coluna aleatória
    novo_estado = estado[:]  # Copia o estado atual
    col = random.randint(0, 7)  # Escolhe uma coluna aleatória
    novo_estado[col] = random.randint(0, 7)  # Move a rainha dessa coluna para uma linha aleatória
    return novo_estado

def tempera_simulada(temperatura_inicial=1000, resfriamento=0.95, temperatura_min=1e-3):
    """
    Algoritmo de Têmpera Simulada para resolver o problema das 8 rainhas.
    """
    inicio = time.time()  # Marca o tempo inicial para medir a duração

    # Gera um estado inicial aleatório
    estado_atual = [random.randint(0, 7) for _ in range(8)]
    conflitos_atual = calcular_conflitos(estado_atual)

    temperatura = temperatura_inicial  # Define a temperatura inicial
    iteracoes = 0  # Contador de iterações

    melhor_estado = estado_atual[:]  # Inicializa o melhor estado encontrado
    menor_conflito = conflitos_atual  # Inicializa o menor número de conflitos encontrados

    # Executa enquanto a temperatura não estiver muito baixa e ainda houver conflitos
    while temperatura > temperatura_min and conflitos_atual > 0:
        iteracoes += 1

        # Gera um estado vizinho ao estado atual
        novo_estado = gerar_vizinho(estado_atual)
        conflitos_novo = calcular_conflitos(novo_estado)

        delta = conflitos_novo - conflitos_atual  # Diferença entre conflitos do novo e do atual

        # Aceita a nova solução se for melhor (menos conflitos)
        # Ou aceita com certa probabilidade mesmo que seja pior (controle pela temperatura)
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            estado_atual = novo_estado
            conflitos_atual = conflitos_novo

            # Atualiza o melhor estado encontrado, se o novo for melhor
            if conflitos_novo < menor_conflito:
                melhor_estado = novo_estado
                menor_conflito = conflitos_novo

        temperatura *= resfriamento  # Resfria a temperatura multiplicando pelo fator de resfriamento

    fim = time.time()  # Marca o tempo final

    # Exibe informações sobre o resultado
    print("🔥 Algoritmo: Têmpera Simulada")
    print("⏱️ Tempo de execução:", round(fim - inicio, 4), "segundos")
    print("🔁 Iterações:", iteracoes)
    print("📉 Menor número de conflitos encontrados:", menor_conflito)
    print("✅ Solução final:", melhor_estado)

    return melhor_estado
