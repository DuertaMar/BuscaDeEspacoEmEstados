from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult
from typing import List, Set, Tuple

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        # Estado, profundidade, ancestrais
        pilha: List[Tuple[State, int, Set[State]]] = [(initial, 0, {initial})]

        nos_expandidos: int = 0
        nos_gerados: int = 1
        max_fronteira: int = 1

        while len(pilha) > 0:
            # Retira estado mais recente
            atual, profundidade, ancestrais = pilha.pop()

            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=nos_expandidos,
                    nodes_generated=nos_gerados,
                    max_frontier_size=max_fronteira,
                    depth=profundidade,
                )

            # Expande se não é limite
            if profundidade < self.depth_limit:
                nos_expandidos += 1

                vizinhos: List[State] = atual.neighbors()
                vizinhos.reverse() #Inverte por causa da pilha (esquerda, direita, cima, baixo)

                for filho in vizinhos:
                    # Filho por vizinho e não passado
                    if filho not in ancestrais:
                        nos_gerados += 1

                        novos_ancestrais: Set[State] = set(ancestrais)
                        novos_ancestrais.add(filho)

                        pilha.append((filho, profundidade + 1, novos_ancestrais))

                        if len(pilha) > max_fronteira:
                            max_fronteira = len(pilha)

        # Se vazia ou sem solução
        return SearchResult(
            solution=None,
            nodes_expanded=nos_expandidos,
            nodes_generated=nos_gerados,
            max_frontier_size=max_fronteira,
            depth=0,
        )
        #raise NotImplementedError("Implemente o método search na classe DFS.")
