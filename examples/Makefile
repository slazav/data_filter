all: data1_skip.dat data2_skip.dat data2_avrg.dat data1_avrg.dat 

data1.dat: mk_test_data
	./$<
data2.dat: mk_test_data2
	./$<

# There are two test programs:
# test_graphene creates a database, and uses it for filtering, as in real life.
# test_simple just run the filter command in non-safe tcl interpreter,
# good for debugging.

#TEST_PRG=./test_graphene
PROG=../data_filter

data1_skip.dat: data1.dat $(PROG)
	$(PROG) --avrg 0 --maxd 1.5 --maxn 50 < $< > $@

data2_skip.dat: data2.dat $(PROG)
	$(PROG) --avrg 0 --maxd 1.5 --maxn 50 < $< > $@

data1_avrg.dat: data1.dat $(PROG)
	$(PROG) --avrg 1 --maxd 1.5 --maxn 50 < $< > $@

data2_avrg.dat: data2.dat $(PROG)
	$(PROG) --avrg 1 --maxd 1.5 --maxn 50 < $< > $@

clean:
	rm -f *.dat *.png
