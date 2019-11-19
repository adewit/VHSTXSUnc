from ROOT import *; import glob, numpy as n; from array import array
from AdditionalFunctions import*

#inputFileName = "pwgevents-0001-mod"
inputFileName = "../pwgevents-hadd-mod"
gStyle.SetOptStat(0);
gStyle.SetTitleYOffset(1.2)
gStyle.SetTitleXOffset(1.2)
xsec = 0.044837
r = 0.5 #factor dor deltaX, X>=150
CMS=True
if CMS:NVar = 9
else:NVar = 8

histcolors = [221,94, 209, 4, 2, 1]
scaleVars=[]#array of histogram with scale variations
scaleVarsReBinned=[]#array of histogram with scale variations
scaleVarsInclpT=[]#array of histogram with scale variations
scaleVarsInclpTXTitles=[]#array of histogram with scale variations
deltaTitles = ["#Delta_{Y}", "#Delta_{75}", "#Delta_{150}", "#Delta_{250}", "#Delta_{400}", "Total"]
pTtitles = ["0-75 GeV", "75-150 GeV", "150-250 GeV", "250-400 GeV", ">400 GeV"]
scaleTitles= ["#mu_{R}=1.0 & #mu_{F}=1.0","#mu_{R}=1.0 & #mu_{F}=2.0", "#mu_{R}=2.0 & #mu_{F}=1.0", "#mu_{R}=2.0 & #mu_{F}=2.0", "#mu_{R}=1.0 & #mu_{F}=0.5", "#mu_{R}=0.5 & #mu_{F}=1.0", "#mu_{R}=0.5 & #mu_{F}=0.5"]
CMS=True
if not CMS:
    inputFileName = "../pwgevents-hadd-mod"
    f = TFile(inputFileName+".root", "read")
else:
    filein = TFile("../STXSUnc/ZH_ZToLL_HToBB.root",'read')
    maintree=filein.Get("Events")

for i in range(0,NVar):
    if not CMS:
        if i>0:
            scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30["+str(i)+"]"))
        else:scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30")) #forward region
        scaleVars[i].SetName("scaleVars"+str(i))
        scaleVarsInclpT.insert(i,GetInclpT(scaleVars[i], "scaleVarsInclpT_"+str(i)))
    else:
        scaleVars.insert(i,  TH1F("scaleVars"+str(i),"scaleVars"+str(i),16,400,416))
        maintree.Draw("HTXS_stage_1p1_uncert_cat>>scaleVars"+str(i), "1*(LHEScaleWeight["+str(i)+"]*genWeight)","goff");
        scaleVarsInclpT.insert(i,GetInclpTCMS(scaleVars[i], "scaleVarsInclpT_"+str(i)))

if not CMS:
    centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30") # mur = 1, muf=1
    centralScaleInclpT = GetInclpT(centralScale, 'centralScaleInclpT')
else:
    centralScaleInclpT =scaleVarsInclpT[4].Clone()
    centralScaleInclpT.SetName("centralScaleInclpT")

MaxScaleDeviationInclpT  = centralScaleInclpT.Clone()
MaxScaleDeviationInclpT.SetName("MaxScaleDeviationInclpT")#histogram with maximum deviations from central scale with all processes combined.
MaxScaleDeviationInclpT.SetTitle("MaxScaleDeviationInclpT")#histogram with maximum deviations from central scale with all processes combined.

#defining the max deviation
for k in range(1, centralScaleInclpT.GetNbinsX()+1):
    dN=[]
    if centralScaleInclpT.GetBinContent(k)==0:continue;
    for i in range(0,NVar):
        if i==6 and CMS:continue;
        dN.insert(i,abs(scaleVarsInclpT[i].Integral(k, centralScaleInclpT.GetNbinsX()+1)-centralScaleInclpT.Integral(k, centralScaleInclpT.GetNbinsX()+1)))
    dNMax = max(dN)
    print dN, dNMax, k
    MaxScaleDeviationInclpT.SetBinContent(k, dNMax)

UncInPt=[]
deltaY = 0; delta75=0; delta150=0; delta250=0; delta400=0; total=0;
for k in range(0, 6):
    UncInPt.insert(k, TH1F("UncInPtBins"+str(k), "",npTBins, 0,npTBins))#k:0=deltaY, 1=delta75, 2=delta150, 3=delta250, 4=delta400, 5=total= 

#Define deltas:
for i in range(1, 6):
    deltas = []
    deltaY = 0.006                   
    if i==1:
        delta75 = -MaxScaleDeviationInclpT.GetBinContent(2)/(centralScaleInclpT.GetBinContent(1));
    elif i==2:
        delta75 = MaxScaleDeviationInclpT.GetBinContent(2)/(centralScaleInclpT.Integral(2,5));
        delta150 = -r*MaxScaleDeviationInclpT.GetBinContent(3)/centralScaleInclpT.GetBinContent(2);
    elif i==3:
        delta75 = MaxScaleDeviationInclpT.GetBinContent(2)/(centralScaleInclpT.Integral(2,5));
        delta150 = r*MaxScaleDeviationInclpT.GetBinContent(3)/centralScaleInclpT.Integral(3,5);
        delta250 = -r*MaxScaleDeviationInclpT.GetBinContent(4)/centralScaleInclpT.GetBinContent(3)
    elif i==4:       
        delta75 = MaxScaleDeviationInclpT.GetBinContent(2)/(centralScaleInclpT.Integral(2,5));
        delta150 = r*MaxScaleDeviationInclpT.GetBinContent(3)/centralScaleInclpT.Integral(3,5);
        delta250 = r*MaxScaleDeviationInclpT.GetBinContent(4)/centralScaleInclpT.Integral(4,5);
        delta400 = -r*MaxScaleDeviationInclpT.GetBinContent(5)/centralScaleInclpT.GetBinContent(4);
    elif i==5:
        delta75 = MaxScaleDeviationInclpT.GetBinContent(2)/(centralScaleInclpT.Integral(2,5));
        delta150 = r*MaxScaleDeviationInclpT.GetBinContent(3)/centralScaleInclpT.Integral(3,5);
        delta250 = r*MaxScaleDeviationInclpT.GetBinContent(4)/centralScaleInclpT.Integral(4,5);
        delta400 = r*MaxScaleDeviationInclpT.GetBinContent(5)/centralScaleInclpT.Integral(5,5);
    total = sqrt(deltaY**2 + delta75**2+delta150**2 + delta250**2 + delta400**2)
    deltas.insert(0,deltaY)
    deltas.insert(1,delta75)
    deltas.insert(2,delta150)
    deltas.insert(3,delta250)
    deltas.insert(4,delta400)
    deltas.insert(5,total)
    #fill the histograms:
    for k in range(0, 6):
        UncInPt[k].SetBinContent(i,deltas[k])
        UncInPt[k].GetXaxis().SetBinLabel(i,pTtitles[i-1])


#Save the results
fOut = TFile("MaxScaleVarInclpT.root",'recreate')
MaxScaleDeviationInclpT.Write()
centralScaleInclpT.Write()
for i in range(0,NVar):
    scaleVarsInclpT[i].Write()
#    scaleVars[i].Write()
#    scaleVarsReBinned[i].Write()
#    ScaleDeviationsInclpT[i].Write()
for i in range(1, 6):
    UncInPt[i].Write()
fOut.Close()
#Plotting 

_MYW = 800; _MYH = 600
_MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
_MYL = 0.14*_MYW; _MYR = 0.18*_MYW
cB=0;
cB=TCanvas("cB","cB",_MYW,_MYH);
cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
UncInPt[0].SetLineColor(6)
UncInPt[0].SetYTitle("Relative QCD uncertainty")
UncInPt[0].SetAxisRange(-0.04, 0.1, "Y");
UncInPt[0].Draw()
UncInPt[0].SetLineWidth(3)
for i in range(1, 6):
    UncInPt[i].SetLineColor(histcolors[i])
    UncInPt[i].SetLineWidth(2)
    UncInPt[i].Draw("same")
leg = TLegend(0.7, 0.7, 0.9, 0.90);
leg.SetTextFont(42)
for i in range(0, 6):
    leg.AddEntry(UncInPt[i], deltaTitles[i], "l");
leg.Draw('same');
cB.SetTickx(0); cB.SetTicky(0);
cB.SaveAs("pTBinsUnc.pdf");
