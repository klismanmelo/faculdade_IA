import matplotlib.pyplot as plt

def show_move_evaluation(move_scores, chosen_move):
    import matplotlib.pyplot as plt

    directions = list(move_scores.keys())
    scores = [move_scores[dir] for dir in directions]

    colors = ['green' if dir == chosen_move else 'gray' for dir in directions]

    plt.figure(figsize=(6, 4))
    plt.bar(directions, scores, color=colors)
    plt.title(f"IA Escolheu: {chosen_move}")
    plt.xlabel("Movimentos possíveis")
    plt.ylabel("Pontuação da heurística")
    plt.ylim(min(scores) - 10, max(scores) + 10)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    
    plt.show(block=False)  # não bloqueia o loop
    plt.pause(2)           # mostra por 2 segundos
    plt.close()            # fecha a janela
