# tempera.py

import random
import math
import time

def calcular_conflitos(estado):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if estado[i] == estado[j] or abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def gerar_vizinho(estado):
    novo_estado = estado[:]
    col = random.randint(0, 7)
    novo_estado[col] = random.randint(0, 7)
    return novo_estado

def tempera_simulada(temperatura_inicial=1000, resfriamento=0.95, temperatura_min=1e-3):
    """
    Algoritmo de Têmpera Simulada para resolver o problema das 8 rainhas.
    """
    inicio = time.time()
    estado_atual = [random.randint(0, 7) for _ in range(8)]
    conflitos_atual = calcular_conflitos(estado_atual)

    temperatura = temperatura_inicial
    iteracoes = 0

    melhor_estado = estado_atual[:]
    menor_conflito = conflitos_atual

    while temperatura > temperatura_min and conflitos_atual > 0:
        iteracoes += 1
        novo_estado = gerar_vizinho(estado_atual)
        conflitos_novo = calcular_conflitos(novo_estado)

        delta = conflitos_novo - conflitos_atual

        # Aceita a nova solução se for melhor ou com probabilidade baseada na temperatura
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            estado_atual = novo_estado
            conflitos_atual = conflitos_novo

            if conflitos_novo < menor_conflito:
                melhor_estado = novo_estado
                menor_conflito = conflitos_novo

        temperatura *= resfriamento

    fim = time.time()

    print("🔥 Algoritmo: Têmpera Simulada")
    print("⏱️ Tempo de execução:", round(fim - inicio, 4), "segundos")
    print("🔁 Iterações:", iteracoes)
    print("📉 Menor número de conflitos encontrados:", menor_conflito)
    print("✅ Solução final:", melhor_estado)
    return melhor_estado
