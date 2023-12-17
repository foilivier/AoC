import sys
import time
import heapq
from aoc import *

#                 S      E       N       W
S,E,N,W   =       0,     1,      2,      3
MOVES     = [ (0,1), (1,0), (0,-1), (-1,0) ]
DIRS_NEXT = [ [E,W], [S,N],  [E,W],  [S,N] ]
MAXX = MAXY = 0


def solve(path, minStraight, maxStraight) :
    
    global MAXX, MAXY
    
    map = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            map.append( [int(x) for x in list(line)])

    MAXY = len(map)
    MAXX = len(map[0])

    cache = dict() # (x,y,inDir) -> loss
    queue = [] # (loss,dir,x,y), priority list sorted by loss then dir
    
    queue.append( (0,E,0,0) )
    queue.append( (0,S,0,0) )
    
    best = sys.maxsize
    
    while queue :
        
        loss,dir,x,y = heapq.heappop(queue)

        if loss >= best :
            continue

        if x == MAXX-1 and y == MAXY-1 :
            best = min(best, loss)
            continue

        # predict smallest loss until end
        if loss + (MAXX - x - 1) + (MAXY - y -1) > best :
            continue

        key = (x,y,dir)
        done = cache.get( key )
        if done is not None and done <= loss :
            continue
        cache[key] = loss
        
        steps = minStraight
        dx, dy = MOVES[dir]
        for steps in range(1, maxStraight + 1) :
            x += dx
            y += dy
            if x < 0 or y < 0 or x >= MAXX or y >= MAXY :
                break
            loss += map[y][x]
            if steps >= minStraight :
                for nextDir in DIRS_NEXT[dir] :
                    heapq.heappush(queue, (loss,nextDir,x,y) ) 
            steps += 1

    return best


start_ns = time.time_ns()

# print( solve('inputs/2023/17.example.txt',1,3) )
# print( solve('inputs/2023/17.example.txt',4,10) )
# print( solve('inputs/2023/17.example2.txt',4,10) )

print( solve('inputs/2023/17.txt',1,3) )
print( solve('inputs/2023/17.txt',4,10) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
