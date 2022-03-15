#!/usr/bin/env python3

"""
Ising Model N-Ary Tree Energy Minimizer

This file contains the main execution point and helper functions for
loading and preparing input data.
The general execution is performed via command line

Usage Examples:
    ./isingtree.py -h
    ./isingtree.py -i <input file>
    ./isingtree.py -i <input file> -r <node to make root> --verbose
    ./isingtree.py -i my_test_1000 -r 29 --verbose
"""

from solver import Data, Node
import argparse
import logging
import sys

def loadinput(inputfilepath):
    """
    Checks input format and converts to dictionary objects
    Input - inputfilepath - string that has relative path to input file
    Output - hdict: dictionary of h referenced by node id
            Jdict: dictionary of J referenced by node id 1, node id 2
    """
    inputfilepath=str(inputfilepath)
    logging.info("Loading input from " + inputfilepath)
    with open(inputfilepath, "r") as f:
        lines = [line.rstrip() for line in f.readlines()
                    if not line.startswith('c')]
    if len(lines) < 1:
        raise InputError(lines, "Less than 1 non-comment line read from input")
    pline = lines.pop(0).split()
    if pline[0] != 'p':
        raise InputError(pline, "First non-comment line does \
                                    not start with \'p\'")
    elif len(pline) != 4:
        raise InputError(pline, "Fist non-comment line does not have 4 \
                                    elements separated by white space")
    try:
        pname=str(pline[1])
    except ValueError as err:
        logging.error("Problem name not able to read as string")
        logging.error(err.args)
    try:
        nnodes=int(pline[2])
    except ValueError as err:
        logging.error("Number of nodes not able to read as integer")
        logging.error(err.args)
    try:
        nedges=int(pline[3])
    except ValueError as err:
        logging.error("Number of edges not able to read as integer")
        logging.error(err.args)
    if len(lines) != nedges:
        raise InputError(nedges, "Number of input lines does not equal \
                                specified number of edges")
    data = Data(pname, nnodes, nedges)
    logging.info("Loaded problem line for name: {}, nnodes: {}, \
                    nedges {}".format(pname, nnodes, nedges))

    # First item from input
    startNode = lines[0][0]

    # Gather all h, J values
    # TODO: Don't put zeros here
    nodes=dict(zip(range(0, nnodes), [0] * nnodes))
    edges={}

    for nline, line in enumerate(lines):
        lsplit = [int(i) for i in line.split()]

        logging.info("Reading line {} : {}".format(nline, line))
        if len(lsplit) != 3:
            raise InputError(line, "Input line {} does not have 3 entries \
                                    separated by white space".format(nline))

        # TODO: elif all integers
        # TODO: elif the node number>nnodes
        if lsplit[0] == lsplit[1]:
            # TODO: Check this isn't a repeat entry
            nodes[lsplit[0]] = lsplit[2]
        else:
            # add mirrored dicts
            if lsplit[0] in edges.keys():
                edges[lsplit[0]][lsplit[1]] = lsplit[2]
            else:
                edges[lsplit[0]] = {lsplit[1]: lsplit[2]}
            if lsplit[1] in edges.keys():
                edges[lsplit[1]][lsplit[0]] = lsplit[2]
            else:
                edges[lsplit[1]] = {lsplit[0]: lsplit[2]}

    return nodes, edges

class Error(Exception):
    """Base class for exceptions."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def main(filename, n=0):
    """
    Main function for Ising Model Tree Energy Minimizer
    Functionally works according to
        1.) load input, check format
        2.) choose/create root node
        3.) discover child nodes and create tree
        4.) calculate minimum energies and spins for each sub-tree,
                traversing up from leaf nodes
        5.) calculate minimum energy and spin, walking down from root node
        6.) print results to stdout
    """
    nodes, edges = loadinput(filename)
    if n > len(nodes)-1:
        raise ValueError("n must be less than number of nodes - 1")
    root = Node(n)
    root.discover_children(nodes, edges)
    root.calculate_esmins(nodes, edges)
    spindict={}
    res=root.set_minE_spin(spindict)
    print(res)
    spinstr=str()
    for n in range(len(spindict)):
        spin = spindict[n]
        if spin == -1:
            spinstr += '-'
        elif spin == 1:
            spinstr += '+'
        else:
            spinstr += '?'
    print(spinstr)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Ising Model Tree Solver')
    parser = argparse.ArgumentParser(description = 'Solves the ground state \
        configuration for Ising Model on an N-ary Tree')
    parser.add_argument('-i','--input', dest="filename", type=str, required=True,
        help='Input File Path, input file has specific format requirements. \
            See README.md for examples.', metavar="PATHTOINPUTFILE")
    parser.add_argument('-r','--root', dest="rootnode", nargs='?', const=1,
        type=int, help='Specify node number to use as root node, must be less \
            than total number of nodes')
    parser.add_argument('-v','--verbose', help='Enable verbose logging',
        action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if args.rootnode is None:
        args.rootnode = 0
    main(args.filename, args.rootnode)
