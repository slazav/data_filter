#!/usr/bin/gnuplot

set terminal png size 1024,512
set output "data3.png"

plot\
 "data3.dat" u 1:2 w lp pt 6 ps 1 lc 3 title "original data",\
 "data3_out.dat" u 1:2 w lp pt 7 ps 0.5 lc 7 title "filtered data",\
