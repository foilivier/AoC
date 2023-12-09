import sys
import time
import re
import math
from aoc import printTime
from itertools import cycle

start_ns = time.time_ns()

dirs = None
network = {}
ghostPos = []

with open("inputs/2023/08.txt") as file :
    for l in file :
        line = l.rstrip('\n')
        if dirs is None :
            dirs = list(map(lambda x : "LR".find(x), line )) # left = 0, right = 1, used as index
        elif len(line) > 0 :
            m = re.match(r'(...) = \((...), (...)\)', line)
            key = m.group(1)
            network[key] = (m.group(2), m.group(3)) # left index 0, right index 1
            if (key[2] == 'A') :
                ghostPos.append(key)

def solve(startPos, endNodeRE) :
    count = 0
    pos = startPos
    for dir in cycle(dirs) :
        if re.match(endNodeRE, pos) :
            return count
        pos = network[pos][dir]
        count += 1

print(solve('AAA', r'ZZZ'))

# ghosts are cycling, just find the Least Common Multiple of all cycles
counts = map(lambda startPos : solve(startPos, r'..Z'), ghostPos)
print( math.lcm( *counts ) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
