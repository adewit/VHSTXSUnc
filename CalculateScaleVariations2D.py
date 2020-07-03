from ROOT import *; import glob, numpy as n; from array import array
from AdditionalFunctions import*

#inputFileName = "pwgevents-0001-mod"
gStyle.SetOptStat(0);
gStyle.SetTitleYOffset(1.2)
gStyle.SetTitleXOffset(1.2)
histcolors = [2,94, 209, 221, 4, 1, 923, 435,416,620,435]
CMS=False
if CMS:NVar = 9
else:NVar = 8
#else:NVar = 11
scaleVars=[]#array of histogram with scale variations
scaleVarsCMS=[]#array of histogram with scale variations
scaleVarsRebinnedCMS=[]#array of histogram with scale variations
scaleVarsRebinned=[]#array of histogram with scale variations
scaleVarsInclpT=[]#array of histogram with scale variations
scaleVarsInclpTXTitles=[]#array of histogram with scale variations
pTJetstitles = ["FWD","0-75 GeV0J", "0-75 GeV1J","0-75 GeVGE2J","75-150 GeV0J", "75-150 GeV1J","75-150 GeVGE2J","150-250 GeV0J", "150-250 GeV1J","150-250 GeVGE2J","250-400 GeV0J", "250-400 GeV1J","250-400 GeVGE2J",">400 GeV0J", ">400 GeV1J",">400 GeVGE2J"]
scaleTitles= ["#mu_{R}=1.0 & #mu_{F}=1.0","#mu_{R}=1.0 & #mu_{F}=2.0", "#mu_{R}=2.0 & #mu_{F}=1.0", "#mu_{R}=2.0 & #mu_{F}=2.0", "#mu_{R}=1.0 & #mu_{F}=0.5", "#mu_{R}=0.5 & #mu_{F}=1.0", "#mu_{R}=0.5 & #mu_{F}=0.5"]
if not CMS:
    #inputFileName = "pwgevents-0326-mod"
    #inputFileName = "../VHSTXS_Files/full_isLepton"
    inputFileName = "../VHSTXS_Files/all"
    #inputFileName = "../VHSTXS_Files/pwgevents-393"
    f = TFile(inputFileName+".root", "read")
else:
    filein = TFile("../STXSUnc/ZH_ZToLL_HToBB.root",'read')
    maintree=filein.Get("Events")

if not CMS:
    #centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30[000]") # mur = 1, muf=1
    centralScale = f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30") # mur = 1, muf=1
    centralScaleRebinned = ReorganisedHist(centralScale, 'centralScaleRebinned')
else:
    centralScaleRebinned=scaleVarsRebinned[4].Clone()
    centralScaleRebinned.SetName("centralScaleRebinnedCMS")

scaleVarsRebinnedDiff=[]


for i in range(0,NVar):
    if not CMS:
        if i<10 and  i>0:
            scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30["+str(i)+"]")) 
            #scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30[00"+str(i)+"]")) 
        elif i==0 :scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30")) #forward region
        elif i==10:scaleVars.insert(i, f.Get("/HiggsTemplateCrossSections/STXS_stage1_1_fine_pTjet30[010]")) #forward region
        scaleVars[i].SetName("scaleVars_"+str(i))
        scaleVarsRebinned.insert(i,ReorganisedHist(scaleVars[i], "scaleVarsRebinned_"+str(i)))
        #scaleVarsRebinned[i].Scale(centralScaleRebinned.Integral()/scaleVarsRebinned[i].Integral())
        scaleVarsRebinnedDiff.insert(i, scaleVarsRebinned[i].Clone())
    else:
        scaleVarsCMS.insert(i,  TH1F("scaleVarsCMS"+str(i),"scaleVarsCMS"+str(i),16,400,416))
        maintree.Draw("HTXS_stage_1p1_uncert_cat>>scaleVarsCMS"+str(i), "1*(LHEScaleWeight["+str(i)+"]*genWeight)","goff");
        scaleVarsCMS.insert(i, maintree.GetHistogram())
        scaleVarsRebinned.insert(i, ReorganisedHistCMS(scaleVarsCMS[i], "scaleVarsRebinned_"+str(i)))

MaxScaleDeviationRebinned  = centralScaleRebinned.Clone()
MaxScaleDeviationRebinned.SetName("MaxScaleDeviationRebinned")#histogram with maximum deviations from central scale with all processes combined.
MaxScaleDeviationRebinned.SetTitle("MaxScaleDeviationRebinned")#histogram with maximum deviations from central scale with all processes combined.

for k in range(0, npTBins):
    for j in range(0, nJetBins):
        dN=[]
        globalBin = nJetBins*k + j + 1
        binMax = nJetBins*k+(nJetBins)
        if centralScaleRebinned.GetBinContent(globalBin)==0:
            print globalBin
            continue;
        for i in range(0,NVar):
            if (i==5 or i==7) and CMS:continue;
            dN.insert(i,abs(scaleVarsRebinned[i].Integral(globalBin, binMax)-centralScaleRebinned.Integral(globalBin, binMax)))
            scaleVarsRebinnedDiff[i].SetBinContent(globalBin, scaleVarsRebinned[i].GetBinContent(globalBin) - centralScaleRebinned.GetBinContent(globalBin))
        dNMax = max(dN)
        print globalBin, dN, dNMax, centralScaleRebinned.Integral(globalBin, binMax)
        MaxScaleDeviationRebinned.SetBinContent(globalBin, dNMax)

centralScaleRebinnedCMS=scaleVarsRebinned[4].Clone()
centralScaleRebinnedCMS.SetName("centralScaleRebinnedCMS")
if CMS:f0 = TFile("MaxScaleVarInclpT_CMS.root","read")
else: f0 = TFile("MaxScaleVarInclpT_central.root","read")
UncInPtBins5 = f0.Get("UncInPtBins5")

UncInPtandNJets=[]
for k in range(0, 4):
    UncInPtandNJets.insert(k, TH1F("UncInPtandNJets"+str(k), "",nJetBins*npTBins+1, 0,nJetBins*npTBins+1))#k:0=deltapTTotal, 1=delta1, 2=delta2, 3=total
UncInPtandNJets[0].SetBinContent(1, 0)
UncInPtandNJets[1].SetBinContent(1, 0)
UncInPtandNJets[2].SetBinContent(1, 0)
UncInPtandNJets[3].SetBinContent(1, 0)
##Define deltas:
for j in range(0, nJetBins):
    for k in range(0, npTBins):
        delta1=0;  delta2 = 0;
        globalBin = nJetBins*k + j + 1
        binMax = nJetBins*k+(nJetBins) 
        if j==0:
            delta1 = -MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j+ 2)/centralScaleRebinned.GetBinContent(nJetBins*k+j+1)
            delta2 = 0
        if j==1:
            delta1 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j + 1)/(centralScaleRebinned.Integral(nJetBins*k + j + 1, nJetBins*k + j + 2))
            delta2 = -MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j + 2)/(centralScaleRebinned.GetBinContent(nJetBins*k + j + 1))
        if j==2:
            delta1 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j)/(centralScaleRebinned.Integral(nJetBins*k + j,nJetBins*k + j + 1))
            delta2 = MaxScaleDeviationRebinned.GetBinContent(nJetBins*k + j+1)/centralScaleRebinned.GetBinContent(nJetBins*k + j+1)
        deltapTTotal = UncInPtBins5.GetBinContent(k+1);
        print deltapTTotal
        total = sqrt(deltapTTotal**2 + delta1**2 +  delta2**2)
        UncInPtandNJets[0].SetBinContent(globalBin+1, deltapTTotal)
        UncInPtandNJets[1].SetBinContent(globalBin+1, delta1)
        UncInPtandNJets[2].SetBinContent(globalBin+1, delta2)
        UncInPtandNJets[3].SetBinContent(globalBin+1, total)
        UncInPtandNJets[1].GetXaxis().SetBinLabel(globalBin,pTJetstitles[globalBin-1])
        UncInPtandNJets[2].GetXaxis().SetBinLabel(globalBin,pTJetstitles[globalBin-1])

#Save the results
if CMS:fOut = TFile("MaxScaleVarJetsandPt_CMS.root",'recreate')
else: fOut = TFile("MaxScaleVarJetsandPt_central.root",'recreate')
MaxScaleDeviationRebinned.Write()
centralScaleRebinned.Write()
UncInPtandNJets[1].Write()
UncInPtandNJets[2].Write()
UncInPtandNJets[3].Write()
UncInPtandNJets[0].Write()
for i in range(0,NVar):
    if CMS:scaleVarsCMS[i].Write()
    else: scaleVars[i].Write()
    scaleVarsRebinned[i].Write()
fOut.Close()

_MYW = 800; _MYH = 600
_MYT = 0.08*_MYH; _MYB = 0.18*_MYH;
_MYL = 0.12*_MYW; _MYR = 0.1*_MYW
cB=0;
cB=TCanvas("cB","cB",_MYW,_MYH);
cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
UncInPtandNJets[1].SetLineColor(kRed)
UncInPtandNJets[1].SetAxisRange(-0.15, 0.25, "Y");
UncInPtandNJets[1].SetYTitle("Relative QCD uncertainty")
UncInPtandNJets[1].Draw()
UncInPtandNJets[2].SetLineColor(kBlue)
UncInPtandNJets[2].SetLineWidth(3)
UncInPtandNJets[3].SetLineWidth(3)
UncInPtandNJets[1].SetLineWidth(3)
UncInPtandNJets[0].SetLineWidth(3)
UncInPtandNJets[2].Draw("same")
UncInPtandNJets[3].SetLineColor(kGreen+3)
UncInPtandNJets[3].Draw("same")
UncInPtandNJets[0].SetLineColor(kBlack)
UncInPtandNJets[0].Draw("same")
leg = TLegend(0.55, 0.7, 0.85, 0.90);
leg.SetTextFont(42)
leg.AddEntry(UncInPtandNJets[0], "p_{T}^{V} bins uncertainty", "l");
leg.AddEntry(UncInPtandNJets[1], "#Delta_{1}", "l");
leg.AddEntry(UncInPtandNJets[2], "#Delta_{2}", "l");
leg.AddEntry(UncInPtandNJets[3], "Total", "l");
leg.SetBorderSize(0);
leg.Draw('same');
UncInPtandNJets[3].Draw("same")
cB.SetTickx(0); cB.SetTicky(0);
if CMS:cB.SaveAs("pTBinsJetsUnc_CMS.pdf")
else: cB.SaveAs("pTBinsJetsUnc_central.pdf")

MAXVAL=[]
for i in range(0,NVar):
    MAXVAL.insert(i,scaleVarsRebinned[i].GetMaximum())


_MYW = 800; _MYH = 600
_MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
_MYL = 0.14*_MYW; _MYR = 0.18*_MYW
cB=0;
cB=TCanvas("cB","cB",_MYW,_MYH);
cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
centralScaleRebinned.SetLineColor(kRed)
centralScaleRebinned.SetYTitle("Cross-section")
centralScaleRebinned.SetAxisRange(0, 1.1*max(MAXVAL), "Y");
#centralScaleRebinned.SetLineWidth(3)
centralScaleRebinned.Draw()
for i in range(0, 7):
    scaleVarsRebinned[i].SetLineColor(histcolors[i])
    #scaleVarsRebinned[i].SetLineWidth(2)
    scaleVarsRebinned[i].Draw("same")
#leg = TLegend(0.5, 0.5, 0.7, 0.90);
leg = TLegend(0.55, 0.4, 0.75, 0.90);
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.SetTextSize(0.04)
for i in range(0, 7):
    leg.AddEntry(scaleVarsRebinned[i], scaleTitles[i], "l");
leg.Draw('same');
centralScaleRebinned.Draw("same")
cB.SetTickx(0); cB.SetTicky(0);
cB.SaveAs("XsectionpTJetsBinsUnc_powheg.pdf");


_MYW = 800; _MYH = 600
_MYT = 0.08*_MYH; _MYB = 0.14*_MYH;
_MYL = 0.14*_MYW; _MYR = 0.18*_MYW
MAXVAL=[]
MINVAL=[]
for i in range(0,NVar):
    scaleVarsRebinnedDiff[i].Divide(centralScaleRebinned)
    MAXVAL.insert(i,scaleVarsRebinnedDiff[i].GetMaximum())
    MINVAL.insert(i,scaleVarsRebinnedDiff[i].GetMinimum())

cB=0;
cB=TCanvas("cB","cB",_MYW,_MYH);
cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
scaleVarsRebinnedDiff[0].SetLineColor(kGray)
scaleVarsRebinnedDiff[0].SetLineStyle(kDashed)
scaleVarsRebinnedDiff[0].SetYTitle("Relative variation")
scaleVarsRebinnedDiff[0].SetTitle("")
scaleVarsRebinnedDiff[0].SetAxisRange(-1.1*max(MAXVAL), 1.8*max(MAXVAL), "Y");
scaleVarsRebinnedDiff[0].SetLineWidth(3)
scaleVarsRebinnedDiff[0].Draw("")
for i in range(1, 7):
    if i==9 or i==4:
        if i==4:scaleVarsRebinnedDiff[i].SetLineColor(38)
        else: scaleVarsRebinnedDiff[i].SetLineColor(28)
    else:scaleVarsRebinnedDiff[i].SetLineColor(i+1)
    #scaleVarsRebinnedDiff[i].SetLineWidth(3)
    scaleVarsRebinnedDiff[i].Draw("same")
#leg = TLegend(0.5, 0.5, 0.7, 0.90);
leg = TLegend(0.4, 0.68, 0.8, 0.90);
leg.SetNColumns(2);
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.SetTextSize(0.02)
leg.AddEntry(0, "", "");
leg.AddEntry(scaleVarsRebinnedDiff[0], "nominal", "l");
for i in range(1, 7):
    leg.AddEntry(scaleVarsRebinnedDiff[i], scaleTitles[i], "l");
leg.Draw('same');
cB.SetTickx(0); cB.SetTicky(0);
cB.SaveAs("XsectionpTJetsBinsUnc_powheg_Relative.pdf");

##merging according to the analysis splitting scheme ZH: 75-150 GeV (merging 3 bins), 150-250 0J, 150-250 >=1J (merging 2 bins), 250-inf GeV (merging 6 bins)
#pTJetstitlesMerged = ["0-150 GeV","150-250 GeV0J", "150-250 GeV GE1J",">250 GeV"]
#histMerged = TH1F("histMerged", "histMerged", 4, 0, 4)
##deltagroup1 = (UncInPtandNJets[3].GetBinContent(5)*centralScaleRebinned.GetBinContent(4) + UncInPtandNJets[3].GetBinContent(6)*centralScaleRebinned.GetBinContent(5) + UncInPtandNJets[3].GetBinContent(7)*centralScaleRebinned.GetBinContent(6))/(centralScaleRebinned.GetBinContent(6) + centralScaleRebinned.GetBinContent(5) + centralScaleRebinned.GetBinContent(4))
#n0 = 2
#deltagroup1 = 0
#for i in range(0,6):
#    deltagroup1 +=  UncInPtandNJets[3].GetBinContent(i+n0)*centralScaleRebinned.GetBinContent(i+n0-1)
#deltagroup1 = deltagroup1/centralScaleRebinned.Integral(1, 6)
#deltagroup2 = UncInPtandNJets[3].GetBinContent(8)
#deltagroup3 = (UncInPtandNJets[3].GetBinContent(9)*centralScaleRebinned.GetBinContent(8) + UncInPtandNJets[3].GetBinContent(10)*centralScaleRebinned.GetBinContent(9))/(centralScaleRebinned.GetBinContent(8) + centralScaleRebinned.GetBinContent(9))
#n0 = 11
#deltagroup4 = 0;
#for i in range(0,6):    
#    deltagroup4 +=  UncInPtandNJets[3].GetBinContent(i+n0)*centralScaleRebinned.GetBinContent(i+n0-1)
#deltagroup4 = deltagroup4/centralScaleRebinned.Integral(10, 15)
#histMerged.SetBinContent(1,deltagroup1)
#histMerged.SetBinContent(2,deltagroup2)
#histMerged.SetBinContent(3,deltagroup3)
#histMerged.SetBinContent(4,deltagroup4)
#histMerged.GetXaxis().SetBinLabel(1, pTJetstitlesMerged[0])
#histMerged.GetXaxis().SetBinLabel(2, pTJetstitlesMerged[1])
#histMerged.GetXaxis().SetBinLabel(3, pTJetstitlesMerged[2])
#histMerged.GetXaxis().SetBinLabel(4, pTJetstitlesMerged[3])
#
#B=0;
#cB=TCanvas("cB","cB",_MYW,_MYH);
#cB.SetLeftMargin( _MYL/_MYW );  cB.SetRightMargin( _MYR/_MYW );
#cB.SetTopMargin( _MYT/_MYH );   cB.SetBottomMargin( _MYB/_MYH );
#histMerged.SetLineColor(kRed)
##histMerged.SetAxisRange(-0.15, 0.25, "Y");
#histMerged.SetYTitle("Relative QCD uncertainty")
#histMerged.Draw()
#if CMS:cB.SaveAs("MergedUnc_CMS.pdf")
#else: cB.SaveAs("MergedUnc_central.pdf")
#
