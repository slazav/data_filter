#!/usr/bin/gnuplot

set title "filter\\_data --maxd 0.05 --maxn 100"

plot\
 "data1.dat" u 1:2 w p pt 6 ps 1 lc 3 title "original data",\
 "data1_out.dat" u 1:2 w lp pt 7 lc 7 ps 0.5 title "filtered data",\

pause -1

set terminal png size 1024,512 noenhanced
set output "data1.png"

replot