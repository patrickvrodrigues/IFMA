from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from core.maze.generic_search import dfs, bfs, astar,node_to_path, Node
import time
import timeit
'''
Serão ilustrados os problemas de busca em profundidade e busca em largura em um labirinto
O Labirinto é bidimensional, em forma de uma caixa ou grade
'''


'''
Aqui a classe Cell é uma célula do labirinto. 
A reprentação é feita por um enum de strings.
Vazio (“ “), bloqueado (“X”), início (“S”), chegada (“G”) 
e caminho (“*”) são as opções, traduzidas do inglês.
'''
class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"

'''
MazeLocation é uma classe que recebe uma tupla composta por 
linha (row) e coluna (column), uma coordenada que 
representa um lugar específico no labirinto gerado.

Representação de um local no labirinto
'''
class MazeLocation(NamedTuple):
    row: int
    column: int

#Aqui o labirinto é inicializado com (__init__), construtor
class Maze:
    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        sparseness: float = 0.2,
        start: MazeLocation = MazeLocation(0, 0),
        goal: MazeLocation = MazeLocation(9, 9),
    ) -> None:
        # inicializa as variáveis de instância básicas
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # preenche a grade ou caixa com cells o tipo 'EMPTY', vazias
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(columns)] for r in range(rows)
        ]
        # preenche a grade ou caixa com cells o tipo 'BLOCKED'
        self._randomly_fill(rows, columns, sparseness)
        # preenche as posições inicial (START) e final (GOAL)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    '''tal função definirá quão espaço o labirinto será, através do parâmetro sparseness
    o default é 20% das posições bloqueadas, se o número gerado por random for menor que 20%,
    os espaços vazios serão preenchidos por células bloqueadas ou paredes
    '''
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    # devolve uma versão do labirinto formatado para exibiçao
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output
    '''
    Recebe uma MazeLocation e returna um bool (comparando ml 
    com a chegada do labirinto gerado). Se ml for igual 
    a chegada, returna true, caso contrário, false.
    
    Testa a chegada do labirinto
    '''
    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    '''
    Como se mover no labirinto? 
    A função successors ficará responsável por isso
    
    No código, uma lista de MazeLocation é criada, denominada locations. 
    
    Ela guardará as posições percorridas no labirinto. 

    A ordem é ml.row + 1, ml.row -1, ml.column +1, ml.column -1 ou 
    acima, abaixo, direita, esquerda, respectivamente.
    
    Se a célula for diferente de Cell.Blocked, caminha para a 
    posição em questão, caso contrário, passa para a próxima.
    
    As MazeLocation fora da caixa do labirinto não são verificadas
    
    Uma lista com todas as localidades possíveis é construída e retornada (locations)
    '''
    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if (
            ml.row + 1 < self._rows
            and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if (
            ml.column + 1 < self._columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    '''
    Na função mark:
    
    para exibição, será marcado o caminho percorrido ("PATH") na lista devolvida (pilha)
    
    será marcada a linha e coluna que representa o início (start) (estado inicial)
    
    e a linha e coluna que representa a chegada (goal) (estado final)
    '''

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    '''
    A função clear remove o caminho percorrido, permitindo testar um algoritmo de 
    busca diferente no mesmo labirinto gerado
    '''

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        print(ml)
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        #print("Resultado--------------")
        #print("Coluna: "+ str(xdist))
        #print("Linha: " + str(ydist))
        #print("##########################")
        #print(xdist + ydist)
        return (xdist + ydist)
    return distance

'''if __name__ == "__main__":

    # gera labirinto e escreve
    m: Maze = Maze()
    print("LABIRINTO GERADO")
    print(m)

    # test DFS
    inicio = timeit.default_timer()
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    fim = timeit.default_timer()
    if solution1 is None:
        print("Sem solução para a depth-first search!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print("SOLUÇÃO COM DFS")
        print(m)
        m.clear(path1)
        print('tempo de execução da DFS: %f' % (fim - inicio))
    # test BFS
    inicio = timeit.default_timer()
    solution2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test, m.successors)
    fim = timeit.default_timer()
    if solution2 is None:
        print("Sem solução para a breadth-first search!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        print("SOLUÇÃO COM BFS")
        print(m)
        m.clear(path2)
        print('tempo de execução da BFS: %f' % (fim - inicio))
'''
def runWeb():
    #Um dicionario que armazena tudo que vai para a página web
    labirintoDados = {}
    # gera labirinto e escreve
    m: Maze = Maze()

    labirintoDados['original'] = percorreAlgoritimo(m)
    
    # test DFS
    inicio = timeit.default_timer()
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    #print(dir(solution1.state))
    fim = timeit.default_timer()
    if solution1 is None:
        labirintoDados['dfs'] = None
        #print("Sem solução para a depth-first search!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        #print("SOLUÇÃO COM DFS")
        #print(m)
        labirintoDados['dfs'] = percorreAlgoritimo(m)
        labirintoDados['dfs_temp'] = fim - inicio

        m.clear(path1)
        #m.clear(path_teste)
        #print('tempo de execução da DFS: %f' % (fim - inicio))
    # test BFS
    inicio = timeit.default_timer()
    solution2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test, m.successors)
    fim = timeit.default_timer()
    if solution2 is None:
        labirintoDados['bfs'] = None
        #print("Sem solução para a breadth-first search!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        #print("SOLUÇÃO COM BFS")
        #print(m)
        labirintoDados['bfs'] = percorreAlgoritimo(m)
        labirintoDados['bfs_temp'] = fim - inicio
        m.clear(path2)
        #print('tempo de execução da BFS: %f' % (fim - inicio))

    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    inicio = timeit.default_timer()
    solution3: Optional[Node[MazeLocation]] = astar(m.start, m.goal_test, m.successors, distance)
    fim = timeit.default_timer()
    if solution3 is None:
        labirintoDados['astar'] = None
        #print("Sem solução para a breadth-first search!")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        m.mark(path3)
        #print("SOLUÇÃO COM BFS")
        #print(m)
        labirintoDados['astar'] = percorreAlgoritimo(m)
        labirintoDados['astar_temp'] = fim - inicio
        m.clear(path3)
        #print('tempo de execução da BFS: %f' % (fim - inicio))

    return labirintoDados
#Percorre todo o algoritimo para criar uma cópia da matriz do labirinto
def percorreAlgoritimo(m):
    lista = []
    for te in m._grid:
        lis = []
        for t in te:
            if t[0]== " ":
                lis.append(" ")
            if t[0]== "X":
                lis.append("X")
            if t[0]== "S":
                lis.append("S")
            if t[0]== "G":
                lis.append("G")
            if t[0]== "*":
                lis.append("*")
        lista.append(lis)
    return lista


