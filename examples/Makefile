all: data1_out.dat data2_out.dat

data1.dat: mk_test_data
	./$<
data2.dat: mk_test_data2
	./$<

PROG=../data_filter

data1_out.dat: data1.dat $(PROG)
	$(PROG) --avrg 1 --maxd 0.05 --maxn 50 < $< > $@
data2_out.dat: data2.dat $(PROG)
	$(PROG) --avrg 1 --maxd 0.05 --maxn 50 < $< > $@

clean:
	rm -f *.dat *.png
