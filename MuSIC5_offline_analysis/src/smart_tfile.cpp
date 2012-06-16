//
//  STSmartFile.cc
//  stopping_target_sim
//
//  Created by Sam Cook on 30/01/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include <cstdlib>
#include <map>
#include <string>
#include "smart_tfile.h"
#include "TFile.h"

std::map<std::string, smart_tfile*> smart_tfile::mFileMap = std::map<std::string, smart_tfile*>();

smart_tfile::smart_tfile(): mPtrCount(1) {;}
smart_tfile::smart_tfile(std::string filename, std::string options)
    :TFile(filename.c_str(), options.c_str()), mPtrCount(1) 
{;}

smart_tfile::~smart_tfile() {;}

void smart_tfile::close()
{
    --mPtrCount;
    if (mPtrCount==0) 
    {
        this->Write();
        delete this;
    }
}

void smart_tfile::forceClose()
{
    // automatically closes all open files ignoring number of active pointers
    std::cout << "WARNING: force closing all open root files"<< std::endl;
    std::map<std::string, smart_tfile*>::iterator iter;
    for (iter = mFileMap.begin(); iter != mFileMap.end(); ++iter) 
    {
        iter->second->Write();
        iter->second->Close();
    }
}

smart_tfile* smart_tfile::getTFile(std::string filename, std::string options)
{
    std::map<std::string, smart_tfile*>::iterator iter;
    iter = mFileMap.find(filename);
    if (iter == mFileMap.end()) 
    {
        // new file
        smart_tfile* ptr = new smart_tfile(filename, options);
        if (!ptr->IsOpen()) 
        {
            std::cout << "\n[ERROR] file "<< filename <<" not opened, exiting"<< std::endl;
            exit(1);
        }
        mFileMap[filename] = ptr;
        return ptr;
    } else
    { 
        smart_tfile* ptr = iter->second;
        ptr->incPtrCount();
        return ptr;
    }
    
}



