import sys
import time
import re
from aoc import *

from collections import defaultdict


def getHash(s):
    hash = 0
    for asc in s :
        hash = (hash + ord(asc)) * 17 % 256
    return hash


def solve(path, part) :

    res = 0

    # init boxes
    boxes = [list() for _ in range(256)]
                    
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            steps = line.split(',')
            for step in steps :
                if part == 1 :
                        res += getHash(step)
                else :
                    if step[-1] == '-' :
                        # remove lens
                        label = step[:-1]
                        box = boxes[getHash(label)]
                        for idx, lens in enumerate(box) :
                            if lens[0] == label :
                                del box[idx] # delete lens if found
                                break
                    else :
                        # add lens
                        label = step[:-2]
                        focal = int(step[-1])
                        box = boxes[getHash(label)]
                        for idx, lens in enumerate(box) :
                            if lens[0] == label :
                                box[idx] = (label, focal) # replace lens if it already exists
                                break
                        else :
                            box.append( (label, focal) ) # add at end if not found

    if part == 2 :
        for ibox, box in enumerate(boxes, 1) :
            for ilens, lens in enumerate(box, 1) :
                fpower = ibox * ilens * lens[1]
                res += fpower
                
    return res

start_ns = time.time_ns()

print( solve('inputs/2023/15.example.txt', 1) )
print( solve('inputs/2023/15.example.txt', 2) )
print()
print( solve('inputs/2023/15.txt', 1) )
print( solve('inputs/2023/15.txt', 2) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
