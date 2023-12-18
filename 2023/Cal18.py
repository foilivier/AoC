import sys
import time
import re
from aoc import *

R,D,L,U = 0,1,2,3
MOVES = [(1,0),(0,1),(-1,0),(0,-1)]
X = 0
Y = 1

def solve(path, part) :
    
    x = y = 0
    vertices = list()
    dirs = list()
    vertices.append( [0,0] )
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            if part == 1 :
                m = re.match(r'([RDLU]) ([0-9]+) \(#[0-9a-f]+\)', line)
                dir = 'RDLU'.find(m.group(1))
                lg = int(m.group(2))
            else :
                m = re.match(r'[RDLU] [0-9]+ \(#([0-9a-f]{5})([0123])\)', line)
                dir = int(m.group(2))
                lg = int(m.group(1), 16)
            dx, dy = MOVES[dir]
            x += dx * lg
            y += dy * lg
            vertices.append( [x,y] )
            dirs.append(dir)
    
    enlargeYourPolygon(vertices, dirs)
    
    return computeSignedArea(vertices)


def enlargeYourPolygon(vertices, dirs) :

    assert( vertices[0] == vertices[-1] )
    # let last element be same (identity wise) as first
    vertices.pop()
    vertices.append(vertices[0])

    signedArea = computeSignedArea(vertices)

    # we want to turn clockwise
    # Note : normally, a signed area is positive when polygon goes counterclockwise
    #        and negative otherwise.
    #        But here our coordinates system is mirrored along the X axis so this is the opposite :
    #        positive area means the polygon is turning clockwise, and the 0.5 border
    #        is to be added to the left hand side of the oriented border
    if signedArea < 0 :
        vertices.reverse()
        dirs.reverse()
        for idx, dir in enumerate(dirs) :
            dirs[idx] = (dir + 2) % 4

    n = len(vertices)

    for idx in range(n-1) :
        dir = dirs[idx]
        vertex = vertices[idx]
        nextIdx = (idx + 1) % n
        nextVertex = vertices[nextIdx]

        # shift dimensions 0.5 toward left
        dx,dy = MOVES[dir-1] # turn LEFT is minus one in MOVES array
        vertex[X] += 0.5 * dx
        vertex[Y] += 0.5 * dy
        nextVertex[X] += 0.5 * dx
        nextVertex[Y] += 0.5 * dy
    

def computeSignedArea(vertices) :
    
    # https://en.wikipedia.org/wiki/Polygon
    # A = 1/2 SUM[i=0->i=n-1]((xi.yi+1) - (xi+1.yi)) 
    # x0,y0 = xn,yn
    # also worth reading : https://en.wikipedia.org/wiki/Pick%27s_theorem
    
    n = len(vertices) - 1
    area = 0
    for i in range(0,n) :
        xi   = vertices[i][X]
        xip1 = vertices[i+1][X]
        yi   = vertices[i][Y]
        yip1 = vertices[i+1][Y]
        area += xi * yip1 - xip1 * yi
        
    area = round(area / 2)
    
    return area



start_ns = time.time_ns()

print( solve('inputs/2023/18.example.txt', 1) ) # 62
print( solve('inputs/2023/18.example.txt', 2) ) # 952408144115
print()
print( solve('inputs/2023/18.example2.txt', 1) ) # 4
print( solve('inputs/2023/18.example2.txt', 2) ) # 121
print()
print( solve('inputs/2023/18.txt', 1) ) # 33491
print( solve('inputs/2023/18.txt', 2) ) # 87716969654406

end_ns = time.time_ns()
printTime(end_ns - start_ns)
