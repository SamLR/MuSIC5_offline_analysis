//
//  getopt_test.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 18/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <getopt.h>
#include <assert.h>

int main(int argc, char** argv){
    int aflag = 0;
    int bflag = 0;
    char *cvalue[20];
    int index;
    int c;
    int c_index = 0;
    
    opterr = 0;
    while ((c = getopt (argc, argv, "abc:")) != -1)
        switch (c)
    {
        case 'a':
            aflag = 1;
            break;
        case 'b':
            bflag = 1;
            break;
        case 'c':
            cvalue[c_index++] = optarg;
            break;
        case '?':
            if (optopt == 'c')
                fprintf (stderr, "Option -%c requires an argument.\n", optopt);
            else if (isprint (optopt))
                fprintf (stderr, "Unknown option `-%c'.\n", optopt);
            else
                fprintf (stderr,
                         "Unknown option character `\\x%x'.\n",
                         optopt);
            return 1;
        default:
            abort ();
    }
    
    printf ("aflag = %d, bflag = %d\n",
            aflag, bflag);
    
    for (int i = 0; i < c_index; ++i) {
        printf("c = %s\n", cvalue[i]);
    }
    
    for (index = optind; index < argc; index++)
        printf ("Non-option argument %s\n", argv[index]);
    return 0;
}