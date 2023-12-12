import sys
import time
from aoc import printTime

from collections import defaultdict
from itertools import combinations

start_ns = time.time_ns()

def solve(path, emptyFactor):

    grid = list();
    with open(path) as file :
        y = 0  # original value
        for l in file :
            line = l.rstrip()
            grid.append(list(line))

    MAXY = len(grid)
    MAXX = len(grid[0])

    emptyLines = set()
    for y in range(MAXY) :
        if all( [grid[y][x] == '.' for x in range(MAXX)] ) :
            emptyLines.add(y)
        
    emptyCols = set()
    for x in range(MAXX) :
        if all( [grid[y][x] == '.' for y in range(MAXY)] ) :
            emptyCols.add(x)
    
    STARS = list()
    for y in range(MAXY) :
        for x in range(MAXX) :
            if grid[y][x] == '#' :
                # adjust coords
                xx = x + len(set(range(x)) & emptyCols) * (emptyFactor - 1)                
                yy = y + len(set(range(y)) & emptyLines) * (emptyFactor - 1)                
                STARS.append((xx,yy))
                
    #  compute
    res = 0
    for s1,s2 in combinations(STARS, 2) :
        res += abs(s2[0]-s1[0]) + abs(s2[1]-s1[1])
    return res

print("example")
print( solve("inputs/2023/11.example.txt", 2) )
print( solve("inputs/2023/11.example.txt", 10) )
print( solve("inputs/2023/11.example.txt", 100) )
print("solutions")
print( solve("inputs/2023/11.txt", 2) )
print( solve("inputs/2023/11.txt", 1_000_000) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
