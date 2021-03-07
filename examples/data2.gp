#!/usr/bin/gnuplot

plot\
 "data2.dat" u 1:2 w lp pt 6 ps 1 lc 3 title "original data",\
 "data2_out.dat" u 1:2 w lp pt 7 ps 0.5 lc 7 title "auto noise level",\

pause -1

set terminal png
set output "data2.png"

replot