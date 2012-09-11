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

#ifdef G4UI_USE
#include "G4UIExecutive.hh"
#endif

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
    //
    G4VUserPrimaryGeneratorAction* gen_action = new PrimaryGeneratorAction(detector);
    runManager->SetUserAction(gen_action);
    //
    SteppingAction* stepping_action = new SteppingAction;
    runManager->SetUserAction(stepping_action);
    
    // Run action
    G4UserRunAction* run_action = new RunAction(stepping_action);
    runManager->SetUserAction(run_action);
    
    
    // Initialize G4 kernel
    //
    runManager->Initialize();
    runManager->BeamOn(1000000);
    
//#ifdef G4VIS_USE
//    G4VisManager* visManager = new G4VisExecutive;
//    visManager->Initialize();
//#endif
    
    // Get the pointer to the User Interface manager
//    //
//    G4UImanager * UImanager = G4UImanager::GetUIpointer();
//    
//    if (argc!=1)   // batch mode
//    {
//        G4String command = "/control/execute ";
//        G4String fileName = argv[1];
//        UImanager->ApplyCommand(command+fileName);
//    }
//    else           // interactive mode : define UI session
//    {
//#ifdef G4UI_USE
//        G4UIExecutive * ui = new G4UIExecutive(argc,argv);
//#ifdef G4VIS_USE
//        UImanager->ApplyCommand("/control/execute vis.mac");
//#endif
//        ui->SessionStart();
//        delete ui;
//#endif
//        
//#ifdef G4VIS_USE
//        delete visManager;
//#endif
//    }
    
    // Free the store: user actions, physics_list and detector_description are
    //                 owned and deleted by the run manager, so they should not
    //                 be deleted in the main() program !
    
    delete runManager;
    
    return 0;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

