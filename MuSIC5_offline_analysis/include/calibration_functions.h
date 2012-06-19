// calibration_functions.h
// -- Defines the calibration functions
// Created: 17/06/2012 Andrew Edmonds

#ifndef CALIBRATION_FUNCTIONS_H 
#define CALIBRATION_FUNCTIONS_H 1

int null_calibration(int const ch, int const val);

int qdc_calibration(int const ch, int const val);

int adc_calibration(int const ch, int const val);

int tdc_calibration(int const ch, int const val);
#endif
