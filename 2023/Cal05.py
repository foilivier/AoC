import sys
import re
import time

mapNames = {}
maps = {}
currentMap = None
mapName = None
seeds = None

# read data
with open("inputs/2023/05.txt") as file :
    for line in file :
        if line.strip() == "" :
            continue
        
        match = re.match(r'^((.*) map|seeds): ?(.*)$', line)
        if match :
            # header
            if match.group(1) == "seeds" :
                seeds = [int(x) for x in match.group(3).split()]
            else :
                # map
                mapName = match.group(2) 
                currentMap = list()
                maps[mapName] = currentMap
                tmp = mapName.split("-") # source-to-dest
                mapNames[tmp[0]] = tmp[2]
        else :
            # data
            data = line.split()
            currentMap.append( (int(data[1]), int(data[0]), int(data[2])) ) # tuple (source, dest, len)

def getDest(map, value) :
    for source, dest, len in map : # map is a list of tuple (yep !)
        if source <= value <= source + len - 1 :
            return dest + value - source
    return value # unmapped => unchanged

start_time = time.time()

part1 = []
for seed in seeds :
    currentValue = seed
    sourceType = "seed"
    while sourceType in mapNames :
        destType = mapNames[sourceType]
        mapName = sourceType + "-to-" + destType
        cMap = maps[mapName]
        currentValue = getDest(cMap, currentValue)
        sourceType = destType
    part1.append(currentValue)
print(min(part1))

def findMin(start, end, sourceType) :
    
    if not sourceType in mapNames :
        return start # end of recursion, return smallest (which is the start)

    destType = mapNames[sourceType]
    mapName = sourceType + "-to-" + destType
    cMap = maps[mapName]

    mins = []
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
                mins.append(findMin(getDest(cMap, current), getDest(cMap, realEnd), destType))
                current = realEnd + 1
                break;
        if not entryFound : # not mapped => get values until next range (nextMinStart-1 or end if shorter)
            mins.append(findMin(getDest(cMap, current), getDest(cMap, min(end, nextMinStart - 1)), destType))
            current = nextMinStart;

    return min(mins);

part2 = []
for idx in range(0, len(seeds), 2) :
    start = seeds[idx]
    lg = seeds[idx + 1]
    end = start + lg - 1 # inclusive
    part2.append(findMin(start, end, "seed"))
print(min(part2))

print(f"--- {(time.time() - start_time) * 1000} milliseconds ---" )
