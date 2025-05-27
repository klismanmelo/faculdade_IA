import random
import time

# Configurações do algoritmo genético
TAMANHO_POPULACAO = 100    # Quantidade de indivíduos na população
TAXA_MUTACAO = 0.1         # Probabilidade de mutação de um indivíduo
MAX_GERACOES = 10000       # Número máximo de gerações a serem executadas

def gerar_individuo():
    # Gera um indivíduo, que é uma lista com a posição (linha) de cada rainha em cada coluna (0 a 7)
    # Aqui, cada posição da lista indica a linha da rainha naquela coluna
    return [random.randint(0, 7) for _ in range(8)]

def calcular_conflitos(individuo):
    # Calcula quantos pares de rainhas estão em conflito (mesma linha ou diagonal)
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def fitness(individuo):
    # Calcula o valor de fitness do indivíduo:
    # Quanto menos conflitos, maior o fitness.
    # O máximo de pares sem conflito entre 8 rainhas é 28 (combinatório de 8 sobre 2)
    return 28 - calcular_conflitos(individuo)

def selecao(populacao):
    # Seleção por torneio:
    # Seleciona aleatoriamente 5 indivíduos e retorna o que tem maior fitness entre eles
    torneio = random.sample(populacao, 5)
    torneio.sort(key=lambda x: fitness(x), reverse=True)
    return torneio[0]

def crossover(pai1, pai2):
    # Crossover de ponto único:
    # Cria um filho combinando o início do pai1 e o fim do pai2
    ponto = random.randint(1, 6)  # Ponto de corte entre 1 e 6 para manter diversidade
    filho = pai1[:ponto] + pai2[ponto:]
    return filho

def mutacao(individuo):
    # Mutação:
    # Com uma chance definida, muda a posição (linha) de uma rainha em uma coluna aleatória
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

    # Gera a população inicial aleatória
    populacao = [gerar_individuo() for _ in range(TAMANHO_POPULACAO)]
    melhor_solucao = None
    melhor_fitness = 0
    geracao = 0

    while geracao < MAX_GERACOES:
        # Ordena a população do melhor para o pior com base no fitness
        populacao.sort(key=lambda x: fitness(x), reverse=True)

        # Verifica se encontrou uma solução perfeita (fitness = 28, sem conflitos)
        if fitness(populacao[0]) == 28:
            melhor_solucao = populacao[0]
            melhor_fitness = 28
            break

        nova_populacao = []

        # Cria nova população usando seleção, crossover e mutação
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = selecao(populacao)
            pai2 = selecao(populacao)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao
        geracao += 1

        # Atualiza o melhor indivíduo encontrado até o momento
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
