// calibration_functions.h
// -- Defines the calibration functions
// Created: 17/06/2012 Andrew Edmonds

#ifndef CALIBRATION_FUNCTIONS_H 
#define CALIBRATION_FUNCTIONS_H 1

int null_calibration(int const ch, int const val, int const para1);

int qdc_calibration(int const ch, int const val, int const para1);

int adc_calibration(int const ch, int const val, int const para1);

int tdc_calibration(int const ch, int const val, int const para1);
#endif
