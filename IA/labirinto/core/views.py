from django.shortcuts import render
from core.maze import maze

# Create your views here.
def index(request):
    context = {}
    labirinto = maze.runWeb()
    dfs = labirinto['dfs']
    bfs = labirinto['bfs']
    astar = labirinto['astar']
    try:
        context['original'] = labirinto['original']
        context['dfs'] = labirinto['dfs']
        context['dfs_temp'] = labirinto['dfs_temp']
        context['dfs_custo'] = contador_custo(dfs)
    except:
        context['dfs'] = None
    try:
        context['bfs'] = labirinto['bfs']
        context['bfs_temp'] = labirinto['bfs_temp']
        context['bfs_custo'] = contador_custo(bfs)
    except:
        context['bfs'] = None
    try:
        context['astar'] = labirinto['astar']
        context['astar_temp'] = labirinto['astar_temp']
        context['astar_custo'] = contador_custo(astar)
    except:
        context['astar'] = None
    return render(request,'index.html',context)

def contador_custo(lista):
    contador = 0
    for lis in lista:
        for l in lis:
            if l == "*":
                contador = contador +1
    return contador