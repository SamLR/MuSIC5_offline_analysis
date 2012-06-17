// calibration_functions.h
// -- Defines the calibration functions
// Created: 17/06/2012 Andrew Edmonds

#ifndef CALIBRATION_FUNCTIONS_H_
#define CALIBRATION_FUNCTIONS_H_

int null_calibration(int const ch, int const val) {
	return val;
}

int adc_calibration(int const ch, int const val) {
	return val;
}

int phadc_calibration(int const ch, int const val) {
	return val;
}

int tdc_calibration(int const ch, int const val) {
	return val;
}

#endif
