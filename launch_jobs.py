from jobs import Jobs
import argparse
import os
import ROOT
import json
from array import array
from itertools import product

job_mgr = Jobs()
parser = argparse.ArgumentParser()

parser.add_argument('--step', default='none', choices=['none', 'lhe', 'lheshower', 'rivet', 'all'])
parser.add_argument('--shower-cmd', default='./RunPythia cms_pythia.cmnd')
parser.add_argument('--inputnames', default='test')
parser.add_argument('--infilepath', default='.')
parser.add_argument('--outfilepath', default='.')

job_mgr.attach_job_args(parser)
args = parser.parse_args()
job_mgr.set_args(args)

namelist = args.inputnames.split(',')

for name in namelist:
    if args.step in ['lhe', 'lheshower','all']:
       job_mgr.job_queue.append('python makeLHEReadable.py --inputname %s --inpath %s --outpath %s'%(name,args.infilepath,args.outfilepath)) 

    if args.step in ['lheshower','all']:
       job_mgr.job_queue.append('%s %s/%s-mod.lhe %s/%s-mod.hepmc'%(args.shower_cmd,args.outfilepath,name,args.outfilepath,name))

    if args.step in ['rivet']:
       job_mgr.job_queue.append('rivet --analysis=HiggsTemplateCrossSections %s/%s-mod.hepmc -o %s/%s-mod.yoda'%(args.infilepath,name, args.outfilepath,name))
       job_mgr.job_queue.append('yoda2root %s-mod.yoda'%(name))


    if args.step in ['all']:
       job_mgr.job_queue.append('rivet --analysis=HiggsTemplateCrossSections %s/%s-mod.hepmc -o %s/%s-mod.yoda'%(args.outfilepath,name, args.outfilepath,name))
       job_mgr.job_queue.append('yoda2root %s-mod.yoda'%(name))


 
job_mgr.flush_queue()

