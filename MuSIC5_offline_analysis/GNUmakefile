# GNUmakefile to make programs for MuSIC_Offline_Analysis
# Change PROGNAME and first SOURCES file for different programs

PROGNAME  := mu_analysis
PROGNAME2 := mid2root_converter
SOURCES	  := $(wildcard src/*.cpp)
OBJECTS	  := $(patsubst %.cpp, %.o, ${SOURCES})
INCLUDES  := include/
ROOTFLAGS := $(shell root-config --cflags) # Get ROOT flags for root/include/ etc
ROOTLIBS  := $(shell root-config --libs)   # Get ROOT libs and directory

all: ${PROGNAME} ${PROGNAME2}

${PROGNAME}: ${PROGNAME}.o ${OBJECTS}	
	g++ -o $@ ${PROGNAME}.o ${OBJECTS} ${ROOTLIBS}

${PROGNAME2}: ${PROGNAME2}.o ${OBJECTS} 
	g++ -o $@ ${PROGNAME2}.o ${OBJECTS} ${ROOTLIBS}

# For all .o targets use the corresponding .cpp file
%.o: %.cpp
	@echo $@
	g++ -c -I${INCLUDES} ${ROOTFLAGS} -o $@ $<

clean:
	rm -rf ${PROGNAME} ${OBJECTS}
	rm -rf ${PROGNAME2} ${OBJECTS}
