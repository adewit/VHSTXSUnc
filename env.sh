#!/usr/bin/env bash
export LHAPDF_CONFIG_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc630/external/lhapdf/6.2.1-ghjeda/bin/lhapdf-config"
export RIVET_ANALYSIS_PATH=${PWD}/Classification
export RIVET_VERSION="3.0.1"
export HIGGSPRODMODE=QQ2ZH

if [ -f "local/rivetenv.sh" ]; then
	source local/rivetenv.sh
fi
