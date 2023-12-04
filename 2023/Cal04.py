import sys
import re

part1 = part2 = 0

wins = {} # register cardId -> wins
with open("inputs/2023/04.txt") as file :
    for line in file :
        res = re.match(r'Card +([0-9]+): (.*)\|(.*)', line)
        scratchId = int(res.group(1))
        winningNumbers = [int(x) for x in res.group(2).split()]
        myNumbers = [int(x) for x in res.group(3).split()]
        winCount = len(set(winningNumbers) & set(myNumbers))
        wins[scratchId] = winCount
        if winCount > 0 :
            part1 += pow(2, winCount - 1)
print(part1)

mycards = {} # cardId => cardCount of cards owned
for c in range(1, len(wins) + 1) :
    mycards[c] = 1 # starting with one card of each

for c in range(1, len(wins) + 1) :
    winCount = wins[c]
    cardCount = mycards[c]
    for i in range(c + 1, c + 1 + winCount) :
        # winning these cards cardCount times
        mycards[i] += cardCount

part2 = sum(mycards.values())
print(part2)
