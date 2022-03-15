# Ising Model N-Ary Tree Energy Minimizer

This is an Ising Model on N-Ary Tree Energy Minimizer. Input must be a valid N-ary tree.
It is intended for Python 3.8. There are three main components
* isingtree.py - the main executable python file for command line execution
* solver.py - contains methods for solving the ising model minimization
* gentest.py - generate valid test cases for large Ising models on N-ary trees

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

## Input file example

```
c This is an extra-hard problem
p test04 3 4
0 1 1
1 2 1
0 0 -1
1 1 -1
```

## Test Case Generator

Ising Model Tree - Test Input File Generator. This file contains a simple test generator for testing scale-up. The general execution is performed via command line.

Usage Examples:
```
./gentest.py -h
./gentest.py -n <output file>
./gentest.py -n <output file> -s <number of spins> -w <width, e.g. 4> -x <random number magnitude>
./gentest.py -n my_test_1000 -s 1000 -w 4 -x 2
```

An example of automatically generated examples and test runs
```
#!/bin/bash
#Commands to run a range of test sizes
for num in `seq 0 10000 1000000`; do
  echo "I am running $num spins" >> test.res
  ./gentest.py -n "test_$num" -s $num
  /usr/bin/time -v ./isingtree.py -i test_$num  >> test.res 2>&1
done
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
