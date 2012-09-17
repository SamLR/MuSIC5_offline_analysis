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
// $Id: PrimaryGeneratorAction.cc,v 1.7 2006-06-29 17:48:13 gunter Exp $
// GEANT4 tag $Name: not supported by cvs2svn $
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "PrimaryGeneratorAction.hh"
#include "DetectorConstruction.hh"

#include "G4Event.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"

#include "Randomize.hh"
#include "G4RandomDirection.hh"
#include "globals.hh"

#include "TFile.h"
#include "TTree.h"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......


PrimaryGeneratorAction::PrimaryGeneratorAction(DetectorConstruction* myDC, const char* file_name)
:gun_position_mode(target), particleGun(0), myDetector(myDC)
{
    G4int n_particle = 1;
    particleGun = new G4ParticleGun(n_particle);
    
    // default particle
    
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particle = particleTable->FindParticle("e-");
    
    particleGun->SetParticleDefinition(particle);
    particleGun->SetParticleMomentumDirection(G4ThreeVector(0.,0.,1.));
    particleGun->SetParticleEnergy(10*MeV);
    
    OpenG4BL(file_name);
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

PrimaryGeneratorAction::~PrimaryGeneratorAction()
{
    g4blFile->Close();
    delete g4blFile;
    delete particleGun;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void PrimaryGeneratorAction::OpenG4BL(const char* file_name)
{
    g4blFile = new TFile(file_name);
    particle_tree = (TTree*)g4blFile->Get("t");
    particle_tree->SetBranchAddress("EventID",&in_EventID);
    particle_tree->SetBranchAddress("TrackID",&in_TrackID);
    particle_tree->SetBranchAddress("PDGid",&in_PDGid);
    particle_tree->SetBranchAddress("x",&in_x);
    particle_tree->SetBranchAddress("y",&in_y);
    particle_tree->SetBranchAddress("z",&in_z);
    particle_tree->SetBranchAddress("Px",&in_Px);
    particle_tree->SetBranchAddress("Py",&in_Py);
    particle_tree->SetBranchAddress("Pz",&in_Pz);
    particle_tree->SetBranchAddress("tof",&in_tof);
    particle_tree->SetBranchAddress("Weight",&in_Weight);
    particle_tree->SetBranchAddress("x_new",&in_x_new);
    particle_tree->SetBranchAddress("z_new",&in_z_new);
    particle_tree->SetBranchAddress("Px_new",&in_Px_new);
    particle_tree->SetBranchAddress("Pz_new",&in_Pz_new);
    g_iev = 0;
}

void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
    if (gun_position_mode == target) {
        
        
        // Randomise the position of the particle within the stopping target
        float x =  37*cm * (G4UniformRand() - 0.5);
        float y =  31*cm * (G4UniformRand() - 0.5);
        float z = 0.5*mm * (G4UniformRand() - 0.5);
        // And radomise its direction
        G4ThreeVector direction = G4RandomDirection();
        
        particleGun->SetParticleMomentumDirection(direction);
        particleGun->SetParticlePosition(G4ThreeVector(x,y,z));
        
        particleGun->GeneratePrimaryVertex(anEvent);
    } else if (gun_position_mode == beam_pipe) {
        
        
        do {
            // loop through particles until you find a charged particle
            particle_tree->GetEntry(g_iev++);
        } while (!(abs(in_PDGid) == 11 || abs(in_PDGid) == 13 || // e or mu
                   abs(in_PDGid) == 211 || abs(in_PDGid) == 2212 )); // pi or proton
        
        G4ThreeVector position = G4ThreeVector(in_x*mm, in_y*mm, -30*mm); 
        G4ThreeVector momentum = G4ThreeVector(in_Px*MeV, in_Py*MeV, in_Pz*MeV);
        // dont redefine the energy or other processes can occur (e.g. brem)
        particleGun->SetParticleMomentumDirection(momentum);
        particleGun->SetParticlePosition(position);
        
        particleGun->GeneratePrimaryVertex(anEvent);
    }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

