from __future__ import annotations
from typing import (
    TypeVar,
    Iterable,
    Sequence,
    Generic,
    List,
    Callable,
    Set,
    Deque,
    Dict,
    Any,
    Optional,
)
from typing_extensions import Protocol
from heapq import heappush, heappop

# um tipo T genérico
T = TypeVar("T")

#Implementação de uma pilha LIFO baseada em uma lista
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # negação é verdadeira se o container for vazio

    #adiciona
    def push(self, item: T) -> None:
        self._container.append(item)

    #retira do topo
    def pop(self) -> T:
        return self._container.pop()  # LIFO

    def __repr__(self) -> str:
        return repr(self._container)

#implementação de fila
class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container  # negação é verdadeira se o container for vazio

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # FIFO - elemento mais antigo será eliminado primeiro

    def __repr__(self) -> str:
        return repr(self._container)

'''
Mantém o controle de como se passa de um estado para outro, um Wrapper

Um Wrapper é um decorator em Python, 
que nada mais é que um método para envolver uma função, modificando seu comportamento

No caso do problema do labirinto, tais estados são do tipo MazeLocation (tupla de localização)

Um node será chamado do qual um estado se originou de seu parent (uma location da pilha com locations)

Um Optional Node será fornecido ou caso contrário, o valor será none
'''

class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic
        #print(self.heuristic)

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
'''
busca em profundidade - vai a máxima profundidade possível, antes de retroceder ao último ponto de
decisão se encontrar um caminho sem saída

utiliza um Callable, que é algo como uma classe abstrata

Um callable é um objeto que permite usar parênteses () 
e, eventualmente, passar alguns parâmetros, assim como funções.

manterá o controle de duas estruturas de dados: a pilha de estados possíveis de serem buscados, 
frontier; estados já buscados denominados explored
'''
def dfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
) -> Optional[Node[T]]:
    # frontier são os lugares não visitados
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # explored são lugares já visitados
    explored: Set[T] = {initial}

    # continua enquanto houver lugares a explorar
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # se o objetivo for encontrado, termina a busca no node atual (nó, coordenada)
        if goal_test(current_state):
            return current_node
        # verifica para onde se pode ir e que não tenha sido explorado
        for child in successors(current_state):
            if child in explored:  # ignora filhos já explorados
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # Se passar por todos os lugares sem atingir o objetivo, não há solução


'''
busca em largura - a busca em profundidade, em geral, não encontra os caminhos mais curtos
a busca em largura sempre encontra o caminho mais curto, analisa sistematicamente uma camada de nós
mais distante do estado inicial em cada iteração de busca

A dfs pode ser mais rápida que a bfs, porém não há certeza de caminho mais curto como na bfs

A bfs usará uma fila FIFO, em que os elemento mais antigos sairão primeiro e estarão simbolicamente
à esquerda

'''
def bfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
) -> Optional[Node[T]]:
    # frontier corresponde aos lugares que ainda devem ser visitados
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored representa lugares já visitados
    explored: Set[T] = {initial}

    # continua enquanto houver mais lugares para explorar
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # se o objetivo for encontrado, finaliza a busca
        if goal_test(current_state):
            return current_node
        # verifica e irá para lugares que não foram explorados
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None  # não existem mais lugares a serem explorados e o o bjetivo não foi encontrado


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]], heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't explored
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1  # 1 assumes a grid, need a cost function for more sophisticated apps

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None  # went through everything and never found goal



'''
Partindo do nó de objetivo devolvido, é possível reconstruir o caminho do labirinto pela função
abaixo, desempilhando os nós (nodes)
'''
def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # trabalha do sentido inverso, do final ao início
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
        
    path.reverse()
    return path

