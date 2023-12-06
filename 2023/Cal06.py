import sys

# Time:        41     77     70     96
# Distance:   249   1362   1127   1011

data = { 41 : 249, 77 : 1362, 70 : 1127, 96 : 1011 }

def findRec(time, record) :
    wins = 0
    for t in range(0, time) :
        if (time - t) * t > record : 
            wins += 1
    return wins

part1 = 1
for t, r in data.items() :
    part1 *= findRec(t, r)
print(part1)

print( findRec(41777096, 249136211271011) )
