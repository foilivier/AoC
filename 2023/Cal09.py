import sys
import time
from aoc import printTime
from itertools import pairwise
from collections import deque

start_ns = time.time_ns()


def solve(part2, line) :
    series = deque()
    values = [int(x) for x in line.split()]
    if part2 : 
        values.reverse()
    series.appendleft(values)
    while any(values) :
        values = [y-x for x,y in pairwise(values)]
        series.appendleft(values)
    
    last = 0
    for values in series :
        last = values[-1] + last
        
    return last



part1 = part2 = 0

with open("inputs/2023/09.txt") as file :
    for l in file :
        line = l.rstrip()
        part1 += solve(False, line)
        part2 += solve(True, line)

print(part1)
print(part2)


end_ns = time.time_ns()
printTime(end_ns - start_ns)
