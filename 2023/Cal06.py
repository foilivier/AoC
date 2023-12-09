import sys
import time
import math
from aoc import printTime
from aoc import solve2DegreeEquation

# Time:        41     77     70     96
# Distance:   249   1362   1127   1011

data = { 41 : 249, 77 : 1362, 70 : 1127, 96 : 1011 }

def findRec(time, record) :
    wins = 0
    for t in range(0, time) :
        if (time - t) * t > record : 
            wins += 1
    return wins

def findRecOptimized(time, record) :
    best = int(time / 2) # best I can do
    wleft = findLowestLeftWin(0, best, time, record)
    wright = findBiggestRightWin(best, time, time, record)
    return wright - wleft + 1

def findLowestLeftWin(tmin, tmax, time, record) :
    # tmin loses
    # tmax wins
    while tmin + 1 < tmax :
        tmiddle = int((tmin + tmax) / 2)
        if (time - tmiddle) * tmiddle > record :
            tmax = tmiddle
        else :
            tmin = tmiddle
    return tmax

def findBiggestRightWin(tmin, tmax, time, record) :
    # tmin wins
    # tmax loses
    while tmin + 1 < tmax :
        tmiddle = int((tmin + tmax) / 2)
        if (time - tmiddle) * tmiddle > record :
            tmin = tmiddle
        else :
            tmax = tmiddle
    return tmin

def findRecOptimized2(time, record) :
    # equation to solve : -x*x + Tx - R = 0
    # a = -1 b = T c = -R
    
    low, high = solve2DegreeEquation( -1, time, -record )
    if high < low : 
        low, high = high, low
    low =  math.ceil(low)
    high =  math.floor(high)
     
    return high - low + 1

part1 = 1
for t, r in data.items() :
    part1 *= findRec(t, r)
print(part1)

start_time = time.time_ns()
print( findRecOptimized(41777096, 249136211271011) )
printTime(time.time_ns() - start_time)

start_time = time.time_ns()
print( findRecOptimized2(41777096, 249136211271011) )
printTime(time.time_ns() - start_time)

start_time = time.time_ns()
print( findRec(41777096, 249136211271011) )
printTime(time.time_ns() - start_time)

