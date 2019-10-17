import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--inputname', type=str)
parser.add_argument('--inpath', type=str)
parser.add_argument('--outpath', type=str)
args = parser.parse_args()

wgtgrouprep=False
wgtid=False
counter=0
all_lines =[]
with open (r'%s/%s.lhe'%(args.inpath,args.inputname), mode='r') as f:
  for line in f.readlines():
    if wgtgrouprep:
      line = line.replace('11','0')
      line = line.replace('12','1')
      line = line.replace('21','2')
      line = line.replace('22','3')
      line = line.replace('1H','4')
      line = line.replace('H1','5')
      line = line.replace('HH','6')
    if "</weights>" in line:
      line = line.replace("weights","rwgt")
      wgtid=False
    if wgtid:
      tmpline = line.replace('\n',"</wgt>\n")
      line = '<wgt id=\'%i\'>'%counter 
      line = line + tmpline
      counter+=1
    if "<weightgroup" in line:
      wgtgrouprep=True
    if "</weightgroup" in line:
      wgtgrouprep=False
    if "<weights>" in line:
      line = line.replace("weights","rwgt")
      wgtid=True
      counter=0
    all_lines.append(line) 

with open(r'%s/%s-mod.lhe'%(args.outpath,args.inputname), mode='w') as newfile:
  newfile.writelines(all_lines)
   
