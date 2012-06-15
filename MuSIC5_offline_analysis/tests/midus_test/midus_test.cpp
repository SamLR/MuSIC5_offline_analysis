// midus_test.cpp
// -- To test the midus_entry class
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "../../include/midus_entry.h"

int main() {
	midus_entry* test = new midus_entry();
	
	for (int i = 0; i < 5; i++) {
		std::cout << test->get_QDC_value(i) << " " << test->get_TDC_value(i) << std::endl;
	}
	std::cout << test->get_event_number() << std::endl;
	delete test;
	return 0;
}
