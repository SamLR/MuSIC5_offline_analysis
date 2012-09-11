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
// $Id: DetectorConstruction.hh,v 1.10 2008-09-22 16:41:20 maire Exp $
// GEANT4 tag $Name: not supported by cvs2svn $
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "globals.hh"
#include "G4VUserDetectorConstruction.hh"

class G4Box;
class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Material;
class G4VPVParameterisation;
class G4UserLimits;
class DetectorMessenger;

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
    
    DetectorConstruction();
    ~DetectorConstruction();
    
public:
    
    G4VPhysicalVolume* Construct();
        
private:
    
    G4Box*             solidWorld;    // pointer to the solid envelope
    G4LogicalVolume*   logicWorld;    // pointer to the logical envelope
    G4VPhysicalVolume* physiWorld;    // pointer to the physical envelope
    
    G4Box*             solidTarget;   // pointer to the solid Target
    G4LogicalVolume*   logicTarget;   // pointer to the logical Target
    G4VPhysicalVolume* physiTarget;   // pointer to the physical Target
    
    G4Box*             solidScint1;  // pointer to the solid Scint1
    G4LogicalVolume*   logicScint1;  // pointer to the logical Scint1
    G4VPhysicalVolume* physiScint1;  // pointer to the physical Scint1
    
    G4Box*             solidScint2;  // pointer to the solid Scint2
    G4LogicalVolume*   logicScint2;  // pointer to the logical Scint2
    G4VPhysicalVolume* physiScint2;  // pointer to the physical Scint2
    
    G4double fWorldX;
    G4double fTargetX;
    G4double fScint1X;
    G4double fScint2X;
    
    G4double fWorldY;
    G4double fTargetY;
    G4double fScint1Y;
    G4double fScint2Y;
    
    G4double fWorldZ;
    G4double fTargetZ;
    G4double fScint1Z;
    G4double fScint2Z;
    
    G4double fSeparatorZ;
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif
