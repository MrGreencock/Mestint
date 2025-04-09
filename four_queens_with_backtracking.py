"""
Ez a N királynő probléma kényszerkielégítéssel
változók: a tábla, amiben a királynők pozicióját tárolom (board).
tartomány: a 16 mező (graph).
kényszerek: sor_i != sor_j vagy oszlop_i != oszlop_j vagy |sor_i - sor_j| != |oszlop_i - oszlop_j|

"""

import networkx as nx
import matplotlib.pyplot as plt
import random


def is_consistent(graph, position):
    for i in range(len(position)):
        for j in range(i+1,len(position)):
            if graph[position[i]][position[j]] == 1:
                return False

    return True

"""
Randomizálva próbálja mezőket
Mivel mindig csak a 1 7 8 14-et találja,
ezért variáltam meg a random.shuffle(candidates) használatával.
Bár jobban belegondolva csak 2 megoldása van, ha nem nézzük a randomizált sorrendet...
"""


def backtracking(graph, position, v, queens, h = None):
    #print(position)
    if v == queens:
        return h(graph, position)

    candidates = [i for i in range(len(graph))]
    random.shuffle(candidates)

    for i in candidates:
        if i not in position:
            position[v] = i
            if backtracking(graph, position, v+1, queens, h):
                return True
            position[v] = -1
    #print(position)
    return False


"""
1. sor: 0 1 2 3 
2. sor: 4 5 6 7 
3. sor: 8 9 10 11 
4. sor: 12 13 14 15

"""

queens = 4
board_size = pow(queens, 2)
graph = [[0 for j in range(board_size)] for i in range(board_size)]


for i in range(board_size):
    row = i // 4
    col = i % 4
    for j in range(board_size):
        row_j = j // 4
        col_j = j % 4
        if row == row_j or col == col_j or abs(row - row_j) == abs(col - col_j):
            graph[i][j] = 1

        if i == j:
            graph[i][j] = 0


"""for i in range(16):
    for j in range(16):
        if graph[i][j] == 1:
            print(j, end=" ")
    print()"""


board = []
for i in range(queens):
        board = [-1] * queens
        if backtracking(graph, board, 0, queens, is_consistent):
            print(board)
            break


G = nx.Graph()
for i in range(len(graph)):
    for j in range(i+1, len(graph)):
        if graph[i][j]:
            G.add_edge(i+1, j+1)


node_colors = []
for node in G.nodes:
    if node in board:
        node_colors.append('red')
    else:
        node_colors.append('lightgray')

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True,node_color=node_colors, node_size=800, font_size=16, font_color='black')
plt.title("4 Királynő problémája")
plt.show()







