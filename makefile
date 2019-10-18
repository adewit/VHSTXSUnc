
CXX=g++
CXXFLAGS=-std=c++14

main: RunPythia

RunPythia: RunPythia.cc
		$(CXX) $(CXXFLAGS) $^ -o $@ -I${PYTHIA8_DIR}/include -I/cvmfs/cms.cern.ch/slc7_amd64_gcc630/external/hepmc/2.06.07/include/ -I$(shell root-config --incdir) $(shell root-config --libs) -L${CMSSW_DIR}/lib -lpythia8 -lHepMC -ltbb -llzma -lpcre -lpcreposix
clean:
	  rm RunPythia
