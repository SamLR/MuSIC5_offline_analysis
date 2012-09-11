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
// $Id: DetectorConstruction.cc,v 1.22 2010-01-22 11:57:03 maire Exp $
// GEANT4 tag $Name: not supported by cvs2svn $
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "DetectorConstruction.hh"

#include "G4Material.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4PVParameterised.hh"
#include "G4SDManager.hh"
#include "G4GeometryTolerance.hh"
#include "G4GeometryManager.hh"

#include "G4UserLimits.hh"

#include "G4VisAttributes.hh"
#include "G4Colour.hh"

#include "G4ios.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::DetectorConstruction()
:solidWorld(0),  logicWorld(0),  physiWorld(0),
solidTarget(0), logicTarget(0), physiTarget(0),
solidScint1(0), logicScint1(0), physiScint1(0),
solidScint2(0), logicScint2(0), physiScint2(0),
fWorldX(1*m), fTargetX (37*cm), fScint1X (38*cm),  fScint2X(38*cm),
fWorldY(1*m), fTargetY (31*cm), fScint1Y(8*3*cm), fScint2Y(5*5*cm),
fWorldZ(1*m), fTargetZ(0.5*mm), fScint1Z(0.5*mm), fScint2Z(3.5*mm),
fSeparatorZ(3*mm)
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorConstruction::~DetectorConstruction()
{}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

G4VPhysicalVolume* DetectorConstruction::Construct()
{
    //--------- Material definition ---------
    
    G4double a, z;
    G4double density;
    G4int nel;
    
    //Air
    G4Element* N = new G4Element("Nitrogen", "N", z=7., a= 14.01*g/mole);
    G4Element* O = new G4Element("Oxygen"  , "O", z=8., a= 16.00*g/mole);
    
    G4Material* Air = new G4Material("Air", density= 1.29*mg/cm3, nel=2);
    Air->AddElement(N, 70*perCent);
    Air->AddElement(O, 30*perCent);
    
    //Lead
//    G4Material* Pb = new G4Material("Lead", z=82., a= 207.19*g/mole, density= 11.35*g/cm3);
    
    
    //--------- Definitions of Solids, Logical Volumes, Physical Volumes ---------
    
    //------------------------------
    // World
    //------------------------------
        
    solidWorld= new G4Box("world",fWorldX/2, fWorldY/2, fWorldZ/2);
    logicWorld= new G4LogicalVolume( solidWorld, Air, "World", 0, 0, 0);
    
    //  Must place the World Physical volume unrotated at (0,0,0).
    //
    physiWorld = new G4PVPlacement(0,               // no rotation
                                   G4ThreeVector(), // at (0,0,0)
                                   logicWorld,      // its logical volume
                                   "World",         // its name
                                   0,               // its mother  volume
                                   false,           // no boolean operations
                                   0);              // copy number
    
    //------------------------------
    // Target
    //------------------------------
    
    // position at centre
    G4ThreeVector positionTarget = G4ThreeVector(0,0,0);
    
    solidTarget = new G4Box("target",fTargetX/2, fTargetY/2, fTargetZ/2);
    logicTarget = new G4LogicalVolume(solidTarget, Air,"Target",0,0,0);
    physiTarget = new G4PVPlacement(0,               // no rotation
                                    positionTarget,  // at (x,y,z)
                                    logicTarget,     // its logical volume
                                    "Target",        // its name
                                    logicWorld,      // its mother  volume
                                    false,           // no boolean operations
                                    0);              // copy number
    
    //------------------------------
    // Scint1
    //------------------------------
    
    G4ThreeVector positionScint1 = G4ThreeVector(0,0,+fSeparatorZ);
    
    solidScint1 = new G4Box("Scint1",fScint1X/2,fScint1Y/2,fScint1Z/2);
    logicScint1 = new G4LogicalVolume(solidScint1 , Air, "Scint1",0,0,0);
    physiScint1 = new G4PVPlacement(0,              // no rotation
                                    positionScint1, // at (x,y,z)
                                    logicScint1,    // its logical volume
                                    "Scint1",       // its name
                                    logicWorld,      // its mother  volume
                                    false,           // no boolean operations
                                    0);              // copy number
    
    
    //------------------------------
    // Scint2
    //------------------------------
    
    G4ThreeVector positionScint2 = G4ThreeVector(0,0,-fSeparatorZ);
    
    solidScint2 = new G4Box("Scint2",fScint2X/2,fScint2Y/2,fScint2Z/2);
    logicScint2 = new G4LogicalVolume(solidScint2 , Air, "Scint2",0,0,0);
    physiScint2 = new G4PVPlacement(0,              // no rotation
                                    positionScint2, // at (x,y,z)
                                    logicScint2,    // its logical volume
                                    "Scint2",       // its name
                                    logicWorld,      // its mother  volume
                                    false,           // no boolean operations
                                    0);              // copy number
    
    return physiWorld;
}