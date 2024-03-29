# Ising Model N-Ary Tree Energy Minimizer

This is an Ising Model on N-Ary Tree Energy Minimizer. It functions as a command line tool and is intended for testing scalability of the minimization algorithm. Input must be a valid N-ary tree and as specified below.
It is built for use with Python 3.7 or greater.
There are three main components
* isingtree.py - the main executable file for command line execution
* solver.py - contains methods for solving the ising model minimization
* gentree.py - generate valid trees for large Ising models on N-ary trees

# Install/Usage
The only non-standard module required is argparse. Install using
`pip3 install -r requirements.txt`

Usage Examples:
```
./isingtree.py -h
./isingtree.py -i <input file>
./isingtree.py -i <input file> -r <node to make root> --verbose
./isingtree.py -i my_test_1000 -r 29 --verbose
```

## Input File Structure
* each line defines a weight for a coefficient, structured like `i j w` where `i,j < N_S` are the indices and `w` are the weights

## Input file example

```
#Example
#h
0 0 -1
1 1 -1
#J Couplings
0 1 1
1 2 1
```

## Input Generator

Ising Model Tree Input File Generator. This file contains a simple random input file generator for testing scale-up. The general execution is performed via command line.

Usage Examples:
```
./gentest.py -h
./gentest.py -n <output file>
./gentest.py -n <output file> -s <number of spins> -w <width, e.g. 4> -x <random number magnitude>
./gentest.py -n my_test_1000 -s 1000 -w 4 -x 2
```

An example of automatically generated examples and testing scalability
```
#!/bin/bash
#Commands to run a range of test sizes
for num in `seq 0 10000 1000000`; do
  echo "I am running $num spins" >> test.res
  ./gentest.py -n "test_$num" -s $num
  /usr/bin/time -v ./isingtree.py -i test_$num  >> test.res 2>&1
done
```

## Help Output
```
usage: isingtree.py [-h] -i PATHTOINPUTFILE [-r [ROOTNODE]] [-v]

Solves the ground state configuration for Ising Model on an N-ary Tree

optional arguments:
  -h, --help            show this help message and exit
  -i PATHTOINPUTFILE, --input PATHTOINPUTFILE
                        Input File Path, input file has specific format
                        requirements. See README.md for examples.
  -r [ROOTNODE], --root [ROOTNODE]
                        Specify node number to use as root node, must be less
                        than total number of nodes
  -v, --verbose         Enable verbose logging
```
## Unit Test

Install pytest `pip3 install -r requirements-dev.txt`.
Run unit tests using
```
python3 -m pytest tests.py
======================================== test session starts ========================================
platform linux -- Python 3.8.5, pytest-4.6.9, py-1.8.1, pluggy-0.13.0
rootdir: /home/josiah/Projects/myrepos/dwave
collected 6 items                                                                                   

tests.py ......                                                                               [100%]

===================================== 6 passed in 0.07 seconds ======================================
```
