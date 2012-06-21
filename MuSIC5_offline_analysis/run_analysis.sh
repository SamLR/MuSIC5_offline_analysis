#!/bin/bash
# run_analysis.sh -- runs an analysis program over multiple files
#                 -- Usage: . ./run_analysis.sh ANALYSIS FILES
#					-- ANALYSIS = name of analysis program to run
#					-- FILES    = names of files to combine (enclosed by " ")
#								  NB can except e.g. *.root

# Later make it so that you specifiy program on command line with e.g. ANALYSIS "FILES"
# and also specifiy the input files

if [ $# -ne 2 ] ; then
	echo "Incorrect usage"
	echo ". ./run_analysis.sh ANALYSIS FILES"
	echo "where ANALYSIS is the name of the analysis program to run"
	echo "and FILES is a list of files (enclosed by \" \" and can use wildcards e.g. \"*.root\")"
	return 1;
fi
ANALYSIS=$1
FILES=$2

# Check that ANALYSIS and FILES actually exist
if [ ! -x ${ANALYSIS} ] ; then
	echo "${ANALYSIS} is not an executable -- exiting"
	return 1;
fi

for FILE_NAME in ${FILES}
do
	if [ ! -e ${FILE_NAME} ] ; then
		echo "${FILE_NAME} doesn't exist -- exiting"
		return 1;
	fi
done

hadd -f complete.root ${FILES}
./${ANALYSIS} -i complete.root
