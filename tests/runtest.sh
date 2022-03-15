#!/bin/bash
#Commands to run a range of test sizes
for num in `seq 0 10000 1000000`; do
  echo "I am running $num spins" >> test.res
  ./gentest.py -n "test_$num" -s $num
  /usr/bin/time -v ./solver.py -i test_$num  >> test.res 2>&1
done
