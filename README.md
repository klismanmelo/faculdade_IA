# 2048 com Inteligência Artificial

Este projeto é uma implementação do clássico jogo 2048 utilizando `pygame` e uma IA com o algoritmo **Expectimax** para tomada de decisões.

## 🎮 O que é o jogo 2048?

2048 é um jogo de quebra-cabeça deslizante onde o objetivo é combinar blocos de números iguais até alcançar o bloco de valor `2048`. Cada movimento desliza todos os blocos para uma direção (esquerda, direita, cima ou baixo), combinando blocos iguais e gerando novos blocos aleatórios (2 ou 4).

## 🧠 O que este projeto faz?

Este projeto permite:

- Jogar 2048 manualmente com as setas do teclado
- Usar um agente IA com algoritmo **Expectimax** para simular decisões e encontrar a melhor jogada
- Visualizar o tabuleiro em tempo real com `pygame`
- Estender o jogo para estudos em Inteligência Artificial aplicada a jogos

---

## 🗂️ Estrutura dos Arquivos

- `game_2048.py`: Lógica do jogo, interface com pygame e controle de movimentos
- `expectimax.py`: Implementação da IA com algoritmo Expectimax para tomar decisões

---

## ▶️ Como Executar

### Pré-requisitos

- Python 3.7+
- pygame instalado

### Instalação

```bash
pip install pygame
```

### Executar o jogo

```bash
python main_ia_game.py
```

---

## 🤖 Executar a IA (Expectimax)

Você pode importar o `get_expectimax_move()` no seu próprio script ou usar para treinar bots. Exemplo de uso:

```python
from game_2048 import init_board, draw_board, add_random_tile, has_moves
from expectimax import get_expectimax_move

board = init_board()
draw_board(board)

while has_moves(board):
    move, score, all_scores = get_expectimax_move(board, depth=3)
    print(f"Melhor jogada: {move} | Pontuação esperada: {score}")
    # aplique o movimento e continue o jogo
```

---

## 📌 Como funciona o algoritmo Expectimax?

O Expectimax alterna entre dois tipos de nós:

- **Maximizador** (o jogador): busca o movimento com a melhor pontuação esperada
- **Expectativa** (o jogo): considera a média ponderada das possíveis inserções de peças (2 com 90% ou 4 com 10%)

A pontuação do tabuleiro é calculada com uma heurística simples: **soma de todos os valores + maior valor presente**.

---

## 🛠️ Extensões possíveis

- Melhorar a heurística (ex: cantos, espaços vazios, monotonicidade)
- Jogador automático com visualização da IA
- Interface para alternar entre jogador humano e IA

---

## 📸 Preview

![preview](https://upload.wikimedia.org/wikipedia/commons/7/75/2048_gameplay.gif)

---

## 📄 Licença

MIT ©Klismanmelo
