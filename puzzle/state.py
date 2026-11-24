from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

MOVIMENTOS: List[Tuple[str, int, int]] = [("BAIXO", 1, 0), ("CIMA", -1, 0),
    ("DIREITA", 0, 1), ("ESQUERDA", 0, -1),]

class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        filhos: List[State] = [] 
        indice_atual: int = self.blank_index #Posição 0 

        linha_atual: int = indice_atual // 3  # Vetor Matriz Linha
        coluna_atual: int = indice_atual % 3  # Vetor Matriz Coluna

        #Direção teste
        for acao, passo_linha, passo_coluna in MOVIMENTOS:
            nova_linha: int = linha_atual + passo_linha
            nova_coluna: int = coluna_atual + passo_coluna

            # Limite matriz
            if nova_linha >= 0 and nova_linha < 3 and nova_coluna >= 0 and nova_coluna < 3:
                novo_indice: int = (nova_linha * 3) + nova_coluna #Retorna Matriz para Vetor

                #Troca o 0
                novo_tabuleiro: List[int] = list(self.tiles)
                temporario: int = novo_tabuleiro[indice_atual]
                novo_tabuleiro[indice_atual] = novo_tabuleiro[novo_indice]
                novo_tabuleiro[novo_indice] = temporario

                # Apontamento filho-pai, criação
                filho: State = State(
                    tiles=tuple(novo_tabuleiro), parent=self,
                    action=acao, cost=self.cost + 1,)
                filhos.append(filho)

        return filhos

        #"""Retorna os estados filhos válidos a partir deste estado."""
        #raise NotImplementedError

    def path(self) -> List["State"]:
        estados = []
        atual = self
        while atual is not None:
            estados.append(atual)
            atual = atual.parent
        estados.reverse() #Inverte a ordem
        return estados

        #"""Retorna a sequência de estados do estado inicial até este."""
        #raise NotImplementedError

    def actions(self) -> List[str]:

        resultado = []
        for estado in self.path():
            if estado.action is not None:
                resultado.append(estado.action)
        return resultado
    
        #"""Retorna a sequência de ações do estado inicial até este."""
        # TODO: implemente usando path()
        #raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
