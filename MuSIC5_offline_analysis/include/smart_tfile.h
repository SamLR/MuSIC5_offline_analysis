//
//  STSmartFile.hh
//  stopping_target_sim
//
//  Created by Sam Cook on 30/01/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef smart_tfile_hh
#define smart_tfile_hh 1

#include "TFile.h"
#include <map>
#include <string>

class smart_tfile: public TFile {
public:
    typedef std::map<std::string, smart_tfile*> file_map; 
    static smart_tfile* getTFile(std::string const, std::string const); // returns the smart file of given name with options
    
    void close();
    static void force_close_all();
    
private:
    // you shouldn't call these constructors directly
    smart_tfile();
    smart_tfile(std::string const, std::string const);
    ~smart_tfile();
    
    // these methods shouldn't be used by clients but
    // we want them to maintain their original functionality
    inline void Close() {this->TFile::Close(); } ;
    inline void Write() {this->TFile::Write(); } ;
    
    int const getPtrCount()const {return mPtrCount;} ;
    inline void incPtrCount(){++mPtrCount;} ;
    inline void decPtrCount(){--mPtrCount;} ;
    
    int mPtrCount;
    
    static file_map file_map_m; // filename: file ptr pairs
    
};


#endif
