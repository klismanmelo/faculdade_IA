from collections import deque
import heapq

class Puzzle8:
    def __init__(self, initial_state):
        # Estado inicial do puzzle armazenado como tupla (imutável)
        self.initial_state = tuple(initial_state)
        # Estado objetivo final do puzzle (posição correta dos números)
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        
        # Dicionário que define os movimentos possíveis para cada posição do espaço vazio (0)
        self.moves = {
            0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
        }
        
        # Pré-calcula a posição final de cada número no estado objetivo para acelerar a heurística
        self.goal_positions = {val: idx for idx, val in enumerate(self.goal_state)}

    def heuristic(self, state):
        """
        Heurística do A*: calcula a soma das distâncias de Manhattan de cada peça 
        até sua posição correta no estado objetivo.
        """
        distance = 0
        for i, val in enumerate(state):
            if val == 0:
                continue  # Não considera o espaço vazio (0)
            goal_idx = self.goal_positions[val]  # Posição alvo do valor atual
            current_row, current_col = divmod(i, 3)  # Coordenadas atuais da peça  -> retorna uma tupla com dois valores (O quociente da divisão inteira de a por b & O resto dessa divisão)
            goal_row, goal_col = divmod(goal_idx, 3)  # Coordenadas da posição alvo
            # Soma as distâncias horizontais e verticais (Manhattan)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col) # Valor absoluto
        return distance

    def astar(self):
        """
        Implementação do algoritmo A* para encontrar o caminho da configuração inicial
        até o estado objetivo.
        """
        start = self.initial_state
        goal = self.goal_state

        # Fila de prioridade contendo tuplas: (custo estimado total, custo atual, estado atual, caminho até aqui)
        queue = [] # Cria uma fila de prioridade
        heapq.heappush(queue, (self.heuristic(start), 0, start, []))  # Transforma uma lista comum em uma heap (fila de prioridade)

        # Dicionário para guardar o menor custo já encontrado para cada estado
        visited = {}

        while queue:
            est_total, cost, state, path = heapq.heappop(queue)

            # Se alcançou o estado objetivo, retorna o caminho e número de estados testados
            if state == goal:
                return path, len(visited)

            # Se já visitou este estado com custo menor ou igual, ignora
            if state in visited and visited[state] <= cost:
                continue

            # Marca o estado como visitado com o custo atual
            visited[state] = cost

            zero_index = state.index(0)  # Localiza o espaço vazio
            # Gera novos estados trocando o espaço vazio com posições possíveis
            for move in self.moves[zero_index]:
                new_state = list(state)
                # Troca a posição do espaço vazio com o número adjacente
                new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
                new_tuple_state = tuple(new_state)

                new_cost = cost + 1  # Custo incrementa 1 a cada movimento
                est = new_cost + self.heuristic(new_tuple_state)  # Custo estimado total

                # Se não visitado ou se encontrou um caminho mais barato, adiciona à fila
                if new_tuple_state not in visited or visited[new_tuple_state] > new_cost:
                    heapq.heappush(queue, (est, new_cost, new_tuple_state, path + [new_tuple_state]))

        # Caso não encontre solução, retorna None e número de estados testados
        return None, len(visited)
    
    def bfs(self):
        """
        Busca em largura (BFS) para encontrar o caminho do estado inicial até o objetivo.
        Usado como referência, mas menos eficiente para 8-puzzle.
        """
        queue = deque([(self.initial_state, [])])
        visited = set()
        visited.add(self.initial_state)
        
        while queue:
            state, path = queue.popleft()

            # Se chegou ao estado objetivo, retorna caminho e estados testados
            if state == self.goal_state:
                return path, len(visited)
            
            zero_index = state.index(0)
            # Gera os próximos estados possíveis movendo o espaço vazio
            for move in self.moves[zero_index]:
                new_state = list(state)
                new_state[zero_index], new_state[move] = new_state[move], new_state[zero_index]
                new_tuple_state = tuple(new_state)
                
                if new_tuple_state not in visited:
                    queue.append((new_tuple_state, path + [new_tuple_state]))
                    visited.add(new_tuple_state)
        
        # Caso não encontre solução
        return None, len(visited)

# Função principal que lê a entrada do usuário, valida e executa a resolução pelo A*
def main():
    entrada = input("Digite o estado inicial (ex: 1 2 3 4 5 6 7 0 8): ")
    estado_inicial = entrada.split()
    
    # Valida se a entrada tem exatamente 9 números
    if len(estado_inicial) != 9 or not all(i.isdigit() for i in estado_inicial):
        print("Erro: A entrada deve conter exatamente 9 números separados por espaço.")
        return
    
    # Converte a lista de strings para inteiros
    estado_inicial = list(map(int, estado_inicial))
    
    # Valida se os números de 0 a 8 estão presentes e sem repetições
    if set(estado_inicial) != set(range(9)):
        print("Erro: A entrada deve conter os números de 0 a 8 sem repetições.")
        return
    
    # Cria o objeto Puzzle8 com o estado inicial
    puzzle = Puzzle8(estado_inicial)
    # Executa o algoritmo A* para resolver o puzzle
    caminho, estados_testados = puzzle.astar()
    
    if caminho:
        print("Solução encontrada!")
        # Exibe cada passo do caminho da solução
        for step in caminho:
            print(step)
        print(f"Número de estados testados: {estados_testados}")
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
