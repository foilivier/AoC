import sys
import time
from aoc import *
from itertools import combinations
from numpy import *
import sympy as sym

def solve2(hs1,hs2,hs3):
    
    x1,y1,z1,a1,b1,c1 = hs1
    x2,y2,z2,a2,b2,c2 = hs2
    x3,y3,z3,a3,b3,c3 = hs3
    
    # x = a*t + x0
    # y = b*t + y0
    # z = c*t + z0
    #
    # stone :
    # xs = as*t + xs0
    # ys = bs*t + ys0
    # zs = cs*t + zs0
    #
    # each hailstone needs to intersect the stone trajectory
    # (but not necessarily at the same time)
    # hs1 :
    # x = a1*t + x1
    # y = b1*t + y1
    # z = c1*t + z1
    # hs2 :
    # x = a2*t + x2
    # y = b2*t + y2
    # z = c2*t + z2
    # hs3 :
    # x = a3*t + x3
    # y = b3*t + y3
    # z = c3*t + z3
    #
    # Collision 1 (t1, xt1, yt1, zt1) avec hs1
    # xt1 = as*t1 + xs0
    # xt1 = a1*t1 + x1
    # yt1 = bs*t1 + ys0
    # yt1 = b1*t1 + y1
    # zt1 = cs*t1 + zs0
    # zt1 = c1*t1 + z1
    # Collision 2 (t2, xt2, yt2, zt2) avec hs2
    # xt2 = as*t2 + xs0
    # xt2 = a2*t2 + x2
    # yt2 = bs*t2 + ys0
    # yt2 = b2*t2 + y2
    # zt2 = cs*t2 + zs0
    # zt2 = c2*t2 + z2
    # Collision 1 (t3, xt3, yt3, zt3) avec d3
    # xt3 = as*t3 + xs0
    # xt3 = a3*t3 + x3
    # yt3 = bs*t3 + ys0
    # yt3 = b3*t3 + y3
    # zt3 = cs*t3 + zs0
    # zt3 = c3*t3 + z3
    
    syms = sym.symbols('t1,t2,t3,aas,bs,cs,xs0,ys0,zs0')
    t1,t2,t3,aas,bs,cs,xs0,ys0,zs0 = syms
    eqs = list()
    eqs.append( sym.Eq(a1*t1 + x1, aas*t1 + xs0) )
    eqs.append( sym.Eq(b1*t1 + y1, bs*t1 + ys0 ) )
    eqs.append( sym.Eq(c1*t1 + z1, cs*t1 + zs0 ) )
    eqs.append( sym.Eq(a2*t2 + x2, aas*t2 + xs0) )
    eqs.append( sym.Eq(b2*t2 + y2, bs*t2 + ys0 ) )
    eqs.append( sym.Eq(c2*t2 + z2, cs*t2 + zs0 ) )
    eqs.append( sym.Eq(a3*t3 + x3, aas*t3 + xs0) )
    eqs.append( sym.Eq(b3*t3 + y3, bs*t3 + ys0 ) )
    eqs.append( sym.Eq(c3*t3 + z3, cs*t3 + zs0 ) )
    result = sym.solve(eqs, syms)
    
    res = 0
    for idx,s in enumerate(syms) :
        if s.name in ['xs0', 'ys0', 'zs0'] :
            res += result[0][idx]
    return res


def intersect(d1,d2,MIN,MAX):
    
    x1,y1,_,a1,b1,_ = d1
    x2,y2,_,a2,b2,_ = d2

    # x = at + x0
    # y = bt + y0
    #
    # x = a1t + x1
    # y = b1t + y1
    #
    # x = a2t' + x2
    # y = b2t' + y2
    # 
    # a1*t1 + x1 = a2*t2 + x2
    # b1*t1 + y1 = b2*t2 + y2
    #
    # a1*t1 - a2*t2 = x2 - x1
    # b1*t1 - b2*t2 = y2 - y1
    #
    # pas de 0 dans le jeu de test
    
    
    A=matrix([[a1,-a2],[b1,-b2]])
    B=matrix([[x2-x1],[y2-y1]])
    if linalg.det(A) == 0 :
        # parallel, no intersection
        return 0
    solution=linalg.solve(A,B)
    t1 = solution[0,0]
    t2 = solution[1,0]
    
    x = a1 * t1 + x1
    y = b1 * t1 + y1
    x2 = a2 * t2 + x2
    y2 = b2 * t2 + y2
    assert isclose(x,x2)
    assert isclose(y,y2)
    # compute t with x = x0 + at
    if t1 < 0 or t2 < 0 :
        return 0
         
    return int(MIN <= x <= MAX and MIN <= y <= MAX)

    
def solve(path, part, MIN, MAX) :
    trajs = list()
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            x,y,z,dx,dy,dz = ints(line)
            trajs.append(  (x,y,z,dx,dy,dz) )

    res = 0
    if part == 1 :    
        for d1,d2 in combinations(trajs,2) :
            if d1 != d2 :
                res += intersect(d1, d2, MIN, MAX)
                
    if part == 2 :
        res = solve2(trajs[0],trajs[1],trajs[2])

    return res


start_ns = time.time_ns()

print( solve('inputs/2023/24.example.txt', 1, 7, 27) )
print( solve('inputs/2023/24.example.txt', 2, 0, 0) )
print()
print( solve('inputs/2023/24.txt', 1, 200000000000000, 400000000000000) ) # 12783
print( solve('inputs/2023/24.txt', 2, 0, 0) ) # 948485822969419


end_ns = time.time_ns()
printTime(end_ns - start_ns)
