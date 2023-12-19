import sys
import time
import re
from aoc import *

def solveWf(wf, xmas):
    for rule in wf :
        idx, test, value = rule 
        if idx < 0 :
            return value
        x = xmas[idx]
        if test < 0 :
            if x < -test :
                return value
        else :
            if x > test :
                return value


def accepted(workflows, xmas):
    res = 'in'
    while res != "A" and res != "R" :
        wf = workflows[res]
        res = solveWf(wf, xmas)
    return res == "A"


def solve(path) :
    res = 0
    workflows = {}
    endWF = False
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            if not line :
                endWF = True
                continue
            if endWF :
                # read & compute parts
                part = line[1:-1].split(',')
                xmas = [int(x[2:]) for x in part]
                if accepted(workflows, xmas) :
                    res += sum(xmas)
            else :
                # read rules
                m = re.match(r'([a-z]+){(.*)}', line)
                
                name = m.group(1)
                wf = list()
                workflows[name] = wf 
                for r in m.group(2).split(',') :
                    i = r.find(':')
                    if i > 0 :
                        cond = r[:i]
                        value = r[i+1:]
                        if '<' in cond :
                            test = -int(cond[2:])
                            idx = "xmas".find(cond[0:1])
                        elif '>' in cond :
                            test = int(cond[2:])
                            idx = "xmas".find(cond[0:1])
                        else :
                            assert( False)
                    else :
                        idx = -1
                        test = 0
                        value = r
                    wf.append( (idx, test, value) )
    return res


start_ns = time.time_ns()

print( solve('inputs/2023/19.example.txt') )
print( solve('inputs/2023/19.txt') )

end_ns = time.time_ns()
printTime(end_ns - start_ns)
