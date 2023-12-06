import sys
import time

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

