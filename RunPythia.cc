// main31.cc is a part of the PYTHIA event generator.
// Copyright (C) 2017 Richard Corke, Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Example how to perform merging with PWOHEG-BOX events,
// based on the code found in include/Pythia8Plugins/PowhegHooks.h.

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/PowhegHooks.h"
#include "Pythia8Plugins/HepMC2.h"
#include "TFile.h"
#include "TTree.h"

#include <string>
#include <iostream>
using namespace Pythia8;

//==========================================================================

using namespace Pythia8;
int main(int argc, char *argv[]) {

  if (argc < 4) {
    std::cout << "Not enough options specified, usage is: RunPythia [pythia cmnd file] [input file] [output file]" << std::endl;
    return 1;
  }

  std::string cmnd_file = argv[1];
  std::string lhe_input_file = argv[2];
  std::string hepmc_output_file = argv[3];

  HepMC::Pythia8ToHepMC ToHepMC;
  HepMC::IO_GenEvent ascii_io(hepmc_output_file, std::ios::out);

  Pythia pythia;

  pythia.readFile(cmnd_file);

  pythia.readString("Beams:frameType = 4");
  pythia.readString("Beams:LHEF = " + lhe_input_file);
  pythia.init();

  // Read in main settings
  int nEvent      = pythia.settings.mode("Main:numberOfEvents");
  int nError      = pythia.settings.mode("Main:timesAllowErrors");
  // Read in key POWHEG merging settings
  int vetoMode    = pythia.settings.mode("POWHEG:veto");
  int MPIvetoMode = pythia.settings.mode("POWHEG:MPIveto");
  bool loadHooks  = (vetoMode > 0 || MPIvetoMode > 0);

  // Add in user hooks for shower vetoing
  PowhegHooks *powhegHooks = NULL;
  if (loadHooks) {

    // Set ISR and FSR to start at the kinematical limit
    if (vetoMode > 0) {
      pythia.readString("SpaceShower:pTmaxMatch = 2");
      pythia.readString("TimeShower:pTmaxMatch = 2");
    }

    // Set MPI to start at the kinematical limit
    if (MPIvetoMode > 0) {
      pythia.readString("MultipartonInteractions:pTmaxMatch = 2");
    }

    powhegHooks = new PowhegHooks();
    pythia.setUserHooksPtr((UserHooks *) powhegHooks);
  }

  // Initialise and list settings

  // Counters for number of ISR/FSR emissions vetoed
  unsigned long int nISRveto = 0, nFSRveto = 0;

  // Begin event loop; generate until nEvent events are processed
  // or end of LHEF file
  int iEvent = 0, iError = 0;
  while (true) {

    // Generate the next event
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop
      if (pythia.info.atEndOfFile()) break;

      // Otherwise count event failure and continue/exit as necessary
      cout << "Warning: event " << iEvent << " failed" << endl;
      if (++iError == nError) {
        cout << "Error: too many event failures.. exiting" << endl;
        break;
      }

      continue;
    }

    if (loadHooks) {
      nISRveto += powhegHooks->getNISRveto();
      nFSRveto += powhegHooks->getNFSRveto();
    }

    // If nEvent is set, check and exit loop if necessary

    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
    hepmcevt->weights().clear();
    for (int i = 0; i < pythia.info.getWeightsDetailedSize(); i++){
      hepmcevt->weights().push_back(pythia.info.getWeightsDetailedValue(std::to_string(i)));
    }

    ToHepMC.fill_next_event( pythia, hepmcevt );
    ascii_io << hepmcevt;
    delete hepmcevt;
    if (iEvent % 100 == 0) {
        std::cout << "Processed " << iEvent << "events...\n";
    }
    ++iEvent;
    if (nEvent != 0 && iEvent == nEvent) break;

  } // End of event loop.

  // Statistics, histograms and veto information
  pythia.stat();
  cout << "Number of ISR emissions vetoed: " << nISRveto << endl;
  cout << "Number of FSR emissions vetoed: " << nFSRveto << endl;
  cout << endl;

  // Done.
  if (powhegHooks) delete powhegHooks;
  return 0;
}
