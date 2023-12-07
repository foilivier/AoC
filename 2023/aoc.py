import sys
import time
import math

def printTime(t_ns: int) -> None :
    if t_ns < 10_000 :
        print(f"--- {t_ns} nanoseconds ---" )
    else :
        t_us = int(t_ns / 1_000)
        if t_us < 10_000 :
            print(f"--- {t_us} microseconds ---" )
        else :
            t_ms = int(t_ns / 1_000_000)
            if t_ms < 10_000 :
                print(f"--- {t_ms} milliseconds ---" )
            else :
                t_sec = int(t_ns / 1_000_000_000)
                print(f"--- {t_sec} seconds ---" )


def solve2DegreeEquation(a: float, b: float, c: float) :
    delta = (b * b) - (4.0 * a * c)
    rdelta = math.sqrt(delta)
    solutions = []
    if delta == 0 :
        solutions.append( -b / ( 2.0 * a) )
    elif delta > 0 :
        solutions.append( (-b - rdelta) / ( 2.0 * a) )
        solutions.append( (-b + rdelta) / ( 2.0 * a) )
    return solutions