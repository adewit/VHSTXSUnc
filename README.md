# VHSTXSUnc
Scripts heavily based on https://github.com/ajgilbert/HiggsPtWeighting and https://github.com/ajgilbert/EFT2Obs-Demo 

## First setup:

    cd /cvmfs/cms.cern.ch/slc7_amd64_gcc630/cms/cmssw/CMSSW_9_4_0/src/ #(make use of software distributions via cvmfs)
    cmsenv
    cd -
    source setup_env.sh
    source setup_rivet.sh
    source setup_rivet_plugins.sh 
    source setup_env.sh  #Set the environment again
    make #Build pythia plugin

Every subsequent time you want to use the now configured area, source the cms environment from cvmfs and do `source setup_env.sh` again.

The different steps needed are described here:

    python makeLHEReadable.py --inputname pwgevents-0001#inputname should be the full lhe file name except the .lhe extension. This produces pwgevents-0001-mod.lhe
    ./RunPythia cms\_pythia.cmnd pwgevents-0001-mod.lhe 0001-mod.hepmc #Run pythia and create the HepMCFile, with all of the weights.
    rivet --analysis=HiggsTemplateCrossSections 0001-mod.hepmc -o 0001-mod.yoda #run the STXS module on the hepmc file
    yoda2root 0001-mod.yoda #this produces 0001-mod.root

For convenience they have been wrapped in a script as well:

    python launch_jobs.py --inputnames pwgevts-test,pwgevents-0001 --step all
    
The different available steps are 'all' (run the full chain of four steps), 'lhe' (only edit the LHE files), 'lheshower' (edit LHE files to be parsable and run pythia), 'rivet' (only run rivet and yoda2root. This still expects the input file name to be STRING-mod.hepmc)
It is envisaged that the files may need to be read from a different path. The --inputfilepath and --outputfilepath options default to the current directory, but can be set to a different path to read / write the files to/from.
Job submission is possible, the syntax:

    python launch_jobs.py --inputnames pwgevts-test,pwgevents-0001 --step all --job-mode condor --sub-opts '+JobFlavour="longlunch"' --merge 4

Note that the argument to --merge needs to be a multiple of 4; if not the jobs will be mismatched in terms of which in-and output files are produced by the chain of commands

