all: data1.png data2.png data3.png

data1.dat: mk_data1
	./$< > $@
data2.dat: mk_data2
	./$< > $@
data3.dat: mk_data3
	./$< > $@

PROG=../data_filter.tcl

data1_out.dat: data1.dat $(PROG) Makefile
	$(PROG) --noise 0.1 --auto_noise 0 < $< > $@
data2_out.dat: data2.dat $(PROG) Makefile
	$(PROG) --noise 0.05  < $< > $@
#data3_out.dat: data3.dat $(PROG) Makefile
#	$(PROG) --noise 0.2 --auto_noise 0 --minn 20 < $< > $@

data3_out.dat: data3.dat $(PROG) Makefile
	$(PROG) --noise 0 --auto_noise 0 --minn 30 --maxn 30 < $< > $@

%.png: %.gp %.dat %_out.dat
	./$<

clean:
	rm -f *.dat *.png
