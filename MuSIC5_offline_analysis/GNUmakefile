# GNUmakefile to make programs for MuSIC_Offline_Analysis
# Change PROGNAME and first SOURCES file for different programs

PROGNAME  := mu_analysis
SOURCES   := mu_analysis.cpp $(wildcard src/*.cpp)
OBJECTS   := $(patsubst %.cpp, %.o, ${SOURCES})
INCLUDES  := include/
ROOTFLAGS := $(shell root-config --cflags) # Get ROOT flags for root/include/ etc
ROOTLIBS  := $(shell root-config --libs)   # Get ROOT libs and directory

${PROGNAME}: ${OBJECTS}	
	g++ -o $@ ${OBJECTS} ${ROOTLIBS}

# For all .o targets use the corresponding .cpp file
%.o: %.cpp
	@echo $@
	g++ -c -I${INCLUDES} ${ROOTFLAGS} -o $@ $<

clean:
	rm -rf ${PROGNAME} ${OBJECTS}
