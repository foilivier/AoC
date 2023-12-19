import sys
import time
import re
from aoc import *
from copy import deepcopy

# xmas = [ (xlo,xhi), (mlo,mhi), (alo,ahi), (slo,shi) ]
def count(workflows, wf, xmas ) :
    
    if wf == 'R' :
        return 0 # rejected, does not count
 
    if wf == 'A' :
        # accepted for x * m * a * s combinations
        res = 1
        for rg in xmas :
            res *= rg[1] - rg[0] + 1
        return res

    res = 0
    wf = workflows[wf]
    for rule in wf :
        idx, test, value = rule 
        if idx < 0 : # found result of a rule
             return res + count(workflows, value, xmas)
            
        rg_start, rg_end = xmas[idx]
        if test < 0 :
            test = -test
            # xmas[idx] < test
            lower_rg = ( rg_start, min(rg_end, test-1) )
            if lower_rg[0] <= lower_rg[1] :
                nxmas = deepcopy(xmas)
                nxmas[idx] = lower_rg
                res += count(workflows, value, nxmas) # count this rule with low range
            higher_range = ( max(rg_start,test), rg_end )
            if higher_range[0] <= higher_range[1] :
                xmas[idx] = higher_range # high range will be tested by next rule
        else :
            # xmas[idx] > test
            lower_rg = ( rg_start, min(rg_end, test) )
            higher_range = ( max(rg_start,test+1), rg_end )
            if higher_range[0] <= higher_range[1] :
                nxmas = deepcopy(xmas)
                nxmas[idx] = higher_range
                res += count(workflows, value, nxmas) # count this rule with high range
            xmas[idx] = lower_rg # other range will be tested by next rule
    return res


def solve(path) :
    workflows = {}
    with open(path) as file :
        for l in file :
            line = l.rstrip()
            if not line :
                break
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
                    idx = -1
                    test = 0
                    value = r
                wf.append( (idx, test, value) )
    
    return count(workflows, 'in', [(1,4000), (1,4000), (1,4000), (1,4000)] )


start_ns = time.time_ns()

print( solve('inputs/2023/19.example.txt') )
print( solve('inputs/2023/19.txt') )

end_ns = time.time_ns()
printTime(end_ns - start_ns)

