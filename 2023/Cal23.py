import sys
import time
import re
from aoc import *

from collections import deque
from collections import defaultdict
# from itertools import combinations
# from itertools import combinations_with_replacement
# from itertools import permutations
# from itertools import pairwise
# from itertools import cycle
# from operator import itemgetter
import heapq


MOVES = { '>' : [(1,0,'>')], '<' : [(-1,0,'<')], 'v' : [(0,1,'v')], '^' : [(0,-1,'^')], '.' : [(0,1,'S'), (0,-1,'N'), (1,0,'E'), (-1,0,'W')]}
MOVES2 = [(0,1,'S'), (0,-1,'N'), (1,0,'E'), (-1,0,'W')]
STARTX, STARTY = 1, 0
MAXX = MAXY = 0

# get possible moves (depends on which part we are)
def getMoves(map,x,y,part):
    if part == 1 :
        ch = map[y][x]
        return MOVES[ch]
    if part == 2 :
        return MOVES2
    assert( False )

# from a position return possible exits
def getExits(map,x,y,part):
    exits = list()
    for dx,dy,_ in getMoves(map,x,y,part) :
        xx = x + dx
        yy = y + dy
        if 0 <= xx < MAXX and 0 <= yy < MAXY and map[yy][xx] != '#' :
            exits.append( (xx,yy) )
    return exits

# from an intersection or start :
# follow every path in every possible direction
# stop path when cycling or when at an intersection
# note : intersection is a node with more than two exits OR final node (fx,fy)
def nextIntersections(map,sx,sy,fx,fy,part) :
    res = list()
    for ex in getExits(map,sx,sy,part) :
        done = set()
        done.add( (sx,sy) )
        todo = deque()
        x,y = ex
        todo.append( (x,y) )
        count = 1
        while todo :
            x,y = todo.popleft()
            if x == fx and y == fy :
                # at finish
                res.append( (x,y,count) )
                break
            exits = getExits(map,x,y,part)
            if len(exits) > 2 :
                # end of path
                res.append( (x,y,count) )
                break
            count += 1
            done.add( (x,y) )
            for ex in exits :
                if ex not in done :
                    todo.append(ex)
    return res


# as map is essentially long corridors, pre-compute path from intersections to intersections
# (with correct count)
# graph : (x,y) -> [ (x1,y1,steps1), (x2,y2,steps2), ... ]
# note that all intersections lead to many routes (except route to finish maybe)
def buildGraph(map, sx, sy, fx, fy, part) :
    graph = defaultdict(set)
    done = set()
    todo = deque()
    todo.append( (sx,sy) )
    while todo :
        x,y = todo.popleft()
        if (x,y) in done :
            continue
        done.add( (x,y) )
        nexts = nextIntersections(map,x,y,fx,fy,part)
        for nx,ny,count in nexts :
            if nx != STARTX or ny != STARTY : # do not get back to start
                graph[(x,y)].add((nx,ny,count))
            todo.append( (nx,ny) )
        
    return graph

def solve(path, part) :
    
    global MAXX, MAXY
    
    MAX = MAXX*MAXY
    
    map = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            map.append(list(line))
            
    MAXY = len(map)
    MAXX = len(map[0])
    FINISHX = MAXX - 2
    FINISHY = MAXY - 1
    assert map[FINISHY][FINISHX] == '.'
    STARTX, STARTY = 1,0
    MAX=MAXX*MAXY # heapq key
    
    graph = buildGraph(map, STARTX, STARTY, FINISHX, FINISHY, part)
    
    todo = []
    heapq.heapify(todo)
    heapq.heappush(todo, (MAX,STARTX, STARTY, 0, set()) )
    best = 0
    steps = 0
    while todo :
        steps += 1
        _,x,y,count,pp = heapq.heappop(todo)
        nexts = graph.get( (x,y) )
        for nx,ny,cc in nexts :
            if (nx,ny) in pp : # dont visit twice
                continue
            if nx == FINISHX and ny == FINISHY :
                best = max(best, count + cc)
                continue
            np = pp.copy()
            np.add( (nx,ny) )
            nc = count+cc
            heapq.heappush(todo, (MAX-nc,nx,ny,nc,np))
    return best



start_ns = time.time_ns()

print( solve('inputs/2023/23.example.txt', 1) ) # 94
print( solve('inputs/2023/23.example.txt', 2) ) # 154
print()
print( solve('inputs/2023/23.txt', 1) ) # 2110
print( solve('inputs/2023/23.txt', 2) ) # 6514


end_ns = time.time_ns()
printTime(end_ns - start_ns)
