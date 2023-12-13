import sys
import time
from aoc import printTime


def findSymetry(cols, left, right) :
    
    l = left
    r = right
    
    while l >= 0 and r < len(cols) :
        if cols[l] != cols[r] :
            return -1
        l -= 1
        r += 1
    return left + 1


def findReflectionBF(pattern) :
    
    # Brute Force for the win
    oldSym = findReflection(pattern, -1)
    
    for y in range(len(pattern)) :
        old = pattern[y]
        for x in range(len(old)) :
            repl = list(old)
            v = repl[x]
            newv = '.' if v == '#' else '.'
            repl[x] = newv
            pattern[y] = ''.join(repl)
            res = findReflection(pattern, oldSym)
            pattern[y] = old
            if res > 0 :
                return res
    return -1


def findReflection(pattern, oldSym) :

    rows = list()
    cols = list()
    vert = [''] * len(pattern[0])
    
    res = 0
    
    for line in pattern : 
        rows.append(int(line.replace('.', '0').replace('#', '1'), 2))
        for idx, c in enumerate(line) :
            vert[idx] += c
    for line in vert :
        cols.append(int(line.replace('.', '0').replace('#', '1'), 2))
    
    count = 0
    
    # test cols
    for i in range(len(cols) - 1) :
        if cols[i] == cols[i+1] :
            left = findSymetry(cols, i, i+1)
            if left > 0 and left != oldSym :
                return left
    
    # test rows
    for i in range(len(rows) - 1) :
        if rows[i] == rows[i+1] :
            above = findSymetry(rows, i, i+1)
            if above > 0 and above * 100 != oldSym :
                return above * 100
            
    return res   


def solve(path, part) :
    res = 0
    pattern = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            if line :
                pattern.append(line)
            else :
                if part == 1 :
                    res += findReflection(pattern, -1)
                else :
                    res += findReflectionBF(pattern)
                pattern = list() # reset

    # do not forget last pattern ...
    if part == 1 :
        res += findReflection(pattern, -1)
    else :
        res += findReflectionBF(pattern)

    return res


start_ns = time.time_ns()


print( solve('inputs/2023/13.example.txt', 1) )
print( solve('inputs/2023/13.example.txt', 2) )

print( solve('inputs/2023/13.txt', 1) )
print( solve('inputs/2023/13.txt', 2) )


end_ns = time.time_ns()
printTime(end_ns - start_ns)
