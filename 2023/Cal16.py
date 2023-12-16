import sys
import time
import re
from aoc import *

MAXX = MAXY = 0
REFLECTIONS = { ('>','|'):('^','v'), ('>','/'):('^'), ('>','\\'):('v'), ('<','|'):('^','v'), ('<','/'):('v'), ('<','\\'):('^'), ('v','-'):('<','>'), ('v','/'):('<'), ('v','\\'):('>'), ('^','-'):('<','>'), ('^','/'):('>'), ('^','\\'):('<') } 
ADVANCE = { '>':(1,0), '<':(-1,0), 'v':(0,1), '^':(0,-1) }

def solve(path, part) :

    global MAXX, MAXY
    
    tiles = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            tiles.append(list(line))
    
    MAXX = len(tiles[0])
    MAXY = len(tiles)

    if part == 1 :
        return run(tiles, '>', (0,0) )
    
    # part2
    res = 0
    # from top dir = v
    for x in range(MAXX) :
        res = max(res, run(tiles, 'v', (x,0) ))
    # from bottom dir = ^
    for x in range(MAXX) :
        res = max(res, run(tiles, '^', (x,MAXY-1) ))
    # from left dir = >
    for y in range(MAXY) :
        res = max(res, run(tiles, '>', (0,y) ))
    # from right dir = <
    for y in range(MAXY) :
        res = max(res, run(tiles, '<', (MAXX-1,y) ))
    return res

def run(tiles, dir, pos) :
    
    beams = set() # cache (x,y,dir) 
    x,y = pos
    
    # solve reflections on start position (from IN dir to OUT dir)
    reflections = REFLECTIONS.get( (dir,tiles[y][x]) )
    if reflections == None :
        reflections = (dir,) # do not change
    
    # run baby, run !
    for reflected in reflections :
        throwRay(tiles, beams, pos, reflected)

    # remove duplicates (cache key is (x,y,dir), we want unique (x,y))
    res = set()
    for x,y,_ in beams :
        res.add( (x,y) )
    return len(res) 


def throwRay(tiles, beams, pos, dir) :

    # ray goes OUT of tile at (x,y) in given direction
    x,y = pos
    d = dir
    
    while True :
        key = (x,y,d)
        if key in beams :
            return # already done         
        beams.add(key)
        
        # prepare to move
        dx,dy = ADVANCE[d]
        nextX = x + dx
        nextY = y + dy
        if nextX < 0 or nextY < 0 or nextX >= MAXX or nextY >= MAXY :
            return # out of bounds
        next = tiles[nextY][nextX]
        reflections = REFLECTIONS.get( (d,next) ) # from IN dir to OUT dir(s)
        if reflections == None :
            reflections = (d,) # direction does not change
        
        if len(reflections) == 1 :
            # continue following ray within this loop (too much recursion is bad)
            x,y,d = nextX, nextY, reflections[0]
        else :
            # recurse
            for reflected in reflections :
                throwRay(tiles, beams, (nextX, nextY), reflected)
            break


start_ns = time.time_ns()

print( solve('inputs/2023/16.example.txt', 1) )
print( solve('inputs/2023/16.example.txt', 2) )
print()
print( solve('inputs/2023/16.txt', 1) )
print( solve('inputs/2023/16.txt', 2) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
