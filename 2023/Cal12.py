import sys
import time
import re
from functools import cache
from aoc import printTime

## Compute the number of different valid combinations given the spring && check values
@cache # It's a kind of magic
def combs(spring, checks) :

    # if spring empty, end recursion.
    # if checks says that spring should still contain faulty parts, then this combination is impossible
    if spring == "" :

        if len(checks) == 0 :
            # spring = "", checks=()
            # this combination is possible, count it (as 1, no variations possible here)
            return 1
        
        else :
            # spring = "", checks=(n...)
            # impossible, do not count
            return 0

    # if no more checks to do, end recursion
    # if spring contains faulty parts but checks says otherwise, then this combination is impossible
    if len(checks) == 0 : # nothing more to check

        if '#' in spring :
            # spring = "..#...", checks=()
            # we needed at least one defective spring, impossible, do not count
            return 0
        
        else :
            # spring = "..??..", checks=() => spring value must be "......" 
            # possible, count this solution (as 1 => no variations possible here)
            return 1
    
    # sum of all faulty parts + intervals (of 1) > length : spring not big enough, impossible, do not count
    # (1,2,3) => sum=6 + 2 intervals => spring must be at least 8
    if sum(checks) + len(checks) - 1 > len(spring) :
        return 0

    count = 0
    next = spring[0] # next char
    
    # if good part (or assume it is a good part)
    if next == '.' or next == '?' : 
        # just skip this, it does not need to be checked against faults as it is good (or supposed to be)
        # spring = ".#..??..." checks=(1,2) => combs('#..??...', (1,2)) 
        # spring = "?#..??..." checks=(1,2) => treat first ? as . and combs('#..??...', (1,2)) [alternate version spring='##..??...' checks=(1,2) will be tested later]
        count += combs(spring[1:], checks)

        
    # if faulty part (or assume it is a faulty part)
    if next == '#' or next == '?':
        
        # here the '#'is the START of a faulty part
        # can we fit a faulty part here according to the checks ?
        if '.' in spring[0:checks[0]] : 
            # found a good part indicator where it is supposed to be faulty : impossible
            # spring='#?.????" checks=(3,1)
            return count
        
        if checks[0] < len(spring) and spring[checks[0]] == "#" : 
            # found at separator position : should be a . or ? here => impossible
            # spring='#??#???" checks=(3,1)
            return count
        
        # cannot tell yet if it is impossible or not : recurse on remaining part of string (after separator) and remaining checks
        # spring='#????????" checks=(3,1,1) => must be spring='###.?????" checks=(3,1,1) => combs( '?????', (1,1) )
        count += combs(spring[checks[0] + 1:], checks[1:])

    return count


def solve(path, part2) :
    res = 0
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            spring, check = line.split(' ')
            checks = tuple([int(x) for x in check.split(',')])
            if part2 :
                spring = '?'.join((spring,) * 5)
                checks = checks * 5
            res += combs(spring, tuple(checks))
    return res

start_ns = time.time_ns()
print( solve('inputs/2023/12.example.txt', False) )
print( solve('inputs/2023/12.example.txt', True) )
print()
print( solve('inputs/2023/12.txt', False) )
print( solve('inputs/2023/12.txt', True) )
end_ns = time.time_ns()

printTime(end_ns - start_ns)
