// calibration_functions.h
// -- Defines the calibration functions
// Created: 17/06/2012 Andrew Edmonds

#ifndef CALIBRATION_FUNCTIONS_H 
#define CALIBRATION_FUNCTIONS_H 1

double null_calibration(int const ch, int const val, int const para1);

double qdc_calibration(int const ch, int const val, int const para1);

double adc_calibration(int const ch, int const val, int const para1);

double tdc_calibration(int const ch, int const val, int const para1);
#endif
