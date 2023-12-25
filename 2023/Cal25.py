import sys
import time
from aoc import *
import networkx as nx

def solve(path) :
    
    G = nx.Graph()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            left,rights = line.split(': ')
            G.add_node(left)
            for right in rights.split(' ') :
                G.add_node(right)
                G.add_edge(left, right)
    
    cut, pair = nx.stoer_wagner(G)
    
    if cut == 3 :
        g1, g2 = pair
        return len(g1) * len(g2)
    return -1
    
start_ns = time.time_ns()

print( solve('inputs/2023/25.example.txt') ) # 54
print( solve('inputs/2023/25.txt') ) # 558376

end_ns = time.time_ns()
printTime(end_ns - start_ns)
