# This is a simple makefile to build programs that require the ROOT
# libraries (see root.cern.ch).  Modify the variables PROGNAME,
# SOURCES and INCLUDES appropriately (for e.g. additional sources list
# without commas, use \ to go to new line).

# Type gmake to build the program; use gmake test to look e.g. at
# values of defined variables; use gmake clean to remove executable
# and object files.  

# Glen Cowan, RHUL Physics, November 2007.

PROGNAME      = midus_test
SOURCES       = midus_test.cpp ../../src/*.cpp
INCLUDES      = ../../include
ROOTFLAGS     = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --libs)

${PROGNAME}:
	g++ -o $@ ${SOURCES} -I${INCLUDES} ${ROOTFLAGS} ${ROOTLIBS}

clean:
	rm -rf ${PROGNAME}

#OBJECTS       = $(patsubst %.cpp, %.o, $(SOURCES))
#ROOTCFLAGS   := $(shell root-config --cflags)
#ROOTLIBS     := $(shell root-config --libs)
#ROOTGLIBS    := $(shell root-config --glibs)
#ROOTLIBS     := $(shell root-config --nonew --libs)
#CFLAGS       += $(ROOTCFLAGS)
#LIBS         += $(ROOTLIBS)
#  Not sure why Minuit isn't being included -- put in by hand
#
#LIBS         += -lMinuit
#LDFLAGS       = -O

#$(PROGNAME):    $(OBJECTS)
#		g++ -o $@ $(OBJECTS) -I${INCLUDES} $(LDFLAGS) $(LIBS)
#
#../../src/%.o :$(SOURCE_T) 
#%.o : %.cpp  
#	g++ ${CFLAGS} -c  -g -o $@ $<

#test:
#	@echo $(ROOTCFLAGS)

#clean:	
#	-rm -f ${PROGNAME} ${OBJECTS}
