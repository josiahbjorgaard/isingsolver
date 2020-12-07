#!/usr/bin/env python3

"""
Generates test cases for ising solver using parameters
nspins, mwidth, xrandom
"""
import random
import argparse

def main(name, nspins, mwidth, xrandom):
    """
    generate test cases
    """
    if xrandom > mwidth:
        raise ValueError("can't have random number larger than mwidth\n")
    with open(name, 'w') as f:
        lines=list()
        m=0
        for n in range(nspins):
            width=mwidth + random.randint(-xrandom,xrandom)
            if width < 0:
                if n > 2:
                    width = 0
                else:
                    width = 1
            for m in range(m+1, m+1+width):
                if m >= nspins:
                    break
                J = random.randint(-xrandom,xrandom)
                if J == 0:
                    J = 1 if random.random() < 0.5 else -1
                lines.append("{} {} {}\n".format(n, m, J))
            if m >= nspins:
                break
        for n in range(nspins):
            h = random.randint(-xrandom,xrandom)
            if h !=0:
                lines.append("{} {} {}\n".format(n, n, h))
        nlines=len(lines)
        lines.insert(0,"p {} {} {}\n".format(name, nspins, nlines))
        lines.insert(0,"c This is a test problem: inputs are nspins={} mwidth={} xrandom={}\n".format(nspins,mwidth,xrandom))
        for line in lines:
            f.write(line)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Ising Solver Test Generator')
    parser = argparse.ArgumentParser(description = 'Generates Test Cases')
    parser.add_argument('-n','--name', dest="filename", required=True,
        help='File name / problem name for test case.', metavar="NAME")
    parser.add_argument('-s','--spins', dest="nspins", nargs='?', const=10, type=int,
        help='Number of spins to create in test file')
    parser.add_argument('-w','--width', dest="width", help='Average number of \
        children/spin-node', nargs='?', const=2, type=int)
    parser.add_argument('-x','--xfactor', help='Magnitude of random integers to \
        modify width and generate constants.', dest="xfactor",
        nargs='?', const=1, type=int)
    args = parser.parse_args()
    if args.nspins is None:
        args.nspins = 10
    if args.width is None:
        args.width = 2
    if args.xfactor is None:
        args.xfactor = 1
    main(args.filename, args.nspins, args.width, args.xfactor)
