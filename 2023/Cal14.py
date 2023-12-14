import sys
import time
import re
from aoc import *
from itertools import count

MAXX = MAXY = 0


def weightNorth(rocks) :
    res = 0
    weight = MAXY
    for row in rocks :
        res += row.count('O') * weight
        weight -= 1
    return res


def slideNorth(rocks) :
    for y in range(MAXY) :
        for x in range(MAXX) :
            v = rocks[y][x]
            if v == 'O' :
                yy = y
                while 1 <= yy and rocks[yy-1][x] == '.' :
                    yy -= 1
                if y != yy :
                    rocks[y][x] = '.'
                    rocks[yy][x] = 'O' 


def slideSouth(rocks) :
    for y in reversed(range(MAXY)) :
        for x in range(MAXX) :
            v = rocks[y][x]
            if v == 'O' :
                yy = y
                while yy+1 < MAXY and rocks[yy+1][x] == '.' :
                    yy += 1
                if y != yy :
                    rocks[y][x] = '.'
                    rocks[yy][x] = 'O' 


def slideWest(rocks) :
    for x in range(MAXX) :
        for y in range(MAXY) :
            v = rocks[y][x]
            if v == 'O' :
                xx = x
                while 1 <= xx and rocks[y][xx-1] == '.' :
                    xx -= 1
                if x != xx :
                    rocks[y][x] = '.'
                    rocks[y][xx] = 'O' 


def slideEast(rocks) :
    for x in reversed(range(MAXX)) :
        for y in range(MAXY) :
            v = rocks[y][x]
            if v == 'O' :
                xx = x
                while xx+1 < MAXX and rocks[y][xx+1] == '.' :
                    xx += 1
                if x != xx :
                    rocks[y][x] = '.'
                    rocks[y][xx] = 'O' 


def goRound(rocks) :
    slideNorth(rocks)
    slideWest(rocks)
    slideSouth(rocks)
    slideEast(rocks)


def solve(path, part) :
    
    global MAXX, MAXY

    rocks = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            rocks.append(list(line))
    
    MAXY = len(rocks)
    MAXX = len(rocks[0])
    
    if part == 1 :        
        slideNorth(rocks)
        return weightNorth(rocks)        

    # part2 : search for a cycle
    cache = dict()
    startCycle = endCycle = -1
    rounds = 0
    while True :
        goRound(rocks)
        rounds += 1
        key = str(rocks)
        startCycle = cache.get(key)
        if startCycle is not None :
            endCycle = rounds    
            break # found a cycle
        cache[key] = rounds

    # virtually repeat cycle
    cycleLen = endCycle - startCycle
    remainingRounds = (1_000_000_000 - startCycle) % cycleLen 
    
    # do the last rounds
    for _ in range(remainingRounds) :
        goRound(rocks)

    return weightNorth(rocks) 



start_ns = time.time_ns()

print( solve('inputs/2023/14.example.txt', 1) )
print( solve('inputs/2023/14.example.txt', 2) )
print()
print( solve('inputs/2023/14.txt', 1) )
print( solve('inputs/2023/14.txt', 2) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
