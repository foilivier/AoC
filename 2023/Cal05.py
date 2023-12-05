import sys
import re
from collections import defaultdict

def getDest(map, value) :
    for (source, dest, len) in map :
        if source <= value <= source + len - 1 :
            return dest + value - source
    return value

def findMin(start, end, source) :
    
    if not source in mapNames :
        return start
    dest = mapNames[source]
    mapName = source + "-to-" + dest
    cMap = maps[mapName]

    bestMin = sys.maxsize
    current = start
    while current <= end :
        entryFound = False
        nextMinStart = sys.maxsize
        for eSource, eDest, eLen in cMap :
            eEnd = eSource + eLen - 1
            if eSource > current :
                nextMinStart = min(nextMinStart, eSource)

            if eSource <= current <= eEnd :
                entryFound = True
                if eEnd >= end :
                    bestMin = min(bestMin, findMin(getDest(cMap, current), getDest(cMap, end), dest))
                    current = end + 1
                else :
                    bestMin = min(bestMin, findMin(getDest(cMap, current), getDest(cMap, eEnd), dest))
                    current = eEnd + 1
                break;
        if not entryFound :
            bestMin = min(bestMin, findMin(getDest(cMap, current), getDest(cMap, min(end, nextMinStart - 1)), dest))
            current = nextMinStart;

    return bestMin;



mapNames = {}
maps = {}
currentMap = None
currentSection = None
seeds = None

with open("inputs/2023/05.txt") as file :
    for l in file :
        line = l.rstrip('\n')
        if line.strip() == "" :
            continue
        
        match = re.match(r'^(.*?)( map)?: ?(.*)$', line)
        if match :
            # header
            currentSection = match.group(1)
            if currentSection == "seeds" :
                seeds = [int(x) for x in match.group(3).split()]
            else :
                # map
                currentMap = list()
                maps[currentSection] = currentMap
                tmp = currentSection.split("-")
                mapNames[tmp[0]] = tmp[2]
        else :
            # data
            d = line.split()
            currentMap.append( (int(d[1]), int(d[0]), int(d[2])) ) # source, dest, len


part1 = sys.maxsize
for seed in seeds :
    currentValue = seed
    source = "seed"
    while source in mapNames :
        dest = mapNames[source]
        mapName = source + "-to-" + dest
        cMap = maps[mapName]
        currentValue = getDest(cMap, currentValue)
        source = dest
    part1 = min(part1, currentValue)

print(part1)

part2 = sys.maxsize
for i in range(0, len(seeds), 2) :
    start = seeds[i]
    len = seeds[i + 1]
    part2 = min(part2, findMin(start, start + len - 1, "seed"))
print(part2)
