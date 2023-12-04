import sys
import re

part1 = part2 = 0
numbersMap = { "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}
with open("inputs/2023/01.txt") as file :
    for line in file :
        matches = re.findall(r'[1-9]', line)
        part1 += numbersMap[matches[0]] * 10 + numbersMap[matches[-1]]
        # use capturing group inside a lookahead to get overlaps : twone => two + one, eighthree => eight + three, sevenine => seven + nine
        matches = re.findall(r'(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))', line)
        part2 += numbersMap[matches[0]] * 10 + numbersMap[matches[-1]]
print(part1)
print(part2)
