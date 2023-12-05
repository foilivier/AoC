import sys
import re

mapNames = {}
maps = {}
currentMap = None
currentSection = None
seeds = None

# read data
with open("inputs/2023/05.txt") as file :
    for lg in file :
        line = lg.rstrip('\n')
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

def getDest(map, value) :
    for source, dest, len in map :
        if source <= value <= source + len - 1 :
            return dest + value - source
    return value # unmapped => unchanged

part1 = sys.maxsize
for seed in seeds :
    currentSeed = seed
    source = "seed"
    while source in mapNames :
        dest = mapNames[source]
        mapName = source + "-to-" + dest
        cMap = maps[mapName]
        currentSeed = getDest(cMap, currentSeed)
        source = dest
    part1 = min(part1, currentSeed)

print(part1)

def findMin(start, end, source) :
    
    if not source in mapNames :
        return start # end of recursion, return smallest (which is the start)

    dest = mapNames[source]
    mapName = source + "-to-" + dest
    cMap = maps[mapName]

    bestMin = sys.maxsize
    current = start
    while current <= end : # cover full range from start to end
        entryFound = False
        nextMinStart = sys.maxsize
        for eSource, eDest, eLen in cMap :
            eEnd = eSource + eLen - 1
            if eSource > current :
                nextMinStart = min(nextMinStart, eSource) # find next range with minimum start

            if eSource <= current <= eEnd :
                entryFound = True # this part of range is mapped
                realEnd = min(end, eEnd) # mapped till the end or not ?
                bestMin = min(bestMin, findMin(getDest(cMap, current), getDest(cMap, realEnd), dest))
                current = realEnd + 1
                break;
        if not entryFound : # not mapped => get values until next range (nextMinStart)
            bestMin = min(bestMin, findMin(getDest(cMap, current), getDest(cMap, min(end, nextMinStart - 1)), dest))
            current = nextMinStart;

    return bestMin;

part2 = sys.maxsize
for idx in range(0, len(seeds), 2) :
    start = seeds[idx]
    lg = seeds[idx + 1]
    end = start + lg - 1 # inclusive
    part2 = min(part2, findMin(start, end, "seed"))
print(part2)
