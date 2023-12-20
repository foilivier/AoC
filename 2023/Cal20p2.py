import sys
import time
import re
from aoc import *

from collections import deque
from collections import defaultdict
from operator import itemgetter

INPUTS = '_inputs'

def pushButton(network, types, states, pushCount, rxInputs, rxCycles ) :
 
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
            if mod in rxInputs :
                idx = rxInputs.index(mod)
                cycle = rxCycles[idx]
                cycle.append(pushCount)
        
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
     
    # rx receives its inputs from conjonction(s) modules
    # in my input :
    #      rx <- &qb <- [ &kv, &jg, &rz, &mr ]
    # so find all these inputs (and check that they are all conjonctions [is that really mandatory?])
    # conjonctions send low pulse when all inputs are high 
    #   => if they cycle then final conjonction will send low pulse to rx when all cycles aligns (=> LCM)
    rxInputs = ['rx']
    while len(rxInputs) == 1 :
        mod = rxInputs[0]
        rxInputs = network[mod + INPUTS]
        assert all(map(lambda x : types[x] == '&', rxInputs))
    rxCycles = [list() for _ in rxInputs]

    c = 0
    while True :
        c += 1
        pushButton(network, types, states, c, rxInputs, rxCycles)
        if all(rxCycles) : # find a cycle for all conjonction inputs
            return math.lcm(*map(itemgetter(0), rxCycles))
        # if all(map(lambda x : len(x) >= 100, rxCycles)) :
        #     for cycle in rxCycles :
        #         print( '\t'.join(map(str, cycle)) )
        #     print()
        #     return math.lcm(*list(map(lambda x : x[0], rxCycles)))
    


start_ns = time.time_ns()

print( solve('inputs/2023/20.txt') ) # 238420328103151
# print( solve('inputs/2023/20.example3.txt') ) # 236095992539963 R.Goulais

end_ns = time.time_ns()
printTime(end_ns - start_ns)
