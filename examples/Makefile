all: data1.png data2.png

data1.dat: mk_test_data
	./$<
data2.dat: mk_test_data2
	./$<

PROG=../data_filter

data1_out.dat: data1.dat $(PROG) Makefile
	$(PROG) --noise 0.05 < $< > $@
data2_out.dat: data2.dat $(PROG) Makefile
	$(PROG) --noise 0.2 --auto_noise 0 --maxn 100 --minn 20 < $< > $@

%.png: %.gp %.dat %_out.dat
	./$<

clean:
	rm -f *.dat *.png
