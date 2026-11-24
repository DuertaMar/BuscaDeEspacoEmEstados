from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult
from typing import Deque, Set


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        fila: Deque[State] = deque([initial])
        visitados: Set[State] = {initial}

        nos_expandidos: int = 0
        nos_gerados: int = 1
        max_fronteira: int = 1

        while len(fila) > 0:
            #Retira estado mais antigo
            atual: State = fila.popleft()
            nos_expandidos += 1

            #Verifica movimento por filho
            for filho in atual.neighbors():
                if filho not in visitados:
                    nos_gerados += 1

                    if filho.is_goal:
                        return SearchResult(
                            solution=filho,
                            nodes_expanded=nos_expandidos,
                            nodes_generated=nos_gerados,
                            max_frontier_size=max_fronteira,
                            depth=filho.cost,
                        )
                    #Se não é o objetivo, visitados
                    visitados.add(filho)
                    fila.append(filho)
                    #Atualiza tamanho fila
                    if len(fila) > max_fronteira:
                        max_fronteira = len(fila)
        #Se vazia ou sem solução
        return SearchResult(
            solution=None,
            nodes_expanded=nos_expandidos,
            nodes_generated=nos_gerados,
            max_frontier_size=max_fronteira,
            depth=0,
        )
        #raise NotImplementedError("Implemente o método search na classe BFS.")
