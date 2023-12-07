import sys
import time
import re
from aoc import printTime
from itertools import combinations_with_replacement
from collections import Counter

start_ns = time.time_ns()

def getHandValue1( hand ):
   counter = Counter(hand)
   return _getHandValue(counter)

def getHandValue2( hand ):
    counter = Counter(hand)
    handValue = 0
    if 'J' in counter.keys() : # we have jokers
        jokersCount = counter.pop('J')
        for candidates in combinations_with_replacement("23456789TQKA", jokersCount) :
            c2 = counter.copy()
            c2.update( candidates )
            handValue = max( handValue, _getHandValue(c2))
    else :
        handValue = _getHandValue(counter)
    return handValue

def _getHandValue( counter ):
    handValue = 0
    vmax = max(counter.values())
    vlen = len(counter.values())
    if   vlen == 5 and vmax == 1 : # 1 + 1 + 1 + 1 + 1 => High card
        handValue = 1
    elif vlen == 1 and vmax == 5 : # 5 => Five of a kind
        handValue = 7
    elif vlen == 2 and vmax == 4 : # 4 + 1 => Four of a kind
        handValue = 6
    elif vlen == 2 and vmax == 3 : # 3 + 2 => Full house
        handValue = 5
    elif vlen == 3 and vmax == 3 : # 3 + 1 + 1 => Three of a kind
        handValue = 4
    elif vlen == 3 and vmax == 2 : # 2 + 2 + 1 => Two pairs 
        handValue = 3
    elif vlen == 4 and vmax == 2 : # 2 + 1 + 1 + 1 => One pair 
        handValue = 2
    return handValue

def getSortKey1(hand):
    value = getHandValue1(hand)
    hand_comparable = hand.translate(str.maketrans("TJQKA","ABCDE"))
    return f"{value}-{hand_comparable}"

def getSortKey2(hand):
    value = getHandValue2(hand)
    hand_comparable = hand.translate(str.maketrans("TJQKA","A0CDE"))
    return f"{value}-{hand_comparable}"

def solve(games):
    score = 0
    games.sort()
    for idx, tuple in enumerate(games) :
        rank = idx + 1
        bid = tuple[2]
        score += rank * bid
    return score

games1 = []
games2 = []
with open("inputs/2023/07.txt") as file :
    for line in file :
        m = re.match(r'([2-9TJQKA]+) ([0-9]+)', line)
        hand = m.group(1)
        bid = int(m.group(2))
        games1.append( ( getSortKey1(hand), hand, bid ) ) # put sort key in first place so that we do not need a sort function
        games2.append( ( getSortKey2(hand), hand, bid ) )

print( solve(games1) )        
print( solve(games2) )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
