//
//  STSmartFile.hh
//  stopping_target_sim
//
//  Created by Sam Cook on 30/01/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef smart_tfile_hh
#define smart_tfile_hh 1

#include "globals.hh"
#include "TFile.h"
#include <map>
#include <string>

class smart_tfile: public TFile
{
public:
    static smart_tfile* getTFile(std::string, std::string); // returns the smart file of given name with options
    
    void close();
    static void forceClose();
    
private:
    smart_tfile();
    smart_tfile(std::string, std::string);
    ~smart_tfile();
    
    G4int getPtrCount(){return mPtrCount;}
    void incPtrCount(){++mPtrCount;}
    void decPtrCount(){--mPtrCount;}
    
    G4int mPtrCount;
    
    static std::map<std::string, smart_tfile*> mFileMap; // filename: file ptr pairs
    
};



#endif
