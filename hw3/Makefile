ifndef LIBHOME
ifdef MASTERDIR
   LIBHOME := $(MASTERDIR)/pkg/$(ARCH)/horn
else
   LIBHOME := $(HOME)/pkg/horn
endif
endif

CXXFLAGS = -g -Wall -I$(LIBHOME)/include

LOADLIBS = -L$(LIBHOME)/lib -lgc -lpthread -lrt

default: 6 7

6: 6-parser.o
	g++ $(CXXFLAGS) -o $@ $< $(LOADLIBS)

6-parser.o: 6-parser.cc

6-parser.cc : 6.hn
	horn 6.hn

7: 7.o
	g++ $(CXXFLAGS) -o $@ $<

clean:
	rm -f *.o *~ 
	rm -f 7 6 6.cc 6.output horn-common.h horn-parse-lex.cc 6-*


