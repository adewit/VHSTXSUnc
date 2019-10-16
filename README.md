# VHSTXSUnc
Scripts heavily based on https://github.com/ajgilbert/HiggsPtWeighting and https://github.com/ajgilbert/EFT2Obs-Demo 

Workflow has currently been tested on the NAF, an slc7 version will be provided for lxplus
## First setup:

    /cvmfs/cms.cern.ch/slc6_amd64_gcc630/cms/cmssw/CMSSW_9_4_13/src/ #(make use of software distributions via cvmfs)
    cmsenv
    cd -
    source setup_env.sh
    source setup_rivet.sh
    source setup_rivet_plugins.sh 
    source setup_env.sh  #Set the environment again
    make #Build pythia plugin

Every subsequent time you want to use the now configured area, source the cms environment from cvmfs and do `source setup_env.sh` again.

The different steps needed are described here, and are still to be wrapped in a single script.

    python makeLHEReadable.py --inputname pwgevents-0001 #inputname should be the full lhe file name except the .lhe extension. This produces pwgevents-0001-mod.lhe
    ./RunPythia cms\_pythia.cmnd pwgevents-0001-mod.lhe 0001-mod.hepmc #Run pythia and create the HepMCFile, with all of the weights.
    rivet --analysis=HiggsTemplateCrossSections 0001-mod.hepmc -o 0001-mod.yoda #run the STXS module on the hepmc file
    yoda2root 0001-mod.yoda #this produces 0001-mod.root

The final output files has histograms for each of the different weight variations, which can be analysed. Note: the central value is duplicated! (these should be index 0 and index 7.
   
