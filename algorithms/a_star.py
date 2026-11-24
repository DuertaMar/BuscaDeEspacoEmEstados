import heapq
from typing import Dict, List, Tuple
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distancia: int = 0

        for pos_atual in range(9):
            valor: int = state.tiles[pos_atual]

            if valor != 0:
                pos_final: int = GOAL_STATE.index(valor)

                lin_atual: int = pos_atual // 3 #Vetor Matriz Linha
                col_atual: int = pos_atual % 3 #Vetor Matriz coluna

                lin_final: int = pos_final // 3 #Vetor Matriz linha final
                col_final: int = pos_final % 3 #Vetor Matriz coluna final

                diff_lin: int = lin_atual - lin_final #Diferença linha
                if diff_lin < 0:
                    diff_lin = -diff_lin

                diff_col: int = col_atual - col_final #Diferença coluna
                if diff_col < 0:
                    diff_col = -diff_col

                distancia += diff_lin + diff_col 

        return distancia
        # raise NotImplementedError

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        # Prioridade custo_f, estado, menor caminho para A* 
        f_inicial: int = initial.cost + self.heuristic(initial)
        fila: List[Tuple[int, State]] = [(f_inicial, initial)]

        # Guarda o menor custo, encontrado para cada tabuleiro
        melhor_custo: Dict[State, int] = {initial: 0}

        nos_expandidos: int = 0
        nos_gerados: int = 1
        max_fronteira: int = 1

        while len(fila) > 0:
            #Pega o menor custo
            custo_f, atual = heapq.heappop(fila)
            nos_expandidos += 1

            for filho in atual.neighbors():
                #Só busca se for menor custo ou um novo
                if filho not in melhor_custo or filho.cost < melhor_custo[filho]:
                    melhor_custo[filho] = filho.cost
                    nos_gerados += 1

                    if filho.is_goal:
                        return SearchResult(
                            solution=filho,
                            nodes_expanded=nos_expandidos,
                            nodes_generated=nos_gerados,
                            max_frontier_size=max_fronteira,
                            depth=filho.cost,
                        )
                    #Calculo do custo, passo, distância
                    custo_total: int = filho.cost + self.heuristic(filho)
                    heapq.heappush(fila, (custo_total, filho))

                    #Atualiza tamanho fila
                    if len(fila) > max_fronteira:
                        max_fronteira = len(fila)
        # Se vazia ou sem solução
        return SearchResult(
            solution=None,
            nodes_expanded=nos_expandidos,
            nodes_generated=nos_gerados,
            max_frontier_size=max_fronteira,
            depth=0,
        )
        # raise NotImplementedError
