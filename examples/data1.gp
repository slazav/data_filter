#!/usr/bin/gnuplot

plot\
 "data1.dat" u 1:2 w lp pt 6 ps 0.8 title "original data",\
 "data1_skip.dat" u 1:2 w lp pt 7 ps 0.5 title "no averaging",\
 "data1_avrg.dat" u 1:2 w lp pt 7 ps 0.5 title "averaging",\
 "data1_a.dat" u 1:2 w lp pt 7 ps 0.5 title "auto noise",\

pause -1

set terminal png
set output "data1.png"

replot