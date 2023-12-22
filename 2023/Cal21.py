import sys
import time
import re
from aoc import *

from collections import deque
from collections import defaultdict

MAXX = MAXY = 0
MOVES = [ (1,0), (0,1), (-1,0), (0,-1) ]


def doStep(map, steps, sx, sy) :
    toDo = set()
    toDo.add((sx,sy))
    c = 0
    while c < steps :
        toDoNext = set()
        for x,y in toDo :
            for dx, dy in MOVES :
                nx = x + dx
                ny = y + dy
                if 0 <= nx < MAXX and 0 <= ny < MAXY and map[ny][nx] == '.' :
                    toDoNext.add((nx, ny))
        toDo = toDoNext
        c += 1
    
    return len(toDo)

def doStep2(map, steps, sx, sy) :

    counts = list()
    
    toDo = set()
    toDo.add((sx,sy))
    counts.append(len(toDo))
    step = 0
    while step < steps :
        step += 1
        toDoNext = set()
        for x,y in toDo :
            for dx, dy in MOVES :
                nx = x + dx
                ny = y + dy
                if map[ny%MAXY][nx%MAXX] == '.' :
                    toDoNext.add((nx,ny))
        toDo = toDoNext
        counts.append(len(toDo))
        
        if step > 350 : # enough data to find a cycle
            break
    
    # compute cycle
    
    # assume cycleLen is board size (as seen on extracted data ...)
    cLen = MAXX
    
    diffClen = list() # diff of counts from one full cycle to the other
    for idx in range(step - cLen) :
        diffClen.append(counts[idx+cLen] - counts[idx])
 
    diffDiff = list() # successive diffs between diffs we just computed before
    for idx in range(len(diffClen)-1) :
        diffDiff.append(diffClen[idx+1]-diffClen[idx])
    
    cycleDiff = sum(diffDiff[-cLen:]) # value from which diff varies between cycles, constant value
    
    # do the computation
    step = cLen * 2
    while (steps - step) % cLen != 0 :
        step += 1 # adjust cycle so that we will be perfect
    
    count = counts[step]        # starting point for cycle computation
    diff = diffClen[step-cLen]  # diff between counts
    while step < steps :
        diff += cycleDiff # diff increases
        count += diff     # count increase by diff
        step += cLen      # more steps !
            
    assert step == steps # should be right on spot
    return count


def solve(path, part, steps) :

    global MAXX, MAXY
    
    res = 0
    x = y = -1
    
    map = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            map.append(list(line))
            
    MAXY = len(map)
    MAXX = len(map[0])
    
    y = 0
    for row in map :
        if 'S' in row :
            x = row.index('S')
            break;
        y += 1
    map[y][x] = '.'

    if part == 1 :
        return doStep(map, steps, x, y)
    
    assert x == (MAXX-1) // 2 and y == (MAXY-1) // 2 # S at center
    assert all(map[y][i] == '.' for i in range(MAXX))
    assert all(map[i][x] == '.' for i in range(MAXY))

    return doStep2(map, steps, x, y)


start_ns = time.time_ns()

print( solve('inputs/2023/21.example.txt', 1, 6) ) # 16
print( solve('inputs/2023/21.txt', 1, 64) ) #3743
print( solve('inputs/2023/21.txt', 2, 26501365) )  # 618261433219147

end_ns = time.time_ns()
printTime(end_ns - start_ns)
