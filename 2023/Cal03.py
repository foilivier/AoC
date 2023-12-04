import sys
import re
from collections import defaultdict

part1 = part2 = 0
lines = []
maxX = maxY = 0
with open("inputs/2023/03.txt") as file :
    for l in file :
        line = l.rstrip('\n')
        lines.append(line)
        maxX = max(maxX, len(line))
        maxY += 1

gears = defaultdict(list) # id = coords of '*' / value = list(adjacent numbers)

for i in range(0, maxY) :
    line = lines[i]
    for m in re.finditer(r'[0-9]+', line) :
        start = m.start()
        end   = m.end()
        number = int(m.group())
        hasSymbol = False
        for y in range(max(0,i-1), min(maxY,i+2)) : # from i-1 included to i+1 included with bounds check
            for x in range(max(0,start - 1), min(maxX,end + 1)) :
                c = lines[y][x]
                if re.match(r'[0-9\\.]', c) : # not a symbol
                    continue
                hasSymbol = True
                if c == '*' :
                    gearId = f'{x},{y}'
                    gears[gearId].append(number) # register potential gear
        if hasSymbol :
            part1 += number
print(part1)
for gear in gears.values() :
    if len(gear) == 2 : # real gear
        part2 += gear[0] * gear[1]
print(part2)
