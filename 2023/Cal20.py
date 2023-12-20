import sys
import time
import re
from aoc import *

from collections import deque
from collections import defaultdict

INPUTS = '_inputs'

def pushButton(network, types, states) :
 
    hi = lo = 0   
    queue = deque()
    queue.append( (0, 'broadcaster', 'button') )
    
    while queue :
        pulse, mod, fromMod = queue.popleft()
        type = types[mod]
        if type == 0 :
            type, state = None, 0
        else :
            state = states[mod]
        outs = network[mod]
        
        # print( f'{fromMod} -{pulse}-> {mod}')
        if pulse == 0 :
            lo += 1
        else :
            hi += 1
        
        if type == 'b' :
            for out in outs :
                queue.append( (pulse, out, mod) )
        elif type == '&' :
            newState = state
            ins = network[mod + INPUTS]
            idxIn = ins.index(fromMod)
            modMask = 0
            if len(ins) > 0 :
                modMask = 1 << idxIn
            else :
                pass # no input
            allHighState = pow(2,len(ins)) - 1
            if pulse == 0 :
                newState &= ~modMask;
            else :
                newState |= modMask;
            states[mod] = newState
            if newState == allHighState :
                outPulse = 0
            else :
                outPulse = 1
            for out in outs :
                queue.append( (outPulse, out, mod) )
        elif type == '%' : 
            if pulse == 0 :
                newState = (state + 1) % 2
                outPulse = newState
                states[mod] = newState
                for out in outs :
                    queue.append( (outPulse, out, mod) )
            else :
                pass # ignore high pulse
        else :
            # unknown module => test module => do nothing
            pass
            
    return (hi, lo)


def solve(path) :
    
    network = defaultdict(list) # module_name -> [ outs ] / module_name_inputs -> [ ins ]
    states = defaultdict(int)   # module_name -> state
    types = defaultdict(int)    # module_name -> type (0, '#', 'b', '&' ) # unknown (end transmission), flip-flop, broadcast, conjonction

    with open(path) as file :
        for l in file :
            line = l.rstrip()
            left, right = line.split( ' -> ' )
            outMods = right.split( ', ')
            if left == 'broadcaster' :
                name = left
                type = 'b'
            else :
                type, name = left[:1], left[1:]
            types[name] = type
            
            for out in outMods :
                network[name].append(out)
                network[out + INPUTS].append(name)
    
    hiCount = loCount = 0
    for _ in range(1000) :
        lo, hi = pushButton(network, types, states)
        hiCount += hi
        loCount += lo

    return hiCount * loCount



start_ns = time.time_ns()

print( solve('inputs/2023/20.example.txt') ) #32000000
print( solve('inputs/2023/20.example2.txt') ) # 11687500
print()
print( solve('inputs/2023/20.txt') ) # 898557000


end_ns = time.time_ns()
printTime(end_ns - start_ns)
