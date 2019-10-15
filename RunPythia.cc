// Copyright (C) 2017 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"
#include "TFile.h"
#include "TTree.h"

#include <string>
#include <iostream>

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

  // Initialize Les Houches Event File run. List initialization information.
  pythia.readString("Beams:frameType = 4");
  pythia.readString("Beams:LHEF = " + lhe_input_file);
  pythia.init();


  // Allow for possibility of a few faulty events.
  int nAbort = 10;
  int iAbort = 0;

  // Begin event loop; generate until none left in input file.
  for (int iEvent = 0; iEvent <= 1E7; ++iEvent) {

    // Generate events, and check whether generation failed.
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop.
      if (pythia.info.atEndOfFile()) break;

      // First few failures write off as "acceptable" errors, then quit.
      if (++iAbort < nAbort) continue;
      break;
    }

    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
    hepmcevt->weights().clear();
    for (int i = 0; i < pythia.info.getWeightsDetailedSize(); i++){
      hepmcevt->weights().push_back(pythia.info.getWeightsDetailedValue(std::to_string(i)));
    }

    ToHepMC.fill_next_event( pythia, hepmcevt );
    // Write the HepMC event to file. Done with it.
    ascii_io << hepmcevt;
    delete hepmcevt;
    if (iEvent % 100 == 0) {
      std::cout << "Processed " << iEvent << "events...\n";
    }
  }

  return 0;
}
