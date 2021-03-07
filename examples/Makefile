all: data1_out.dat data2_out.dat

data1.dat: mk_test_data
	./$<
data2.dat: mk_test_data2
	./$<

PROG=../data_filter

data1_out.dat: data1.dat $(PROG) Makefile
	$(PROG) --noise 0.05 --maxn 150 --auto_noise 1 < $< > $@
data2_out.dat: data2.dat $(PROG) Makefile
	$(PROG) --noise 0.05 --maxn 150 --auto_noise 1 < $< > $@

clean:
	rm -f *.dat *.png
