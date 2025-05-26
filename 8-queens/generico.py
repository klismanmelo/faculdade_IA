# generico.py

import random
import time

TAMANHO_POPULACAO = 100
TAXA_MUTACAO = 0.1
MAX_GERACOES = 10000

def gerar_individuo():
    # Um indivíduo é uma permutação de 0 a 7 (linha de cada rainha)
    return [random.randint(0, 7) for _ in range(8)]

def calcular_conflitos(individuo):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def fitness(individuo):
    # Quanto menos conflitos, maior o fitness (28 é o máximo possível de pares de rainhas sem conflito)
    return 28 - calcular_conflitos(individuo)

def selecao(populacao):
    # Seleção por torneio: escolhe os melhores entre 5 aleatórios
    torneio = random.sample(populacao, 5)
    torneio.sort(key=lambda x: fitness(x), reverse=True)
    return torneio[0]

def crossover(pai1, pai2):
    # Crossover de ponto único
    ponto = random.randint(1, 6)
    filho = pai1[:ponto] + pai2[ponto:]
    return filho

def mutacao(individuo):
    # Mutação: altera a linha de uma das rainhas com chance definida
    if random.random() < TAXA_MUTACAO:
        col = random.randint(0, 7)
        linha = random.randint(0, 7)
        individuo[col] = linha
    return individuo

def algoritmo_genetico():
    """
    Algoritmo Genético para resolver o problema das 8 rainhas.
    """
    inicio = time.time()

    populacao = [gerar_individuo() for _ in range(TAMANHO_POPULACAO)]
    melhor_solucao = None
    melhor_fitness = 0
    geracao = 0

    while geracao < MAX_GERACOES:
        populacao.sort(key=lambda x: fitness(x), reverse=True)

        if fitness(populacao[0]) == 28:
            melhor_solucao = populacao[0]
            melhor_fitness = 28
            break

        nova_populacao = []

        # Gera nova população com seleção, crossover e mutação
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = selecao(populacao)
            pai2 = selecao(populacao)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao
        geracao += 1

        # Atualiza melhor solução
        if fitness(populacao[0]) > melhor_fitness:
            melhor_solucao = populacao[0]
            melhor_fitness = fitness(populacao[0])

    fim = time.time()

    print("🧬 Algoritmo: Genético")
    print("⏱️ Tempo de execução:", round(fim - inicio, 4), "segundos")
    print("🔁 Gerações:", geracao)
    print("📉 Conflitos na melhor solução:", calcular_conflitos(melhor_solucao))
    print("✅ Solução final:", melhor_solucao)
    return melhor_solucao
