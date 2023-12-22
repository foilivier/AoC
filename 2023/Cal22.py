import sys
import time
import re
from aoc import *

from collections import deque
from collections import defaultdict

class Brick :
    def __init__(self,id,x1,y1,z1,x2,y2,z2):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

    def __repr__(self) :
        return f'{self.id}[({self.x1},{self.y1},{self.z1})/({self.x2},{self.y2},{self.z2})]'

    def supports( self, other ):
        if self.z2 + 1 != other.z1 :
            return False # too high or too low
        if self.x2 < other.x1 or other.x2 < self.x1 :
            return False
        if self.y2 < other.y1 or other.y2 < self.y1 :
            return False
        return True


def fallingIfRemove(brick, upperBricks, lowerBricks, desintegrated) :
    falling = set()
    for upperBrick in upperBricks[brick] :
        supports = set(lowerBricks[upperBrick])
        if len(supports.difference(desintegrated)) == 0 :
            falling.add(upperBrick) # no more support => brick falls
    return falling


def countFalling(brick, upperBricks, lowerBricks) : 
    toDo = deque()
    toDo.append(brick)
    desintegrated = set()
    desintegrated.add(brick)
    while toDo :
        brick = toDo.pop()
        toFall = fallingIfRemove(brick, upperBricks, lowerBricks, desintegrated)
        for fb in toFall :
            toDo.append(fb)
            desintegrated.add(fb)
    res = len(desintegrated) - 1
    return res


def solve(path) :
    
    # read data
    bricks = list()
    with open(path) as file :
        id = 0
        for l in file :
            line = l.rstrip()
            id += 1
            x1,y1,z1,x2,y2,z2 = ints(line)
            assert x1==x2 or y1==y2 or z1==z2 # two dimensional bricks max
            assert z1 <= z2 and x1 <= x2 and y1 <= y2
            brick = Brick(id,x1,y1,z1,x2,y2,z2)
            bricks.append( brick )
    
    upperBricks = defaultdict(list) # brick -> upper bricks
    lowerBricks = defaultdict(list) # upper bricks -> bricks
    bricks.sort(key=lambda b : b.z1)
    done = set(filter(lambda b : b.z1 == 1, bricks))
    
    # make bricks fall
    highestSoFar = 0 # ground
    for brick in bricks :
        if brick in done :
            highestSoFar = max(highestSoFar, brick.z2)
            continue
        z = brick.z1
        if z > highestSoFar + 1:
            z = highestSoFar + 1 # compute a safe altitude for starting point
            brick.z1, brick.z2 = z, z + brick.z2 - brick.z1 # quick descent with no check
        underBricks = list()
        while z > 1 :
            for testedBrick in done :
                if testedBrick.supports(brick) :
                    underBricks.append(testedBrick)
            if underBricks :
                break
            z -= 1
            # make the brick fall one unit
            brick.z1 -= 1
            brick.z2 -= 1
        assert z == 1 or underBricks # on ground or on other bricks
        highestSoFar = max(highestSoFar, brick.z2)
        done.add(brick)
        # update graphs
        for under in underBricks :
            lowerBricks[brick].append(under)
            upperBricks[under].append(brick)
    
    # part1
    safeToRemove = 0
    for b in bricks :
        falls = fallingIfRemove(b, upperBricks, lowerBricks, {b})
        if len(falls) == 0 :
            safeToRemove += 1
    print( safeToRemove )
    
    # part2
    res = 0
    for b in bricks :
        res += countFalling(b, upperBricks, lowerBricks)
    print(res)



start_ns = time.time_ns()

solve('inputs/2023/22.example.txt') # 5 / 7
print()
solve('inputs/2023/22.txt') # part1 = 451  part2 = 66530


end_ns = time.time_ns()
printTime(end_ns - start_ns)
