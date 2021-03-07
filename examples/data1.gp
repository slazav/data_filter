#!/usr/bin/gnuplot

plot\
 "data1.dat" u 1:2 w lp pt 6 ps 0.8 title "original data",\
 "data1_out.dat" u 1:2 w lp pt 7 ps 0.5 title "auto noise",\

pause -1

set terminal png
set output "data1.png"

replot