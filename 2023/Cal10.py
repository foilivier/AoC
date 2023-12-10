import time
from aoc import printTime

start_ns = time.time_ns()

MOVEMAP = { 'S':(0,1), 'N':(0,-1), 'E':(1,0), 'W':(-1,0), }     # dir -> (dx, dy)
DIRSMAP = { ('N','F'):'E', ('N','7'):'W', ('N','|'):'N',        # (dir, symbol) -> new dir
            ('S','L'):'E', ('S','J'):'W', ('S','|'):'S',
            ('E', '7'):'S', ('E', 'J'):'N', ('E','-'):'E',
            ('W', 'F'):'S', ('W', 'L'):'N', ('W','-'):'W'
          }
RHSMAP = { 'S':(-1,0), 'N':(1,0), 'E':(0,1), 'W':(0,-1) }       # dir -> (rhs dx, rhs dy)

MAP = list()    # input data
LOOP = list()   # 'X' are part of the loop
RHSPOS = list() # 'R' are the right hand side tiles of the loop
START = None    # (x,y) starting position
MAXX = MAXY = 0 # bounds of the map


# symbol at start is hidden, find a valid start direction (there's two, we need only one)
def findStartDir(x,y) :
    # West
    if 0 <= x - 1 :
        v = MAP[y][x-1]
        if v == 'F' or v == 'L' or v == '-' :
            return 'W'
    # East
    if x + 1 < MAXX :
        v = MAP[y][x+1]
        if v == 'J' or v == '7' or v == '-' :
            return 'E'
    # North
    if 0 <= y - 1 :
        v = MAP[y-1][x]
        if v == '7' or v == 'F' or v == '|' :
            return 'N'
    # South
    if y + 1 < MAXY :
        v = MAP[y+1][x]
        if v == 'J' or v == 'L' or v == '|' :
            return 'S'
    assert( False )


def solve() :
    
    for y in range(MAXY) :              # init LOOP map
        LOOP.append(['.'] * MAXX)

    for y in range(MAXY) :               # init RHSPOS map
        RHSPOS.append(['.'] * MAXX)
    
    loopLen = 0
    x,y = START
    dir = findStartDir(x,y)
    
    while True :
        loopLen += 1
        LOOP[y][x] = 'X'        # mark as part of the loop
        
        # mark right hand side of current position (with current dir)
        rhsdx, rhsdy = RHSMAP[dir]
        rhsx = x + rhsdx
        rhsy = y + rhsdy
        if 0 <= rhsx < MAXX and 0 <= rhsy < MAXY :
            RHSPOS[rhsy][rhsx] = 'R'
        
        # move one step in current direction
        dx, dy = MOVEMAP[dir]
        x += dx
        y += dy
        
        # mark right hand side of new position (with current dir)
        rhsdx, rhsdy = RHSMAP[dir]
        rhsx = x + rhsdx
        rhsy = y + rhsdy
        if 0 <= rhsx < MAXX and 0 <= rhsy < MAXY :
            RHSPOS[rhsy][rhsx] = 'R'

        # are we at START again ?
        symb = MAP[y][x]
        if symb == 'S' :
                break
        
        # adjust new direction
        dir = DIRSMAP[dir,symb]


    part1 = loopLen // 2 # loopLen was for a full loop, max dist is halfway
        
    # part2
    # 1 : merge LOOP and RIGHT HAND SIDE maps
    # do not erase LOOP positions
    for y in range(MAXY) :
        for x in range(MAXX) :
            if LOOP[y][x] == '.' and RHSPOS[y][x] == 'R' :
                LOOP[y][x] = 'R'

    # 2 : paint it black ! (paint the outside)
    for x in range(MAXX) :
        for y in range(MAXY) :
            if LOOP[y][x] == 'R' :
                paint(x, y, 'O') # paint it OUT as OUTSIDE but could also be INSIDE, we'll take care of that later
    
    OUT = IN = 0
    for line in LOOP :
        OUT += line.count('O') # OUTSIDE positions
        IN += line.count('.') # INSIDE positions
        
    # is OUT really OUTSIDE or not ?
    inverted = False # assume we're good
    # loop the borders, this is a place where we should not find any real inside
    for y in range(MAXY) :
        for x in [0, MAXX-1] :
            if LOOP[y][x] == '.' :
                inverted = True
    for x in range(MAXX) :
        for y in [0, MAXY-1] :
            if LOOP[y][x] == '.' :
                inverted = True
    
    if inverted :    
        part2 = OUT # OUTSIDE is INSIDE
    else :
        part2 = IN # INSIDE is INSIDE

    for y in range(MAXY) :
        print( ''.join(LOOP[y]) )

    return (part1, part2)



def paint(xx, yy, color):
    todo = set()
    todo.add((xx,yy))
    
    while len(todo) > 0 :
        x,y = todo.pop()
        if (0 <= x < MAXX and 0 <= y < MAXY ) : # check ranges
            v = LOOP[y][x]
            if v == 'X' or v == color : # do not paint loop (X) aor already done
                continue
            LOOP[y][x] = color; # paint
            
            # add neighbours to todo list
            todo.add((x-1,y))
            todo.add((x+1,y))
            todo.add((x,y-1))
            todo.add((x,y+1))
    

with open("inputs/2023/10.txt") as file :
    for y, l in enumerate(file) :
        line = l.rstrip()
        MAP.append(list(line))
        x = line.find('S')
        if x >= 0 :
            START = (x, y)

MAXX = len(MAP[0])
MAXY = len(MAP)

part1, part2 = solve()
print(part1)
print(part2)

end_ns = time.time_ns()
printTime(end_ns - start_ns)
