#!/usr/bin/gnuplot

plot\
 "data2.dat" u 1:2 w lp pt 6 ps 0.8 title "original data",\
 "data2_skip.dat" u 1:2 w lp pt 7 ps 0.5 title "no averaging",\
 "data2_avrg.dat" u 1:2 w lp pt 7 ps 0.5 title "averaging",\
 "data2_a.dat" u 1:2 w lp pt 7 ps 0.5 title "auto noise level",\

pause -1

set terminal png
set output "data2.png"

replot