grep 'Maximum resident set size' test.res | awk '{print $6}' > mem.out
grep 'spins' test.res | awk '{print $4}' > spins.out
grep 'wall' test.res | awk '{print $8}' > time.out
sed -i 's/0://g' time.out
paste spins.out mem.out > memplot.out
paste spins.out time.out > timeplot.out
gnuplot

