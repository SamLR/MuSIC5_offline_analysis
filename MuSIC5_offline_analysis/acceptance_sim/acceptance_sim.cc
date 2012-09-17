//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
//
// $Id: exampleN02.cc,v 1.16 2009-10-30 14:59:59 allison Exp $
// GEANT4 tag $Name: not supported by cvs2svn $
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "PrimaryGeneratorAction.hh"
#include "SteppingAction.hh"
#include "RunAction.hh"

#include "G4RunManager.hh"
#include "G4UImanager.hh"

#ifdef G4VIS_USE
#include "G4VisExecutive.hh"
#endif

//#ifdef G4UI_USE
#include "G4UIExecutive.hh"
//#endif

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

int main(int argc,char** argv)
{
    // Run manager
    //
    G4RunManager * runManager = new G4RunManager;
    
    // User Initialization classes (mandatory)
    //
    DetectorConstruction* detector = new DetectorConstruction;
    runManager->SetUserInitialization(detector);
    //
    G4VUserPhysicsList* physics = new PhysicsList;
    runManager->SetUserInitialization(physics);
    
    // User Action classes
    ///Users/samcook/code/MuSIC/offline_analysis_music5/MuSIC5_offline_analysis/MuSIC5_offline_analysis/acceptance_sim/acceptance_sim.cc
    PrimaryGeneratorAction* gen_action = new PrimaryGeneratorAction(detector, "../../../inputs/monitor6_By-0T_cor.root");
    runManager->SetUserAction(gen_action);
    //
    SteppingAction* stepping_action = new SteppingAction;
    runManager->SetUserAction(stepping_action);
    
    // Run action
    G4UserRunAction* run_action = new RunAction(stepping_action);
    runManager->SetUserAction(run_action);
    
    
#ifdef G4VIS_USE
    G4VisManager* visManager = new G4VisExecutive;
    visManager->Initialize();
#endif
    
    // Get the pointer to the User Interface manager

    
    if (argc!=1)   // use macro
    {
        G4cout << "WARNING: gun mode set to beam pipe" << G4endl;
        gen_action->SetGunMode(beam_pipe);
        G4UImanager * UImanager = G4UImanager::GetUIpointer();
        G4String command = "/control/execute ";
        G4String fileName = argv[1];
        UImanager->ApplyCommand(command+fileName);
        delete UImanager;
    }
    else           // dumb mode
    {
        
        // Initialize G4 kernel
        //
        runManager->Initialize();
        runManager->BeamOn(1000000);
        gen_action->SetGunMode(beam_pipe);
        G4cout << "Starting beam run"<< G4endl;
        runManager->BeamOn(1000000);
    }
    
    // Free the store: user actions, physics_list and detector_description are
    //                 owned and deleted by the run manager, so they should not
    //                 be deleted in the main() program !
    
#ifdef G4VIS_USE
    delete visManager;
#endif
    delete runManager;
    
    return 0;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

