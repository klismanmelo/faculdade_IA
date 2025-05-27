# comparacao_algoritmos_otimizacao.py
"""
Este arquivo descreve e compara três algoritmos de busca e otimização:
- Subida de Encosta com Reinício Aleatório (Hill Climbing with Random Restart)
- Têmpera Simulada (Simulated Annealing)
- Algoritmo Genético (Genetic Algorithm)

Cada técnica possui suas próprias vantagens, desvantagens e aplicações ideais.
"""

# 1. Subida de Encosta com Reinício Aleatório
"""
Inspirado no conceito de "escalar" até encontrar o ponto mais alto (melhor solução).
Se ficar preso em um ótimo local (não global), reinicia com uma nova solução aleatória.

Características:
- Usa apenas um vizinho por vez
- Reinicia quando não encontra melhorias
- Rápido e simples de implementar

Vantagens:
- Baixo custo computacional
- Fácil de implementar
- Útil para problemas simples

Desvantagens:
- Fica preso facilmente em ótimos locais
- Pouca exploração do espaço de busca
"""

# 2. Têmpera Simulada (Simulated Annealing)
"""
Inspirado no resfriamento de metais (têmpera).
Aceita piores soluções com certa probabilidade, que diminui com o tempo.
Isso ajuda a escapar de ótimos locais e encontrar melhores soluções globais.

Características:
- Aceita soluções piores no início (exploração)
- Temperatura diminui gradualmente (resfriamento)
- Requer função de vizinhança e controle da temperatura

Vantagens:
- Mais flexível que a subida de encosta
- Evita ficar preso em ótimos locais
- Boa para problemas complexos com muitos picos locais

Desvantagens:
- Sensível à escolha dos parâmetros (temperatura inicial, taxa de resfriamento)
- Resultados podem variar bastante
- Mais lento que algoritmos simples
"""

# 3. Algoritmo Genético (Genetic Algorithm)
"""
Inspirado na evolução natural: seleção, cruzamento e mutação de uma população de indivíduos.
Cada indivíduo representa uma solução possível.

Características:
- Trabalha com uma população (diversidade genética)
- Usa seleção (pressão seletiva), crossover (recombinação) e mutação (diversidade)
- Evolui soluções ao longo de gerações

Vantagens:
- Explora bem o espaço de busca
- Pode escapar de ótimos locais com facilidade
- Robusto para diferentes tipos de problemas

Desvantagens:
- Requer ajustes finos dos parâmetros (população, taxa de mutação)
- Uso intensivo de memória e tempo
- Mais complexo de implementar
"""

# Comparação geral entre os algoritmos
comparacao = {
    "Critério": [
        "Inspiração",
        "Estratégia",
        "Fuga de ótimos locais",
        "Parâmetros principais",
        "Velocidade",
        "Consistência",
        "Facilidade de implementação",
        "Adequado para"
    ],
    "Subida de Encosta": [
        "Escalada até o topo local",
        "Melhor vizinho sempre",
        "Reinício aleatório",
        "Número de reinícios",
        "Rápido",
        "Baixa",
        "Fácil",
        "Problemas simples"
    ],
    "Têmpera Simulada": [
        "Resfriamento de metais",
        "Aceita piores soluções",
        "Aceitação probabilística",
        "Temperatura e resfriamento",
        "Moderada",
        "Média",
        "Média",
        "Problemas com muitos picos"
    ],
    "Algoritmo Genético": [
        "Evolução biológica",
        "População evolutiva",
        "Diversidade genética",
        "População, mutação, crossover",
        "Pode ser lento",
        "Alta",
        "Média/Alta",
        "Problemas complexos e grandes"
    ]
}

if __name__ == "__main__":
    print("\n📊 Comparação entre algoritmos de otimização:\n")
    for i in range(len(comparacao["Critério"])):
        print(f"{comparacao['Critério'][i]}:")
        print(f"  - Subida de Encosta:   {comparacao['Subida de Encosta'][i]}")
        print(f"  - Têmpera Simulada:    {comparacao['Têmpera Simulada'][i]}")
        print(f"  - Algoritmo Genético:  {comparacao['Algoritmo Genético'][i]}\n")

    print("Dica: escolha o algoritmo com base na complexidade do seu problema e recursos disponíveis!")
