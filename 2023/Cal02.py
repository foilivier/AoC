import sys
import re

part1 = part2 = 0
with open("inputs/2023/02.txt") as file :
    for line in file :
        res = re.match(r'Game ([0-9]+): (.*)', line)
        gameId = res.group(1)
        sets = res.group(2).split('; ')
        possible = True
        mr = mg = mb = 0
        for set in sets :
            r = g = b = 0
            for cube in set.split(', ') :
                res = re.match(r'([0-9]+) (red|green|blue)', cube)
                count = int(res.group(1))
                color = res.group(2)
                if color == 'red' :
                    r = count
                elif color == 'green' :
                    g = count
                elif color == 'blue' :
                    b = count
            if r > 12 or g > 13 or b > 14 :
                possible = False
            mr = max(r,mr)
            mg = max(g,mg)
            mb = max(b,mb)
        if possible :
            part1 += int(gameId)
        part2 += mr*mg*mb
print(part1)
print(part2)
