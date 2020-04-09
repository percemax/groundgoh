#! /usr/bin/env python3

import sys
import math

if (len(sys.argv) != 2):
    print("Wrong usage, run with -h for usage", file=sys.stderr)
    exit (84)

if (str( sys.argv[1] ) == "-h"):
    print("SYNOPSIS")
    print("\t./groundhog period\n")
    print("DESCRIPTION")
    print("\tperiod        the number of days defining a period")
    exit(0)

queue = []
userInput = 0
try:
    period = int (sys.argv[1])
except ValueError:
    print("argument must be an int", file=sys.stderr)
    exit (84)

if period < 1:
    print("argument must be at least 1", file=sys.stderr)
    exit (84)

nbSwitch = 0
g = 0
r = 0
s = 0
prevr = 0
stop = 0

def display_results():
    global nbSwitch
    print("g=", end="")
    if len(queue) <= period:
        print("nan", end="\t")
    else:
        print("%.2f" %g, end="\t")
    print("r=", end="")
    if len(queue) <= period:
        print("nan", end="%\t")
    else:
        print("%.0f" %r, end="%\t")
    print("s=", end="")
    if len(queue) < period:
        print("nan", end="")
    else:
        print("%.2f" %s, end="")
    if (((prevr < 0 and r >= 0) or (prevr >= 0 and r < 0)) and prevr):
        nbSwitch += 1
        print("\ta switch occurs", end="")
    print("")

def averageIncrease():
    if len(queue) <= period:
        return 0
    global g
    g = 0
    for i in range(len(queue) - period, len(queue)):
        tmp = queue[i] - queue[i - 1]
        g += tmp if tmp > 0 else 0
    g /= period


def tempEvolution():
    if len(queue) <= period:
        return 0
    global r
    global prevr
    prevr = r
    value1 = queue[len(queue) - period - 1]
    valueNow = queue[len(queue) - 1]
    r = (valueNow - value1) / value1 * 100

def standardDeviation():
    if len(queue) < period:
        return 0
    global s
    tmp = 0
    tmp2 = 0
    for i in range(len(queue) - period, len(queue)):
        tmp += queue[i]
        tmp2 += queue[i] * queue[i]
    s = math.sqrt(tmp2 / period - (tmp / period) * (tmp / period))

while (stop == 0):
    try:
        userInput = input()
    except EOFError:
        exit(84)
    if stop == 0:
        if str(userInput) == "STOP":
            stop = 1
    if stop == 0:
        try:
            userInput = float(userInput)
            queue.append(userInput)
            averageIncrease()
            tempEvolution()
            standardDeviation()
            display_results()
        except ValueError:
            exit(84)
print("Global tendency switched", nbSwitch, "times")
exit(0)